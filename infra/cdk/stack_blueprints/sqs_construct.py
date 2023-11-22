"""
# AWS SQS Construct Library

This construct library allows you to create AWS SQS and related Resources.
"""
from typing import List
from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
    aws_iam as iam
)

class SqsConstruct():
    """
    # AWS SQS Construct Class
    ### This class holds all methods to create AWS SQS and related Resources.
    * `create_sqs_queue`
    * `get_sqs_read_permissions`
    * `get_sqs_read_write_permissions`
    * `grant_publish_to_sns_permissions`
    """

    @staticmethod
    def create_sqs_queue(
        stack: Stack,
        config: dict,
        env: str,
        queue_name: str,
        dlq_name: sqs.Queue = None
    ) -> sqs.Queue:
        """
        ## Create an SNS Topic.
        # Use this method to create an SNS Topic in your CloudFormation Stack.
       
        * param `stack`: A root construct which represents a CloudFormation Stack.
        * param `config`: A dictionary that contains key value pairs for variable substitution based on deployment environments.
        * param `env`: The deployment environment. No need to specify dev, stg, or prd as it is dynamically selected by the CI/CD Pipeline.
        * param `queue_name`: The name of the Queue.
        * param `dlq_name`: (Optional) Name of another queue which will be used as a Dead-Letter Queue
        * returns `sqs.Queue`: Returns an object of type aws_sqs.Queue
        """
        dict_props = {
            "queue_name": queue_name,
            "retention_period": Duration.days(90)
        }
        if dlq_name is not None:
            dict_props['dead_letter_queue'] = sqs.DeadLetterQueue(max_receive_count=100,queue=dlq_name)
        return sqs.Queue(
            scope=stack,
            id=f"{config[env]['appName']}-{queue_name}-{config[env]['awsRegion']}",
            **dict_props
        )

    @staticmethod
    def get_sqs_read_permission(
        principals: List[str],
        resources: str = None
    ) -> iam.PolicyStatement:
        """
        ## Get SQS Read only Permission
        Use this method to get Read only permissions for an SQS Queue as a PolicyStatement.

        * :param `principals`: A list of object of type aws_iam.Principal.
        * :param `resources`: A list of all the resources for which you want these permissions.
        * returns `iam.PolicyStatement`: returns an object of type aws_iam.PolicyStatement.
        """
        policy = iam.PolicyStatement(
        principals=principals,
        effect=iam.Effect.ALLOW,
        actions=[
            "sqs:GetQueueAttributes",
            "sqs:GetQueueUrl",
            "sqs:ListDeadLetterSourceQueues",
            "sqs:ListQueues"
        ])

        if resources is not None:
            for resource in resources:
                policy.add_resources(resource)
        else:
            policy.add_all_resources()

        return policy

    @staticmethod
    def get_sqs_read_write_permission(
        principals: List[str],
        resources: str = None
    ) -> iam.PolicyStatement:
        """
        ## Get SQS Read Write Permission
        Use this method to get Read-Write permissions for an SQS Queue as a PolicyStatement.

        * :param `principals`: A list of object of type aws_iam.Principal.
        * :param `resources`: A list of all the resources for which you want these permissions.
        * returns `iam.PolicyStatement`: returns an object of type aws_iam.PolicyStatement.
        """
        policy = iam.PolicyStatement(
        principals=principals,
        effect=iam.Effect.ALLOW,
        actions=[
            "sqs:GetQueueAttributes",
            "sqs:GetQueueUrl",
            "sqs:ListDeadLetterSourceQueues",
            "sqs:ListQueues",
            "sqs:SendMessage"
        ])

        if resources is not None:
            for resource in resources:
                policy.add_resources(resource)
        else:
            policy.add_all_resources()

        return policy