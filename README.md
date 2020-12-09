# ReflectionBot

prototype for metacognitive reflection project

# Installation and Setup

1. Setup a virtual environment 
2. $pip install rq redis slack flask
3. In first terminal: $python app.py
4. In second terminal: $ngrok http 3000 (you will need to install ngrok for this)
5. On slack api website: enter ngrok forwarding URL
6. In third terminal: $rq worker 
