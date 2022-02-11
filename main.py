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


def list_rules(sg_id):
    '''
    revoke_security_group_egress
    '''
    try:
        response = ec2_client.describe_security_groups(
            GroupIds=[sg_id]
        )
        print(json.dumps(response, indent=2))
    except Exception as wtf:
        logger.error(wtf, exc_info=True)

    return None


def do_voo_doo():
    try:
        first = True
        for arg in sys.argv:
            if not first:
                print(arg)
                list_rules(arg)
            else:
                first = False
    except Exception as wtf:
        logger.error(wtf, exc_info=True)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        do_voo_doo()
