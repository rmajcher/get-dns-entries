# get-dns-entries
Get Route53 DNS entries for provided record

## Script Execution  
usage example:  
`python3 get-dns.py -r service-bootstrap.clusters.pluto.tv -n 5`  

help message:  
```
Create RSA Key and Upload them to CloudFront for siloh signed URL/signed cookies

-h, --help            
  show this help message and exit
-t TIER, --tier TIER
  Specify other SecOps user tier default: ProdOpsTier4
-r RECORD, --record RECORD
  Specify other DNS record to get Route53 config
-n NUMBEROFENTRIES, --numberofentries NUMBEROFENTRIES
  Specify number of entries to return default: 1
-rt RECORDTYPE, --recordtype RECORDTYPE
  Specify record type SOA|A|TXT|NS|CNAME|MX|NAPTR|PTR|SRV|SPF|AAAA|CAA|DS
```  

output:  
```
MBP-Russell:get-dns-entries rmajcher$ python3 get-dns.py -r service-bootstrap.clusters.pluto.tv -n 5
[
    {
        "Name": "service-bootstrap.clusters.pluto.tv.",
        "Type": "A",
        "SetIdentifier": "service-bootstrap-ecs",
        "Weight": 0,
        "AliasTarget": {
            "HostedZoneId": "Z1ZF3WMUCEYZF2",
            "DNSName": "\\052.bootstrap4-live.clusters.pluto.tv.",
            "EvaluateTargetHealth": false
        }
    },
    {
        "Name": "service-bootstrap.clusters.pluto.tv.",
        "Type": "A",
        "SetIdentifier": "service-bootstrap-eks",
        "Weight": 0,
        "AliasTarget": {
            "HostedZoneId": "Z26RNL4JYFTOTI",
            "DNSName": "k8s-istiosys-istioing-4b5bb4083d-d82c2ba5d7a53e05.elb.us-east-1.amazonaws.com.",
            "EvaluateTargetHealth": false
        }
    },
    {
        "Name": "service-bootstrap.clusters.pluto.tv.",
        "Type": "A",
        "SetIdentifier": "service-bootstrap-eks-new-1",
        "Weight": 0,
        "AliasTarget": {
            "HostedZoneId": "Z35SXDOTRQ7X7K",
            "DNSName": "k8s-istiosys-external-22eb4155c7-1289415235.us-east-1.elb.amazonaws.com.",
            "EvaluateTargetHealth": false
        }
    },
    {
        "Name": "service-bootstrap.clusters.pluto.tv.",
        "Type": "A",
        "SetIdentifier": "service-bootstrap-eks-new-2",
        "Weight": 0,
        "AliasTarget": {
            "HostedZoneId": "Z35SXDOTRQ7X7K",
            "DNSName": "k8s-istiosys-external-9d3260c620-412651427.us-east-1.elb.amazonaws.com.",
            "EvaluateTargetHealth": false
        }
    },
    {
        "Name": "service-bootstrap.clusters.pluto.tv.",
        "Type": "A",
        "SetIdentifier": "service-bootstrap-globalaccelerator",
        "Weight": 100,
        "AliasTarget": {
            "HostedZoneId": "Z2BJ6XQ5FK7U4H",
            "DNSName": "a66dc43f216664758.awsglobalaccelerator.com.",
            "EvaluateTargetHealth": false
        }
    }
]
```
