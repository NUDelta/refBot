from slack import WebClient
from slackeventsapi import SlackEventAdapter
import os
import time
from flask import Flask

#slack_events_adapter = SlackEventAdapter(os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app)

# Initialize a Web API client

app = Flask(__name__)

# Create an events adapter and register it to an endpoint in the slack app for event injestion.
slack_events_adapter = SlackEventAdapter(os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app)


print(os.environ.get("SLACK_TOKEN"))
print(os.environ.get("SLACK_EVENTS_TOKEN"))


slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))

def background_task(channel,delay, actionItem):
    time.sleep(delay)
    reminder_text = "have you done "
    reminder_text += actionItem
    reminder_text += " yet?"

    slack_web_client.chat_postMessage(
    	   **{"channel": channel,
            "blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": reminder_text}}]}
    )

