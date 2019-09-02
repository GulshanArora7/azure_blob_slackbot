import requests
import json
import slack

class SlackPost:
    def __init__(self, slack_channel_id, SLACK_BOT_TOKEN, data):
        self.SLACK_BOT_TOKEN = SLACK_BOT_TOKEN
        self.data = data
        self.slack_channel_id = slack_channel_id

    def slack_notification(self):
        slack_client = slack.WebClient(token=self.SLACK_BOT_TOKEN)
        slack_data = json.dumps(self.data)
        response = slack_client.chat_postMessage(channel=self.slack_channel_id, text=slack_data)
        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )