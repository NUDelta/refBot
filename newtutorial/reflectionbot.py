import random
import data


    # Create a constant that contains the default text for the message


class reflectionBot:

	def _get_question(self, users_collection,channel):
		#print("in get question: self.question is: ", self.question, "&&&&&&&&&&&&&&&&&&")
		question = data.getQuestion(channel,users_collection)


		if question == 1:
			return [{"type": "section", "text": {"type": "mrkdwn", "text": "Going into your last mentor meeting earlier today, what was your riskiest risk?"}}]
		elif question == 2:
			return [{"type": "section", "text": {"type": "mrkdwn", "text": "Did a mentor give you any metacognitive feedback (i.e. feedback about the gaps in your process)? If so, what was it?"}}]
		elif question == 3:
			return [{"type": "section", "text": {"type": "mrkdwn", "text": "What learning strategy does your mentor's feedback fit in? Documenting process and progress, help seeking, grit and growth, or sprint planning and execution?"}}]
		elif question == 4:
			return [{"type": "section", "text": {"type": "mrkdwn", "text": "How could this learning strategy help you address the risks in your project?"}}]
		elif question == 5:
			return [{"type": "section", "text": {"type": "mrkdwn", "text": "How could this learning strategy help you address the risks in your process? (i.e. how you work and think)"}}]
		elif question == 6:
			return [{"type": "section", "text": {"type": "mrkdwn", "text": "What is one action item you can do in the following week to practice this learning strategy? (HINT: Think of things you have done in the past that helped you improve using this learning strategy.)"}}]
		elif question == 7:
			return [{"type": "section", "text": {"type": "mrkdwn", "text": "Does your action item have a defined start and end time (i.e. are you able to complete your task in a day/an hour/etc.)?"}}]
		elif question == 8:
			return [{"type": "section", "text": {"type": "mrkdwn", "text": "If you answered the previous question as ‘no’, what is an action item you can do that DOES have a defined start- and end-time?"}}]
		elif question == 9:
			return [{"type": "section", "text": {"type": "mrkdwn", "text": "When do you plan to do your action item?"}}]
		elif question == 10:
			return [{"type": "section", "text": {"type": "mrkdwn", "text": "I will remind you then!"}}]



    # Craft and return the entire message payload as a dictionary.
	def get_message_payload(self, users_collection, channel):
		return {
	        "channel": channel,
	        "blocks": self._get_question(users_collection,channel),
	    }
