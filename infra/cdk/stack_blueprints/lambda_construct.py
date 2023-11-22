"""
# AWS Lambda Construct Library

This construct library allows you to create AWS Lambda Functions.
"""
from typing import List
from aws_cdk import (
    Stack,
    Tags,
    Duration,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_s3 as s3,
    aws_sns as sns,
    aws_lambda_destinations as destinations,
    aws_ec2 as ec2
)


class LambdaConstruct():
    """
    # AWS Lambda Construct Class
    ### This class holds all methods to create AWS Lambda Functions.
    * `create_lambda_function`
    * `get_lambda_basic_permissions`
    * `grant_lambda_invoke_permission`
    * `grant_lambda_invoke_url_permission`
    """

    @staticmethod
    def create_lambda_function(
        stack: Stack,
        config: dict,
        env: str,
        lambda_name: str,
        env_variables: dict = None,
        handler: str = None,
        role: iam.Role = None,
        time_out: Duration = None,
        memory_size: int = None,
        language: _lambda.Runtime = None,
        layers: List[_lambda.LayerVersion] = None,
        reserved_concurrent_executions: int = None,
        on_failure_lambda: _lambda.Function = None,
        on_failure_sns: sns.Topic = None,
        code_location: _lambda.Code = None,
        retries: int = None,
        vpc: ec2.Vpc = None,
        subnets: List[ec2.Subnet] = None,
        security_groups: List[ec2.SecurityGroup] = None,
        allow_public_subnet: bool = None
    ) -> _lambda.Function:
        """
        ## Create a Lambda Function
        Use this method to create a single lambda function in your stack. Call this method multiple times to create multiple lambdas.

        * param `stack`: A root construct which represents a single CloudFormation stack.
        * param `config`: A dictionary that contains key value pairs for variable substitution based on deployment environments.
        * param `env`: The deployment environment. No need to specify dev, stg, or prd as it is dynamically selected by CI/CD.
        * param `lambda_name`: Name of your lambda function. Best practice is to pick up name of your lambda function from config.
        * param `env_variables`: A dictionary that contains variables that you want to use in your lambda function code.
        * param `handler`: The name of the method within your code that Lambda calls to execute your function. The format includes the file name. Default: "lambda_function.lambda_handler"
        * param `role`: Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. Default: - a new role will be created automatically
        * param `time_out`: The function execution time (in seconds) after which Lambda terminates the function. Defualt: 1 minute
        * param `memory_size`: The amount of memory, in MB, that is allocated to your Lambda function. Default: 256
        * param `language`: The runtime environment for the Lambda function that you are uploading. Default: Python-3.8
        * param `layers`: A list of layers to add to the function's execution environment. Layers are packages of libraries or other dependencies that can be used by multiple functions. Default: - No layers.
        * param `reserved_concurrent_executions`: The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit.
        * param `on_failure_lambda`: Lambda function that will be triggered on failed invocations.
        * param `on_failure_sns`: SNS Topic which will be triggered on failed invocations.
        * param `code_location`: The source code of your Lambda function. Default: src/lambda/<lambda_name>
        * param `retries`: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2
        * param `vpc`: VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. Default: - Function is not placed within a VPC.
        * param `subnets`: List of subnets to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Note: internet access for Lambdas requires a NAT gateway, so picking Public subnets is not allowed. Default: - the Vpc default strategy if not specified
        * param `security_groups`: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        * param `allow_public_subnet`: Lambda Functions in a public subnet can NOT access the internet. Use this property to acknowledge this limitation and still place the function in a public subnet. Default: false
        * returns `aws_lambda.Function`
        """
        dict_props = {
            "code": _lambda.Code.from_asset(f"../../src/lambda/{lambda_name}") if code_location is None else code_location,
            "handler": "lambda_function.lambda_handler" if handler is None else handler,
            "runtime": _lambda.Runtime.PYTHON_3_8 if language is None else language,
            "function_name": f"{config[env]['appName']}-{lambda_name}",
            "memory_size": 256 if memory_size is None else memory_size,
            "timeout": Duration.minutes(1) if time_out is None else time_out
        }
        if env_variables is not None:
            dict_props['environment'] = env_variables
        if role is not None:
            dict_props['role'] = role
        if layers is not None:
            dict_props['layers'] = layers
        if reserved_concurrent_executions is not None:
            dict_props['reserved_concurrent_executions'] = reserved_concurrent_executions
        if on_failure_lambda is not None:
            dict_props['on_failure'] = destinations.LambdaDestination(
                on_failure_lambda)
        if on_failure_sns is not None:
            dict_props['on_failure'] = destinations.SnsDestination(
                on_failure_sns)
        if retries is not None:
            dict_props['retry_attempts'] = retries
        if vpc is not None:
            dict_props['vpc'] = vpc
        if subnets is not None:
            dict_props['vpc_subnets'] = ec2.SubnetSelection(subnets=subnets)
        if security_groups is not None:
            dict_props['security_groups'] = security_groups
        if allow_public_subnet is not None:
            dict_props['allow_public_subnet'] = allow_public_subnet

        return _lambda.Function(
            scope=stack,
            id=f"{lambda_name}-{env}",
            **dict_props
        )

    @staticmethod
    def get_lambda_basic_permissions(
        config: dict,
        env: str
    ) -> iam.PolicyStatement:
        """
        ## Get basic lambda permissions
        Use this method to get basic lambda permissions as a PoliyStatement which can then be added to an IAM Role.

        :param `config`: Config file of the Stack.
        :param `env`: Env in which this Stack is going to be deployed.
        returns `iam.PolicyStatement`: returns an object of type aws_iam.PolicyStatement.
        """
        return iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            resources=[
                f"arn:aws:logs:{config[env]['awsRegion']}:{config[env]['awsAccount']}:*"]
        )

    @staticmethod
    def grant_lambda_invoke_permission(
        lambda_function: _lambda.Function,
        iam_grantee: iam.IGrantable
    ) -> None:
        """
        ## Grant Lambda Invoke Permissions
        Use this method to grant lambda invoke permission to an AWS IAM principal (Role/Group/User)

        :param `lambda_function`: A lambda function object of type aws_lambda.Function
        :param `iam_grantee`: An AWS IAM Principal (Role/Group/User)
        returns `None`: returns None
        """
        return lambda_function.grant_invoke(iam_grantee)

    @staticmethod
    def grant_lambda_invoke_url_permission(
        lambda_function: _lambda.Function,
        iam_grantee: iam.IGrantable
    ) -> None:
        """
        ## Grant Lambda Invoke URL Permissions
        Use this method to grant lambda invoke url permission to an AWS IAM principal (Role/Group/User)

        :param `lambda_function`: A lambda function object of type aws_lambda.Function
        :param `iam_grantee`: An AWS IAM Principal (Role/Group/User)
        returns `None`: returns None
        """
        return lambda_function.grant_invoke_url(iam_grantee)