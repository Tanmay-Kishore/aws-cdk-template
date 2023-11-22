"""
# AWS IAM Construct Library

This construct library allows you to create AWS IAM Resources.
"""
from typing import List
from aws_cdk import (
    Stack,
    aws_iam as iam
)


class IamConstruct():
    """
    # AWS IAM Construct Class
    ### This class holds various methods to create AWS IAM Resources.
    * `create_iam_role`
    * `create_iam_policy`
    * `create_iam_managed_policy`
    """

    @staticmethod
    def create_iam_role(
        stack: Stack,
        config: dict,
        env: str,
        role_name: str,
        assumed_by_service: str
    ) -> iam.Role:
        """
        ## Create an IAM Role
        Use this method to create an IAM Role.

        * param `stack`: A root construct which represents a CloudFormation Stack.
        * param `config`: A dictionary that contains key value pairs for variable substitution based on deployment environments.
        * param `env`: The deployment environment. No need to specify dev, stg, or prd as it is dynamically selected by the CI/CD Pipeline.
        * param `role_name`: The name of the IAM Role that will get created.
        * param `assumed_by_service`: The name of the aws service that will assume this role. Just write 'lambda' instead of writing 'lambda.amazonaws.com'
        * returns `iam.Role`
        """
        return iam.Role(
            scope=stack,
            id=f"{config[env]['appName']}-{role_name}-Role",
            assumed_by=iam.ServicePrincipal(
                f"{assumed_by_service}.amazonaws.com"),
            role_name=f"{config[env]['appName']}-{role_name}-role"
        )

    @staticmethod
    def create_iam_policy(
        stack: Stack,
        config: dict,
        env: str,
        policy_name: str,
        list_of_statements: List[iam.PolicyStatement]
    ) -> iam.Policy:
        """
        ## Create an IAM Policy
        Use this method to create an IAM Policy.

        * param `stack`: A root construct which represents a CloudFormation Stack.
        * param `config`: A dictionary that contains key value pairs for variable substitution based on deployment environments.
        * param `env`: The deployment environment. No need to specify dev, stg, or prd as it is dynamically selected by the CI/CD Pipeline.
        * param `policy_name`: The name of the IAM Policy that will get created.
        * param `list_of_statements`: A list of iam.PolicyStatement to be added to the managed policy.
        * returns `iam.Policy`
        """
        return iam.Policy(
            scope=stack,
            id=f"{config[env]['appName']}-{policy_name}-policy",
            statements=list_of_statements
        )

    @staticmethod
    def create_iam_managed_policy(
        stack: Stack,
        config: dict,
        env: str,
        policy_name: str,
        list_of_statements: List[iam.PolicyStatement]
    ) -> iam.ManagedPolicy:
        """
        ## Create an IAM Managed Policy
        Use this method to create an IAM Managed Policy.

        * param `stack`: A root construct which represents a CloudFormation Stack.
        * param `config`: A dictionary that contains key value pairs for variable substitution based on deployment environments.
        * param `env`: The deployment environment. No need to specify dev, stg, or prd as it is dynamically selected by the CI/CD Pipeline.
        * param `policy_name`: The name of the IAM Managed Policy that will get created.
        * param `list_of_statements`: A list of iam.PolicyStatement to be added to the managed policy.
        * returns `iam.Policy`
        """
        return iam.ManagedPolicy(
            scope=stack,
            id=f"{config[env]['appName']}-{policy_name}",
            managed_policy_name=f"{config[env]['appName']}-{policy_name}-managed-policy",
            statements=list_of_statements
        )

    @staticmethod
    def get_chatbot_policy() -> iam.PolicyStatement:
        """
        ## Get ChatBot policy
        Use this method to get required permissions for ChatBot.
        """
        return iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "cloudwatch:Describe*",
                "cloudwatch:Get*",
                "cloudwatch:List*",
                "sns:ListSubscriptionsByTopic",
                "sns:ListTopics",
                "sns:Unsubscribe",
                "sns:Subscribe",
                "sns:ListSubscriptions",
                "logs:PutLogEvents",
                "logs:CreateLogStream",
                "logs:DescribeLogStreams",
                "logs:CreateLogGroup",
                "logs:DescribeLogGroups"
            ],
            resources=["*"]
        )
