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


def remove_rules(group):
    '''
    revoke_security_group_egress
    revoke_security_group_egress
            SecurityGroupRuleIds=[sg_id]
    '''
    egress_rules = []
    ingress_rules = []
    try:
        first = 'd14aec63'
        next_token = first
        while next_token:
            if next_token == first:
                response = ec2_client.describe_security_group_rules(
                    Filters=[
                        {
                            'Name': 'group-id',
                            'Values': [group]
                        }
                    ]
                )
            else:
                response = ec2_client.describe_security_group_rules(
                    NextToken=next_token,
                    Filters=[
                        {
                            'Name': 'group-id',
                            'Values': [group]
                        }
                    ]
                )
            next_token = response.get('NextToken')
            for rule in response.get('SecurityGroupRules', []):
                rule_id = rule.get('SecurityGroupRuleId')
                if rule.get('IsEgress'):
                    egress_rules.append(rule_id)
                else:
                    ingress_rules.append(rule_id)

        if len(egress_rules) > 0:
            logger.debug(json.dumps(egress_rules, indent=2))
            response = ec2_client.revoke_security_group_egress(
                GroupId=group,
                SecurityGroupRuleIds=egress_rules,
                DryRun=False
            )
            logger.info('revoke_security_group_egress() returned %s', json.dumps(response, indent=2))
        else:
            logger.info('%s had no egress rules', group)

        if len(ingress_rules) > 0:
            logger.debug(json.dumps(ingress_rules, indent=2))
            response = ec2_client.revoke_security_group_ingress(
                GroupId=group,
                SecurityGroupRuleIds=ingress_rules,
                DryRun=False
            )
            logger.info('revoke_security_group_ingress() returned %s', json.dumps(response, indent=2))
        else:
            logger.info('%s had no ingress rules', group)
    except Exception as wtf:
        logger.error(wtf, exc_info=True)

    return None


def do_voo_doo():
    try:
        groups = sys.argv[1:]
        for group in groups:
            remove_rules(group)
        for group in groups:
            response = ec2_client.delete_security_group(GroupId=group)
            logger.info('delete_security_group() returned %s', json.dumps(response, indent=2))
    except Exception as wtf:
        logger.error(wtf, exc_info=True)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        do_voo_doo()
