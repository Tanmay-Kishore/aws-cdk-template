"""
# AWS Cloudformation Stack Construct Library

This construct library creates Cloudformation Stack for your CDK App.
"""
from typing import List, Dict
from aws_cdk import (
    Duration,
    Stack,
    Tags,
    aws_lambda as _lambda,
)
from constructs import Construct
from .iam_construct import IamConstruct
from .lambda_construct import LambdaConstruct
from .layer_construct import LayerConstruct
from .s3_construct import S3Construct


class MainProjectStack(Stack):
    """
    ## AWS Cloudformation Stack Construct Class
    This class holds all methods to create AWS Cloudformation Stack and resources inside the stack.
    * `create_stack`
    * `create_all_lambda_functions`
    * `create_all_layers`
    * `create_all_buckets`
    """

    def __init__(
        self,
        env_var: str,
        scope: Construct,
        app_id: str,
        config: dict,
        **kwargs
    ) -> None:
        """
        ## Create a CloudFormation Stack
        Use this method to create your CloudFormation Stack.

        * param `env_var`: The deployment environment that your CloudFormation Stack will be deployed to. Permitted values: dev | stg | prd
        * param `scope`: A root construct which represents a single CDK App.
        * param `app_id`: Name of your CDK App.
        * param `config`: A dictionary that contains key value pairs for variable substitution based on deployment environments.
        * returns `None`
        """
        super().__init__(scope, app_id, **kwargs)
        self.env_var = env_var
        self.config = config
        MainProjectStack.create_stack(self, self.config, self.env_var)

    def create_stack(
        stack: Stack,
        config: dict,
        env: str
    ) -> None:
        """
        ## Create resources inside a CloudFormation Stack
        Use this method to create resources in your CloudFormation Stack.

        * param `stack`: A root construct which represents a CloudFormation Stack.
        * param `config`: A dictionary that contains key value pairs for variable substitution based on deployment environments.
        * param `env`: The deployment environment. No need to specify dev, stg, or prd as it is dynamically selected by the CI/CD Pipeline.
        * returns `None`
        """
        # buckets = MainProjectStack.create_all_buckets(stack=stack, config=config, env=env)

        layers = MainProjectStack.create_all_layers(
            stack=stack, config=config, env=env)

        MainProjectStack.create_all_lambda_functions(
            stack=stack, config=config, env=env, layers=[layers['sample_layer']])

        MainProjectStack.add_tags(
            stack=stack,
            config=config
        )

    @staticmethod
    def create_all_lambda_functions(
        stack: Stack,
        config: dict,
        env: str,
        layers: List[_lambda.LayerVersion] = None
    ) -> Dict[str, _lambda.Function]:
        """
        ## Create Lambda Functions
        Use this method to create all lambda functions that you need in your CloudFormation Stack.

        * param `stack`: A root construct which represents a CloudFormation Stack.
        * param `config`: A dictionary that contains key value pairs for variable substitution based on deployment environments.
        * param `env`: The deployment environment. No need to specify dev, stg, or prd as it is dynamically selected by the CI/CD Pipeline.
        * param `layers`: A list of layers to add to the function's execution environment. Layers are packages of libraries or other dependencies that can be used by multiple functions. Default: - No layers.
        * returns `dictionary`: Returns a dictionary with names of lambda functions as keys and aws_lambda.Function object as its value.
        """
        lambdas = {}
        # sample lambda ----------------------------------------------------------------------------------------------
        env_variable = {
            "REGION": "us-east-1",
            "APP_NAME": "mcc-rta-twitter-cdk-app"
        }
        lambdas["sample_lambda"] = LambdaConstruct.create_lambda_function(
            stack=stack,
            config=config,
            env=env,
            lambda_name="sample_lambda",
            time_out=Duration.minutes(8),
            layers=layers,
            env_variables=env_variable
        )
        return lambdas

    @staticmethod
    def create_all_layers(
        stack: Stack,
        config: dict,
        env: str
    ) -> Dict[str, _lambda.LayerVersion]:
        """
        ## Create layers
        Use this method to create layers in your CloudFormation Stack, which can then be attached to lambda functions.

        * param `stack`: A root construct which represents a CloudFormation Stack.
        * param `config`: A dictionary that contains key value pairs for variable substitution based on deployment environments.
        * param `env`: The deployment environment. No need to specify dev, stg, or prd as it is dynamically selected by the CI/CD Pipeline.
        * returns `dictionary`: Returns a dictionary with names of layers as keys and aws_lambda.LayerVersion object as its value.
        """
        layers = {}
        # sample layer -----------------------------------------------------------------------------------------------
        layers["sample_layer"] = LayerConstruct.create_layer(
            stack=stack,
            config=config,
            env=env,
            layer_name="sample_layer"
        )

        return layers

    @staticmethod
    def create_all_buckets(
        stack: Stack,
        config: dict,
        env: str
    ):
        """
        ## Creates Buckets
        Use this method to create all buckets required in your CFN Stack.

        * param `stack`: A root construct which represents a CloudFormation Stack.
        * param `config`: A dictionary that contains key value pairs for variable substitution based on deployment environments.
        * param `env`: The deployment environment. No need to specify dev, stg, or prd as it is dynamically selected by the CI/CD Pipeline.
        * returns `dictionary`: Returns a dictionary with names of buckets as keys and aws_s3.Bucket object as its value.
        """
        buckets = {}
        buckets['request_bucket'] = S3Construct.create_bucket(
            stack=stack,
            config=config,
            env=env,
            bucket_name="rta-twitter-request"
        )
        buckets['process_bucket'] = S3Construct.create_bucket(
            stack=stack,
            config=config,
            env=env,
            bucket_name="rta-twitter-process"
        )
        return buckets

    @staticmethod
    def add_tags(
        stack: Stack,
        config: dict
    ) -> None:
        """
        ## Add Tags
        Use this method to tag all the resources in your CloudFormation Stack.

        * param `stack`: A root construct which represents a CloudFormation Stack.
        * param `config`: A dictionary that contains key value pairs for variable substitution based on deployment environments.
        * returns `None`
        """
        Tags.of(stack).add('Owned by', config["global"]["sourceIdentifier"])
        Tags.of(stack).add('App Name', config["global"]["appName"])
