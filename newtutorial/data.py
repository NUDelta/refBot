

def startReflection(channel, user_id,users_collection):
	if users_collection.find_one({"user_id": user_id}) == None:
		mydict = {"user_id": user_id, "channel_id":channel, 'question':1}
		users_collection.insert_one(mydict)
	else:
		myquery = { "user_id": user_id }
		newvalues = { "$set": { "question": 1 } }
		users_collection.update_one(myquery, newvalues)


def getQuestion(channel,users_collection):
	if users_collection.find_one({"channel_id": channel}) == None:
		pass
	else:
		question = users_collection.find_one({"channel_id": channel})['question']
		return question

def incrementQuestion(channel,users_collection):
	if users_collection.find_one({"channel_id": channel}) == None:
		pass
	else:
		question = users_collection.find_one({"channel_id": channel})['question']
		myquery = { "channel_id": channel }
		newvalues = { "$set": { "question": question+1 } }
		users_collection.update_one(myquery, newvalues)

def storeResponse(channel, user_id,  response, question_collection, users_collection):
	if question_collection.find_one({"user_id": user_id}) == None:
		#first question!
		response = list(response)
		mydict = {"user_id": user_id, "channel_id": channel, '1': response, 
		'2': [],
		'3': [],
		'4': [],
		'5': [],
		'6': [],
		'7': [], 
		'8': [],
		'9': []
		}
		question_collection.insert_one(mydict)
	else:
		myquery = { "user_id": user_id }
		questionNum = str(getQuestion(channel, users_collection))
		question_collection.update({'user_id': user_id}, {'$push': {questionNum: response}})
		

def getActionItem(channel, question_collection):
	response = question_collection.find_one({"channel_id": channel})['7']
	print(response)
	response = response[len(response)-1]
	return response
