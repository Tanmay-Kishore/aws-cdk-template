"""
# AWS ChatBot Construct Library

This construct library allows you to create AWS ChatBot and related Resources.
"""
from aws_cdk import (
    Stack,
    aws_chatbot as chatbot,
    aws_sns as sns,
    aws_logs as logs
)
from .iam_construct import IamConstruct


class ChatbotConstruct():
    """
    # AWS ChatBot Construct Class
    ### This class holds various methods to create AWS ChatBot and related Resources.
    * `create_chatbot`
    """

    @staticmethod
    def create_chatbot(
        stack: Stack,
        config: dict,
        env: str,
        chatbot_name: str,
        sns_topic: sns.Topic,
        slack_channel_id: str
    ) -> chatbot.SlackChannelConfiguration:
        """
        ## Create a ChatBot
        Use this method to create a ChatBot to put messages in slack channels

        * param `stack`: A root construct which represents a CloudFormation Stack.
        * param `config`: A dictionary that contains key value pairs for variable substitution based on deployment environments.
        * param `env`: The deployment environment. No need to specify dev, stg, or prd as it is dynamically selected by the CI/CD Pipeline.
        * param `chatbot_name`: The name of the ChatBot that will get created.
        * param `sns_topic`: The SNS Topic which this chatbot will be bound to.
        * param `slack_channel_id`: The Slack Channel ID to which this chatbot will post messages/emails.
        * returns `chatbot.SlackChannelConfiguration`
        """
        chatbot_role = IamConstruct.create_iam_role(
            stack=stack,
            config=config,
            env=env,
            role_name=f"{chatbot_name}-role",
            assumed_by_service="chatbot"
        ).add_managed_policy(IamConstruct.create_iam_managed_policy(
            stack=stack,
            config=config,
            env=env,
            policy_name=f"{chatbot_name}-policy",
            list_of_statements=[IamConstruct.get_chatbot_policy()]
        ))
        return chatbot.SlackChannelConfiguration(
            scope=stack,
            id=f"{config[env]['appName']}-slack-chatbot",
            slack_workspace_id="T04PJ98MR",
            slack_channel_configuration_name=f"{config[env]['appName']}-{chatbot_name}",
            slack_channel_id=slack_channel_id,
            notification_topics=[sns_topic],
            log_retention=logs.RetentionDays.ONE_WEEK,
            logging_level=chatbot.LoggingLevel("INFO"),
            role=chatbot_role
        )
