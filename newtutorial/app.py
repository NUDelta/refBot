import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from reflectionbot import reflectionBot
import data
from flask_pymongo import PyMongo
import redis
import time
from rq import Queue
from reminder import background_task
import natural_time
from datetime import datetime
from datetime import date


mongo = PyMongo()


app = Flask(__name__)

# Create an events adapter and register it to an endpoint in the slack app for event injestion.
slack_events_adapter = SlackEventAdapter(
    os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app)

# Initialize a Web API client

print(os.environ.get("SLACK_TOKEN"))
print(os.environ.get("SLACK_EVENTS_TOKEN"))
print(os.environ.get("SLACK_BOT_TOKEN"))


slack_web_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


app.config["MONGO_URI"] = "mongodb+srv://neha:metacognition2021@cluster0.1rphe.mongodb.net/myUsers?retryWrites=true&w=majority"
mongo.init_app(app)
users_collection = mongo.db.userinfo
question_collection = mongo.db.questionResponses

r = redis.Redis()
q = Queue(connection=r)

global ref_bot


def first_question(channel, user_id):
    """Craft the CoinBot, flip the coin and send the message to the channel
    """
    global ref_bot

    result = slack_web_client.users_info(
        token=os.environ.get("SLACK_BOT_TOKEN"),
        user=user_id)

    print("result\n", result["user"]["real_name"], "\n\n")
    data.startReflection(
        channel, user_id, result["user"]["real_name"], users_collection)
    # Create a new Reflection Bot
    ref_bot = reflectionBot()
    # Get the onboarding message payload
    message = ref_bot.get_message_payload(users_collection, channel)
    slack_web_client.chat_postMessage(**message)


def second_question(channel, text, user_id):
    # this is triggered essentially any other time a message is sent to the bot...

    # this is where we should store the response
    global ref_bot
    result = slack_web_client.users_info(
        token=os.environ.get("SLACK_BOT_TOKEN"),
        user=user_id)

    data.storeResponse(channel, user_id, result["user"]["real_name"], text,
                       question_collection, users_collection)
    data.incrementQuestion(channel, users_collection)

    message = ref_bot.get_message_payload(users_collection, channel)

    # Post the onboarding message in Slack
    slack_web_client.chat_postMessage(**message)


# When a 'message' event is detected by the events adapter, forward that payload
# to this function.
@slack_events_adapter.on("message")
def message(payload):
    """Parse the message event, and if the activation string is in the text,
    simulate a coin flip and send the result.
    """
    print("message\n\n\n")
    print("payload: ", payload, "\n\n\n\n")
    # Get the event data from the payload
    event = payload.get("event", {})
    # Get the text from the event that came through
    text = event.get("text")
    #print(text,"----",event, "*************\n\n")

    if not text or text == "pass":
        return

    # Check and see if the activation phrase was in the text of the message.
    # If so, execute the code to flip a coin.
    if "start reflection" in text.lower():
        # Since the activation phrase was met, get the channel ID that the event
        # was executed on
        channel_id = event.get("channel")
        user_id = event.get("user")
        # Execute the flip_coin function and send the results of
        # flipping a coin to the channel
        return first_question(channel_id, user_id)
    elif "remind me" in text.lower():
        channel_id = event.get("channel")
        time_to_remind = natural_time.natural_time(text.lower())
        #today = date.today()
        action_item = data.getActionItem(channel_id, question_collection)
        #now = datetime.now()
        #print("time to remind:", time_to_remind, "now:", now, "*****")
        #print(time_to_remind - now)
        q.enqueue(background_task, channel_id, 10, action_item)
    elif text != "This content can't be displayed.":
        user_id = event.get("user")
        channel_id = event.get("channel")
        return second_question(channel_id, text, user_id)

        #channel_id = event.get("channel")
        # return question(channel_id)

        # Execute the flip_coin function and send the results of
        # flipping a coin to the channel


if __name__ == "__main__":
    # Create the logging object
    logger = logging.getLogger()

    # Set the log level to DEBUG. This will increase verbosity of logging messages
    logger.setLevel(logging.DEBUG)

    # Add the StreamHandler as a logging handler
    logger.addHandler(logging.StreamHandler())
    # Run our app on our externally facing IP address on port 3000 instead of
    # running it on localhost, which is traditional for development.
    app.run(host='0.0.0.0', port=3000)
