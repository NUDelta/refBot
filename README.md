# ReflectionBot

prototype for metacognitive reflection project

# Installation and Setup

1. Setup a virtual environment
2. $pip install slack flask
3. In first terminal: $python app.py
4. In second terminal: $ngrok http 3000 (you will need to install ngrok for this)
5. On slack api website: enter ngrok forwarding URL as a redirect URL in OAuth& Permission page
6. On slack api website: enter ngrok forwarding URL as http://url/slack/events in Event Subscriptions page