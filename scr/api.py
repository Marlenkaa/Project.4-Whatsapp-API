from flask import Flask, request
from dataCleaning import df, cleaning
import users
import chats
import conversations
import sentiments
import pandas as pd
from bson.json_util import dumps
import json
from mongoConnection import conversations, users, chats

app = Flask(__name__)

@app.route('/createdatabase')
def createDatabase():
    '''Cleans dataset and creates the whole database with users, chats and conversations'''
    data = cleaning(df)
    users.createUsers(data)
    chats.createChats(data)
    conversations.createConversations(data)
    print('Database created')
    return 'Database created'

@app.route('/insert/user/<name>')
def createUser(name):
    users.insertUser(name)
    return f'User "{name}" has been inserted into users collection'

@app.route('/insert/chat/<name>')
def createChat(name):
    chats.insertChat(name)
    return 'Chat has been inserted into chats collection'

@app.route('/insert/user/to/chat/<chat>/<name>')
def insertUser(chat,name):
    users.insertUsertoChat(chat,name)
    return f'User "{name}" has been inserted into chat "{chat}" in chats collection'

@app.route('/insert/message/<chat>/<name>/<datetime>/<message>')
def insertMessage(chat,name,datetime,message):
    conversations.insertMessagetoChat(chat,name,datetime,message)
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

@app.route('/get/sentiments/from/<chat>')
def chatSentiment(chat):
    '''Returns an analysis of sentiments for specified chat'''
    # Extracts the messages from chat
    mI = messagesInfo(chat)
    # Converts to json
    mI = json.loads(mI)
    results = sentiments.sentimentAnalysis(mI,chat)
    return results

app.run('0.0.0.0',5000,debug=True)