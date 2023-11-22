"""
# AWS SNS Construct Library

This construct library allows you to create AWS SNS and related Resources.
"""
from typing import List
from aws_cdk import (
    Stack,
    aws_sns as sns,
    aws_iam as iam,
    aws_sns_subscriptions as sns_subs
)


class SnsConstruct():
    """
    # AWS SNS Construct Class
    ### This class holds all methods to create AWS SNS and related Resources.
    * `create_sns_topic`
    * `create_sns_email_subscription`
    * `get_sns_read_permissions`
    * `get_sns_read_write_permissions`
    * `grant_publish_to_sns_permissions`
    """

    @staticmethod
    def create_sns_topic(
        stack: Stack,
        config: dict,
        env: str,
        topic_name: str,
    ) -> sns.Topic:
        """
        ## Create an SNS Topic.
        Use this method to create an SNS Topic in your CloudFormation Stack.

        * param `stack`: A root construct which represents a CloudFormation Stack.
        * param `config`: A dictionary that contains key value pairs for variable substitution based on deployment environments.
        * param `env`: The deployment environment. No need to specify dev, stg, or prd as it is dynamically selected by the CI/CD Pipeline.
        * param `topic_name`: The name of the sns topic. 
        * returns `sns.Topic`: Returns an object of type aws_sns.Topic
        """
        return sns.Topic(
            scope=stack,
            id=f"{config[env]['appName']}-{topic_name}-{config[env]['awsRegion']}",
            display_name=topic_name,
            topic_name=topic_name
        )

    @staticmethod
    def create_sns_email_subscription(
        sns_topic: sns.Topic,
        email_address: str
    ) -> sns.Topic:
        """
        ## Create an email subscription for an SNS Topic.
        Use this method to create an email subscription for an SNS Topic in your CloudFormation Stack.

        * :param `sns.Topic`: An object of type aws_sns.Topic.
        * :param `email_address`: The email address which you want to subscribe to the SNS Topic.
        """
        return sns_topic.add_subscription(sns_subs.EmailSubscription(email_address))

    @staticmethod
    def get_sns_read_permissions(
        principals: List[str],
        resources: List[str] = None
    ) -> iam.PolicyStatement:
        """
        ## Get SNS Read only Permission
        Use this method to get Read only permissions for an SNS Topic as a PolicyStatement.

        * :param `principals`: A list of object of type aws_iam.Principal.
        * :param `resources`: A list of all the resources for which you want these permissions.
        * returns `iam.PolicyStatement`: returns an object of type aws_iam.PolicyStatement.
        """
        policy = iam.PolicyStatement(
            principals=principals,
            effect=iam.Effect.ALLOW,
            actions=[
                "sns:GetTopicAttributes",
                "sns:List*"
            ])

        if resources is not None:
            for resource in resources:
                policy.add_resources(resource)
        else:
            policy.add_all_resources()

        return policy

    @staticmethod
    def get_sns_read_write_permissions(
        principals: List[str],
        resources: List[str] = None
    ) -> iam.PolicyStatement:
        """
        ## Get SNS Read Write Permission
        Use this method to get Read-Write permissions for an SNS Topic as a PolicyStatement.

        * :param `principals`: A list of object of type aws_iam.Principal.
        * :param `resources`: A list of all the resources for which you want these permissions.
        * returns `iam.PolicyStatement`: returns an object of type aws_iam.PolicyStatement.
        """
        policy = iam.PolicyStatement(
            principals=principals,
            effect=iam.Effect.ALLOW,
            actions=[
                "sns:GetTopicAttributes",
                "sns:List*",
                "sns:Subscribe",
                "sns:Unsubscribe",
                "sns:Publish"
            ])

        if resources is not None:
            for resource in resources:
                policy.add_resources(resource)
        else:
            policy.add_all_resources()

        return policy

    @staticmethod
    def grant_publish_to_sns_permissions(
        sns_topic: sns.Topic,
        iam_grantee: iam.IGrantable,
    ) -> None:
        """
        ## Grant SNS Publish Permissions to an AWS IAM Principal (Role/User/Group)
        Use this method to grant Publish Permission for an SNS Topic.

        * :param `sns_topic`: An object of type aws_sns.Topic
        * :param `iam_grantee`: An AWS IAM Principal (Role/User/Group) for which you want to grant Read-Write permission of the SNS Topic.
        * returns `None`: returns None
        """
        sns_topic.grant_publish(iam_grantee)
