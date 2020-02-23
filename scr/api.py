from flask import Flask, request
from dataCleaning import df, cleaning
import users
import chats
import conversations
import pandas as pd

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

@app.route('/insertuser/<name>')
def createUser(name):
    users.insertUser(name)
    return f'User "{name}" has been inserted into users collection'

@app.route('/insertchat/<name>')
def createChat(name):
    chats.insertChat(name)
    return 'Chat has been inserted into chats collection'

@app.route('/insertusertochat/<chat>/<name>')
def insertUser(chat,name):
    users.insertUsertoChat(chat,name)
    return f'User "{name}" has been inserted into chat "{chat}" in chats collection'

@app.route('/insertmessage/<chat>/<name>/<datetime>/<message>')
def insertMessage(chat,name,datetime,message):
    conversations.insertMessagetoChat(chat,name,datetime,message)
    return f'User "{name}" has been inserted into chat "{chat}" in chats collection'


app.run('0.0.0.0',5000,debug=True)