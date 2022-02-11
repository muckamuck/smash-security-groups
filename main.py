import sys
import json
import logging

import boto3

if __name__ == '__main__':
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format='[%(levelname)s] %(asctime)s.%(msecs)03d (%(module)s) %(message)s',
        datefmt='%Y/%m/%d-%H:%M:%S'
    )

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ec2_client = boto3.client('ec2')


def smash(groups):
    '''
    revoke_security_group_egress
    revoke_security_group_egress
            SecurityGroupRuleIds=[sg_id]
    '''
    try:
        first = 'd14aec63'
        next_token = first
        while next_token:
            if next_token == first:
                response = ec2_client.describe_security_group_rules(
                    Filters=[
                        {
                            'Name': 'group-id',
                            'Values': groups
                        }
                    ]
                )
            else:
                response = ec2_client.describe_security_group_rules(
                    NextToken=next_token,
                    Filters=[
                        {
                            'Name': 'group-id',
                            'Values': groups
                        }
                    ]
                )
            next_token = response.get('NextToken')
            print(json.dumps(response, indent=2))
    except Exception as wtf:
        logger.error(wtf, exc_info=True)

    return None


def do_voo_doo():
    try:
        groups = sys.argv[1:]
        if len(groups) > 0:
            smash(groups)
    except Exception as wtf:
        logger.error(wtf, exc_info=True)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        do_voo_doo()
