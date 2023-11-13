import boto3
import argparse
import json

description = \
"""Get Route53 DNS entries for provided record"""

parser = argparse.ArgumentParser(description = description)
parser.add_argument('-t', '--tier', required = False,
    help = 'Specify other SecOps user tier default: ProdOpsTier4', default = 'ProdOpsTier4')
parser.add_argument('-r', '--record', required = True,
    help = 'Specify other DNS record to get Route53 config')
parser.add_argument('-n', '--numberofentries', required = False,
    help = 'Specify number of entries to return default: 1', default = '1')
parser.add_argument('-rt', '--recordtype', required = False,
    help = 'Specify record type SOA|A|TXT|NS|CNAME|MX|NAPTR|PTR|SRV|SPF|AAAA|CAA|DS')
parser.add_argument('-a', '--activeweightonly', required = False,
    help = 'Only get active weights for records default: false', default = 'false')
args = parser.parse_args()

# domains to zone ID & account ID
hosted_zones_and_accounts = {
    'pluto.tv': {
        'zone_id': 'Z2Z8T9W8E08V8N',
        'account_id': 157385605725
    },
    'corp.pluto.tv': {
        'zone_id': 'Z1443TF62ZX7PA',
        'account_id': 157385605725
    },
    'clusters.pluto.tv': {
        'zone_id': 'Z1ZF3WMUCEYZF2',
        'account_id': 853581745927
    },
    'plutopreprod.tv': {
        'zone_id': 'Z6HWH9U3GR6BW',
        'account_id': 290745908312
    },
    'plutopreprod.tv': {
        'zone_id': 'Z6HWH9U3GR6BW',
        'account_id': 290745908312
    },
    'prd.pluto.tv': {
        'zone_id': 'Z37ZMHN4RVDCQA',
        'account_id': 322304022098
    },
    'live.prd.pluto.tv': {
        'zone_id': 'Z02338143RMSJB9SIO0B6',
        'account_id': 322304022098
    },
    'preprd.pluto.tv': {
        'zone_id': 'Z02607252F64PMO2S8NY',
        'account_id': 474014820769
    },
    'live.preprd.pluto.tv': {
        'zone_id': 'Z07755352NPR8HSHU31O5',
        'account_id': 474014820769
    },
    'nonprd.pluto.tv': {
        'zone_id': 'Z4AU3GYJBQVVQ',
        'account_id': 479133078108
    }
}

def assumerole(account_id):
    sts_client = boto3.client('sts')
    Assumed_Role_object = sts_client.assume_role(
        RoleArn = f"arn:aws:iam::{account_id}:role/{args.tier}",
        RoleSessionName = f"route53-dns-{args.tier}"
    )
    credentials=Assumed_Role_object['Credentials']
    route53_client = boto3.client(
        'route53', 'us-east-1',
        aws_access_key_id = credentials['AccessKeyId'],
        aws_secret_access_key = credentials['SecretAccessKey'],
        aws_session_token = credentials['SessionToken']
    )
    return route53_client

def main():
    # If record is the root record example: plutopreprod.tv
    if args.record in list(hosted_zones_and_accounts.keys()):
        domain = args.record
    # All other records besides root records
    elif 'www' in args.record:
        record_www_strip = args.record.strip('www')
        domain = record_www_strip.split(".", 1)[1]
    else:
        domain = args.record.split(".", 1)[1]
    route53_client = assumerole(hosted_zones_and_accounts[domain]['account_id'])

    # If number of entries argument is specified
    if args.numberofentries != '1':
        rhm = []
        # If specified a specific starting record type example: CNAME
        if args.recordtype:
            response = route53_client.list_resource_record_sets(
                HostedZoneId = hosted_zones_and_accounts[domain]['zone_id'],
                StartRecordName = args.record,
                StartRecordType = args.recordtype,
                MaxItems = args.numberofentries
            )['ResourceRecordSets']
        # All other searches will be generic for starting record type
        else:
            response = route53_client.list_resource_record_sets(
                HostedZoneId = hosted_zones_and_accounts[domain]['zone_id'],
                StartRecordName = args.record,
                MaxItems = args.numberofentries
            )['ResourceRecordSets']

        for i in range(0, len(response)):
            try:
                # Replace html encoded name with proper * wildcard character
                if "\\052." in response[i]['AliasTarget']['DNSName']:
                    response[i]['AliasTarget']['DNSName'] = (f"*.{response[i]['AliasTarget']['DNSName'].split('.', 1)[1]}")
            except:
                wildcard = 0
            try:
                # Only get active weight record and ommit 0 weights
                if 'true' in args.activeweightonly:
                    if response[i]['Weight'] > 0:
                        rhm.append(response[i])
                else:
                    rhm.append(response[i])
            except:
                weighted_record = 0
                rhm.append(response[i])

        # Print json response for record + number of entries
        pretty_json = json.dumps(rhm, indent=4)
        print(pretty_json)
    # Will automatically find the correct entries and put them in the json variable rhm
    else:
        rhm = []
        response = route53_client.list_resource_record_sets(
            HostedZoneId = hosted_zones_and_accounts[domain]['zone_id'],
            StartRecordName = args.record,
            MaxItems = '20'
        )['ResourceRecordSets']

        for i in range(0, len(response)):
            if f"{args.record}." == response[i]['Name']:
                if response[i]['Type'] in ['A', 'AAAA', 'CNAME']:
                    try:
                        # Replace html encoded name with proper * wildcard character
                        if "\\052." in response[i]['AliasTarget']['DNSName']:
                            response[i]['AliasTarget']['DNSName'] = (f"*.{response[i]['AliasTarget']['DNSName'].split('.', 1)[1]}")
                    except:
                        wildcard = 0
                    try:
                        # Only get active weight record and ommit 0 weights
                        if 'true' in args.activeweightonly:
                            if response[i]['Weight'] > 0:
                                rhm.append(response[i])
                        else:
                            rhm.append(response[i])
                    except:
                        weighted_record = 0
                        rhm.append(response[i])

        # Print json response for record
        pretty_json = json.dumps(rhm, indent=4)
        print(pretty_json)

if __name__ == '__main__':
    main()