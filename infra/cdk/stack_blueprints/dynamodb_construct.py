"""
# AWS DynamoDB Construct Library

This construct library allows you to create AWS DynamoDB and related Resources.
"""
from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_kms as kms,
    aws_iam as iam
)


class DynamodbConstruct():
    """
    # AWS DynamoDB Construct Class
    ### This class holds various methods to create AWS DynamoDB and related Resources.
    * `create_dynamodb_table`
    * `create_encrypted_dynamodb_table`
    * `create_dynamodb_table_with_sort_key`
    * `create_encrypted_dynamodb_table_with_sort_key`
    * `dynamodb_full_access_managed_policy`
    * `get_dynamodb_read_write_policy`
    """

    @staticmethod
    def create_dynamodb_table(
        stack: Stack,
        config: dict,
        env: str,
        table_name: str,
        partition_key: dynamodb.Attribute
    ) -> dynamodb.Table:
        """
        ## Create a DynamoDB Table
        Use this method to create an unencrypted DynamoDB Table.

        * param `stack`: A root construct which represents a CloudFormation Stack.
        * param `config`: A dictionary that contains key value pairs for variable substitution based on deployment environments.
        * param `env`: The deployment environment. No need to specify dev, stg, or prd as it is dynamically selected by the CI/CD Pipeline.
        * param `table_name`: The name of the DynamoDB Table that will get created.
        * param `partition_key`: A aws_dynamodb.Attribute object which defines your table's primary key.
        * returns `dynamodb.Table`
        """

        return dynamodb.Table(
            scope=stack,
            id=f"{config[env]['appName']}-dynamodb-{table_name}",
            table_name=f"{config[env]['appName']}-{table_name}",
            partition_key=partition_key
        )

    @staticmethod
    def create_encrypted_dynamodb_table(
        stack: Stack,
        config: dict,
        env: str,
        table_name: str,
        partition_key: dynamodb.Attribute,
        kms_key: kms.Key
    ) -> dynamodb.Table:
        """
        ## Create a DynamoDB Table
        Use this method to create an encrypted DynamoDB Table.

        * param `stack`: A root construct which represents a CloudFormation Stack.
        * param `config`: A dictionary that contains key value pairs for variable substitution based on deployment environments.
        * param `env`: The deployment environment. No need to specify dev, stg, or prd as it is dynamically selected by the CI/CD Pipeline.
        * param `table_name`: The name of the DynamoDB Table that will get created.
        * param `partition_key`: A aws_dynamodb.Attribute object which defines your table's primary key.
        * param `kms_key`: A aws_kms.Key object which will be used to encrypt/decrypt DynamoDB Table objects.
        * returns `dynamodb.Table`
        """

        return dynamodb.Table(
            scope=stack,
            id=f"{config[env]['appName']}-dynamodb-{table_name}",
            table_name=table_name,
            encryption=dynamodb.TableEncryption.CUSTOMER_MANAGED,
            encryption_key=kms_key,
            partition_key=partition_key
        )

    @staticmethod
    def grant_dynamodb_full_access(
        dynamodb_table: dynamodb.Table,
        iam_grantee: iam.IGrantable
    ) -> None:
        """
        ## Grant DynamoDB Full Access.
        Use this method to grant full access of a DynamoDB Table to an AWS IAM Principal (Role/User/Group)

        * param `dynamodb_table`: An object of type aws_dynamodb.Table.
        * param `iam_grantee`: An object of type aws_iam.IGrantable. Should be an AWS IAM Principal (Role/User/Group)
        """
        return dynamodb_table.grant_full_access(iam_grantee)

    @staticmethod
    def grant_dynamodb_read_write_data_access(
        dynamodb_table: dynamodb.Table,
        iam_grantee: iam.IGrantable,
        read_only: bool = True
    ) -> None:
        """
        ## Grant DynamoDB Read-Write Access.
        Use this method to grant Read-Write access of a DynamoDB Table to an AWS IAM Principal (Role/User/Group).

        * param `dynamodb_table`: An object of type aws_dynamodb.Table.
        * param `iam_grantee`: An object of type aws_iam.IGrantable. Should be an AWS IAM Principal (Role/User/Group).
        * param `read_only`: Set to True if you only want read permissions for the table. Set to False for Read-Write Permissions. Default - True (Read only permissions).
        """
        if read_only is True:
            return dynamodb_table.grant_read_data(iam_grantee)
        if read_only is False:
            return dynamodb_table.grant_read_write_data(iam_grantee)
