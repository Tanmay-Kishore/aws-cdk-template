"""
# AWS Cloudformation App Construct

This construct creates Cloudformation Stack(s) inside your CloudFormation App using CDK.
"""
from configparser import ConfigParser, ExtendedInterpolation
from stack_blueprints.stack import MainProjectStack
import aws_cdk as cdk


def main():
    """Main method that the CDK will execute."""
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read("../../.configrc/config.ini")
    _app = cdk.App()
    env = _app.node.try_get_context("env")

    MainProjectStack(
        env_var=env,
        app_id=config["global"]["appId"],
        scope=_app,
        config=config,
        env={
            "region": config[env]['awsRegion'],
            "account": config[env]['awsAccount']
        }
    )
    _app.synth()


main()
