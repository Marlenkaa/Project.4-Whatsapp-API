from flask import Flask, request
from dataCleaning import df, cleaning
import users as user
import chats as chat
import conversations as conversation
import sentiments
import recommendation
import pandas as pd
from bson.json_util import dumps
import json
from mongoConnection import conversations, users, chats

app = Flask(__name__)

@app.route('/createdatabase')
def createDatabase():
    '''Cleans dataset and creates the whole database with users, chats and conversations'''
    data = cleaning(df)
    user.createUsers(data)
    chat.createChats(data)
    conversation.createConversations(data)
    print('Database created')
    return 'Database created'

@app.route('/insert/user/<name>')
def createUser(name):
    user.insertUser(name)
    return f'User "{name}" has been inserted into users collection'

@app.route('/insert/chat/<name>')
def createChat(name):
    chat.insertChat(name)
    return 'Chat has been inserted into chats collection'

@app.route('/insert/user/to/chat/<chat>/<name>')
def insertUser(chat,name):
    user.insertUsertoChat(chat,name)
    return f'User "{name}" has been inserted into chat "{chat}" in chats collection'

@app.route('/insert/message/<chat>/<name>/<datetime>/<message>')
def insertMessage(chat,name,datetime,message):
    conversation.insertMessagetoChat(chat,name,datetime,message)
    return f'User "{name}" has been inserted into chat "{chat}" in chats collection'

@app.route('/get/info/users')
def usersInfo():
    '''Returns a list of users'''
    return dumps(users.distinct('user_name'))

@app.route('/get/info/chats')
def chatsInfo():
    '''Returns a list of chats'''
    return dumps(chats.distinct('chat_date'))

@app.route('/get/info/<chat>')
def messagesInfo(chat):
    '''Returns a list of messages stored in specified chat'''
    # Extracts id's chat to get the conversations/messages from it
    chatid = list(chats.find({'chat_date':chat}, {'chat_id': 1,'_id':0}))[0]['chat_id']
    data = list(conversations.find({'chat_id':chatid},{'_id':0}))
    messages = []
    for m in data:
        info = {}
        info['user_id'] = m['user_id']
        info['conversation_id'] = m['conversation_id']
        info['datetime'] = m['datetime']
        info['message'] = m['message']
        messages.append(info)
    return dumps(messages)

@app.route('/get/messages/<name>')
def messagesUser(name):
    '''Returns all messages wrote by specified user'''
    # Extracts id's user to get the messages
    userid = list(users.find({'user_name':name},{'user_id': 1,'_id':0}))[0]['user_id']
    messages = list(conversations.find({'user_id':userid},{'message':1,'_id':0}))
    return dumps(messages)

@app.route('/get/sentiments/from/<chat>')
def chatSentiment(chat):
    '''Returns an analysis of sentiments for specified chat'''
    # Extracts the messages from chat
    mI = messagesInfo(chat)
    # Converts to json
    mI = json.loads(mI)
    results = sentiments.s.sentimentAnalysis(mI,chat)
    return results

@app.route('/get/sentiments/from/spanish/<chat>')
def spanishChatSentiment(chat):
    '''Returns an analysis of sentiments for specified spanish chat'''
    # Extracts the messages from chat
    mI = messagesInfo(chat)
    # Converts to json
    mI = json.loads(mI)
    sentiments.s.sentimentAnalysis(mI,chat)
    results = sentiments.s.sentimentAnalysisSpanish()
    return results

@app.route('/recommend/user/<name>')
def userRecommendation(name):
    '''Given an user, returns similar users in descending order from the most similar one'''
    result = recommendation.recommendUser(name)
    return result

app.run('0.0.0.0',5000,debug=True)