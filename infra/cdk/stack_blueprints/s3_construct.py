"""
# AWS S3 Construct Library

This construct library allows you to create AWS S3 and related Resources.
"""
from aws_cdk import (
    Stack,
    Tags,
    aws_iam as iam,
    aws_s3 as s3,
    aws_kms as kms,
    aws_lambda as _lambda,
    aws_s3_notifications as s3_notify
)


class S3Construct():
    """
    # AWS S3 Construct Class
    ### This class holds all methods to create AWS S3 and related Resources.
    * `create_bucket`
    * `create_bucket_with_kms_encryption`
    * `add_s3_trigger_to_lambda`
    * `grant_bucket_permissions_to_role`
    * `grant_bucket_access_to_lambda`
    """
    @staticmethod
    def create_bucket(
        stack: Stack,
        config: dict,
        env: str,
        bucket_name: str
    ) -> s3.Bucket:
        """
        ## Create an S3 Bucket.
        Use this method to create an S3 Bucket in your CloudFormation Stack.

        * param `stack`: A root construct which represents a CloudFormation Stack.
        * param `config`: A dictionary that contains key value pairs for variable substitution based on deployment environments.
        * param `env`: The deployment environment. No need to specify dev, stg, or prd as it is dynamically selected by the CI/CD Pipeline.
        * param `bucket_name`: The name of the bucket. 
        * returns `s3.Bucket`: Returns an object of type aws_s3.Bucket
        """
        bucket = s3.Bucket(
            scope=stack,
            id=f"{config[env]['appName']}-{bucket_name}",
            bucket_name=f"{config[env]['appName']}-{bucket_name}"
        )
        Tags.of(bucket).add("Twitter-Scraper-Tag",
                            f"{config[env]['appName']}-s3-{bucket_name}")
        return bucket

    @staticmethod
    def create_bucket_with_kms_encryption(
        stack: Stack,
        config: dict,
        env: str,
        bucket_name: str,
        kms_key: kms.Key
    ) -> s3.Bucket:
        """
        ## Create a KMS encrypted S3 Bucket.
        Use this method to create a KMS encrypted S3 Bucket in your CloudFormation Stack.

        * param `stack`: A root construct which represents a CloudFormation Stack.
        * param `config`: A dictionary that contains key value pairs for variable substitution based on deployment environments.
        * param `env`: The deployment environment. No need to specify dev, stg, or prd as it is dynamically selected by the CI/CD Pipeline.
        * param `bucket_name`: The name of the bucket. 
        * returns `s3.Bucket`: Returns an object of type aws_s3.Bucket
        """
        return s3.Bucket(
            scope=stack,
            id=f"{config[env]['appName']}-{bucket_name}",
            encryption_key=kms_key,
            bucket_name=bucket_name
        )

    @staticmethod
    def add_s3_trigger_to_lambda(
        s3_bucket: s3.Bucket,
        lambda_function: _lambda.Function,
        prefix: str = None,
        suffix: str = None
    ) -> None:
        """Method to add an S3 trigger to a lambda function."""
        if prefix is not None or suffix is not None:
            s3_bucket.add_event_notification(
                s3.EventType.OBJECT_CREATED,
                s3_notify.LambdaDestination(lambda_function),
                s3.NotificationKeyFilter(prefix=prefix, suffix=suffix)
            )
        else:
            s3_bucket.add_event_notification(
                s3.EventType.OBJECT_CREATED,
                s3_notify.LambdaDestination(lambda_function)
            )

    @staticmethod
    def grant_bucket_permissions_to_role(
        s3_bucket: s3.Bucket,
        iam_role: iam.Role,
        read_only: bool = True,
    ) -> iam.IGrantable:
        """
        ## Grant permissions for S3 Bucket to IAM Role
        Method to grant permissions of an S3 Bucket to an IAM Role.

        * param `s3_bucket`: object of type aws_s3.Bucket
        * param `iam_role`: IAM Role which will have access to read data from the above s3 Bucket.
        * param `read_only`: (Optional) grants Read-Write access if False. Default: grants only Read access
        * returns `iam.IGrantable`: an object of type aws_iam.IGrantable
        """

        if read_only is True:
            return s3_bucket.grant_read(
                identity=iam_role
            )
        else:
            return s3_bucket.grant_read_write(
                identity=iam_role
            )

    @staticmethod
    def grant_bucket_access_to_lambda(
        s3_bucket: s3.Bucket,
        lambda_function: _lambda.Function,
        read_only: bool = True
    ) -> iam.IGrantable:
        """
        ## Grant Bucket Access to a Lambda Function
        Use this method to grant Read-Write access to a Lambda Function.

        * param `s3_bucket`: object of type aws_s3.Bucket.
        * param `lambda_function`: object of type aws_lambda.Function.
        * param `read_only`: (Optional) grants Read-Write access if False. Default: grants only Read access
        * returns `iam.IGrantable`: an object of type aws_iam.IGrantable
        """
        if read_only is True:
            return s3_bucket.grant_read(lambda_function)
        else:
            return s3_bucket.grant_read_write(lambda_function)
