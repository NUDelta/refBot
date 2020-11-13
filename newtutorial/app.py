import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from reflectionbot import reflectionBot
import data
from flask_pymongo import PyMongo
from celery import Celery


mongo = PyMongo()


# Initialize a Flask app to host the events adapter
app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
# Create an events adapter and register it to an endpoint in the slack app for event injestion.
slack_events_adapter = SlackEventAdapter(os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))


app.config["MONGO_URI"] = "mongodb+srv://olivia:oliviapassword@cluster0.1rphe.mongodb.net/myUsers?retryWrites=true&w=majority"
mongo.init_app(app)
users_collection = mongo.db.userinfo
question_collection = mongo.db.questionResponses


global ref_bot



@celery.task
def my_background_task(arg1, arg2):
    # some long running task here
    print("yo")

def first_question(channel,user_id):
    """Craft the CoinBot, flip the coin and send the message to the channel
    """
    global ref_bot

    data.startReflection(channel, user_id,users_collection)
    # Create a new Reflection Bot
    ref_bot = reflectionBot()
    #task = my_background_task.apply_async(args=[10, 20], countdown=30)

    # Get the onboarding message payload
    message = ref_bot.get_message_payload(users_collection, channel)
    slack_web_client.chat_postMessage(**message)

def second_question(channel, text, user_id):
    #this is triggered essentially any other time a message is sent to the bot...

    #this is where we should store the response
    global ref_bot
    data.storeResponse(channel, user_id,  text, question_collection, users_collection)
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
    #print("message\n\n\n")
    #print("payload: ", payload, "\n\n\n\n")
    # Get the event data from the payload
    event = payload.get("event", {})
    # Get the text from the event that came through
    text = event.get("text")
    #print(text,"----",event, "*************\n\n")


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
    elif text != "This content can't be displayed.":
        user_id = event.get("user")
        channel_id = event.get("channel")
        return second_question(channel_id, text, user_id)

        #channel_id = event.get("channel")
    	#return question(channel_id)

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