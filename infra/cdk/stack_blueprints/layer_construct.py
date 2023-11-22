"""
# AWS Lambda Layer Construct Library

This construct library allows you to create AWS Lambda Layers.
"""
from typing import List
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
)


class LayerConstruct():
    """
    # AWS Lambda Layers Construct Class
    ### This class holds all methods to create AWS Lambda Layers.
    * `create_layer`
    * `get_layer_from_arn`
    """

    @staticmethod
    def create_layer(
        stack: Stack,
        config: dict,
        env: str,
        layer_name: str,
        zipfile_location: str = None,
        compatible_runtimes: List[_lambda.Runtime] = None
    ) -> _lambda.LayerVersion:
        """
        ## Create a new Lambda Layer Version
        Use this method to create Lambda Layers in your CloudFormation Stack.

        * param `stack`: A root construct which represents a CloudFormation Stack.
        * param `config`: A dictionary that contains key value pairs for variable substitution based on deployment environments.
        * param `env`: The deployment environment. No need to specify dev, stg, or prd as it is dynamically selected by the CI/CD Pipeline.
        * param `layer_name`: The name of this layer. This name will be visible on AWS Console.
        * param `zipfile_location`: (Optional) The location of the zip that will be uploaded to your Lambda Layer. Default: - src/layer/layer_name.zip
        * param `compatible_runtimes`: (Optional) Languages and versions for which this layer has been created. Default: - Python-3.8.
        * returns `aws_lambda.LayerVersion`: an aws_lambda.LayerVersion object.
        """
        dict_props = {
            "code": _lambda.Code.from_asset(f"../../src/layer/{layer_name}.zip"),
            "layer_version_name": layer_name,
            "compatible_runtimes": [_lambda.Runtime.PYTHON_3_8]
        }

        if zipfile_location is not None:
            dict_props['code'] = _lambda.Code.from_asset(zipfile_location)

        if compatible_runtimes is not None:
            dict_props['compatible_runtimes'] = compatible_runtimes

        return _lambda.LayerVersion(
            scope=stack,
            id=f"{config[env]['appName']}-{layer_name}",
            **dict_props
        )

    @staticmethod
    def get_layer_from_arn(
        stack: Stack,
        config: dict,
        env: str,
        layer_arn: str
    ) -> _lambda.LayerVersion:
        """
        ## Import Lambda Layer in your stack.
        Use this method to import pre-existing layers on AWS to your CloudFormation Stack and attach it to your lambda functions.

        * param `stack`: A root construct which represents a CloudFormation Stack.
        * param `config`: A dictionary that contains key value pairs for variable substitution based on deployment environments.
        * param `env`: The deployment environment. No need to specify dev, stg, or prd as it is dynamically selected by the CI/CD Pipeline.
        * param `layer_arn`: The arn of the layer you want to import.
        * returns `aws_lambda.LayerVersion`: an aws_lambda.LayerVersion object.
        """
        return _lambda.LayerVersion.from_layer_version_arn(
            scope=stack,
            id=f"{config[env]['appName']}-{config[env]['awsRegion']}-layer",
            layer_version_arn=layer_arn
        )
