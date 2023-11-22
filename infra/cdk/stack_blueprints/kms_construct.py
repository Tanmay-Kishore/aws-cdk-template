"""
# AWS KMS Construct Library

This construct library allows you to create AWS KMS Resources.
"""
from aws_cdk import (
    Stack,
    aws_kms as kms,
    aws_iam as iam
)


class KmsConstruct():
    """
    # AWS KMS Construct Class
    ### This class holds all methods to create AWS KMS Resources.
    * `create_kms_key`
    * `get_kms_encrypt_decrypt_policy`
    """
    @staticmethod
    def create_kms_key(
        stack: Stack,
        config: dict,
        env: str
    ) -> kms.Key:
        """# Create KMS Key
        Use this method to create KMS Key to encrypt resources.

        * param `stack`: A root construct which represents a CloudFormation Stack.
        * param `config`: A dictionary that contains key value pairs for variable substitution based on deployment environments.
        * param `env`: The deployment environment. No need to specify dev, stg, or prd as it is dynamically selected by the CI/CD Pipeline.
        * returns `kms.Key`: returns a aws_kms.Key object.
        """
        return kms.Key(
            scope=stack,
            id=f"{config[env]['appName']}-{config[env]['awsRegion']}-kms-key",
            description=f"KMS Key for {config[env]['appName']}-{config[env]['awsRegion']}",
            enabled=True,
        )

    @staticmethod
    def grant_kms_encrypt_decrypt_access(
        kms_key: kms.Key,
        iam_grantee: iam.IGrantable
    ) -> None:
        """
        # Grant KMS Encrypt-Decrypt access.
        Use this method to grant KMS encrypt-decrypt access to an AWS IAM principal (Role/Group/User).

        * param `kms_key`: The KMS Key for which you need to grant permissions.
        * param `iam_role`: The IAM Role 
        * returns `None`: return None
        """
        return kms_key.grant_encrypt_decrypt(iam_grantee)
