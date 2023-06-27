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

args = parser.parse_args()

# domains to zone ID & account ID
hosted_zones_and_accounts = {
    'pluto.tv': {
        'zone_id': 'Z2Z8T9W8E08V8N',
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
    'prd.pluto.tv': {
        'zone_id': 'Z37ZMHN4RVDCQA',
        'account_id': 322304022098
    },
    'preprd.pluto.tv': {
        'zone_id': 'Z02607252F64PMO2S8NY',
        'account_id': 474014820769
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
    if args.record in list(hosted_zones_and_accounts.keys()):
        domain = args.record
    else:
        domain = args.record.split(".", 1)[1]
    route53_client = assumerole(hosted_zones_and_accounts[domain]['account_id'])

    if args.recordtype:
        response = route53_client.list_resource_record_sets(
            HostedZoneId = hosted_zones_and_accounts[domain]['zone_id'],
            StartRecordName = args.record,
            StartRecordType = args.recordtype,
            MaxItems = args.numberofentries
        )['ResourceRecordSets']
    else:
        response = route53_client.list_resource_record_sets(
            HostedZoneId = hosted_zones_and_accounts[domain]['zone_id'],
            StartRecordName = args.record,
            MaxItems = args.numberofentries
        )['ResourceRecordSets']

    pretty_json = json.dumps(response, indent=4)
    print(pretty_json)

if __name__ == '__main__':
    main()