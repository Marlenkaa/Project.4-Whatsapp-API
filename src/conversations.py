from mongoConnection import conversations, users, chats
from errorHandler import jsonErrorHandler
import pandas as pd

@jsonErrorHandler
def createConversations(data):
    '''Creates conversations/messages in our database in MongoDB from the dataset cleaned'''
    # Extracts all the info necessary to feed conversations collection
    for index in range(len(data)):
        row = data.iloc[[index]]
        user = list(row['users'])
        date = list(row['date'])
        hour = list(row['hour'])
        message = list(row['messages'])
        # Id generator
        if len(conversations.distinct('conversation_id')) == 0:
            conversation_id = 0
        else:
            conversation_id = len(conversations.distinct('conversation_id'))
        # Finds users and chats ids
        userid = list(users.find({'user_name':user[0]}, {'user_id': 1,'_id':0}))[0]['user_id']
        chatid = list(chats.find({'chat_date':date[0]}, {'chat_id': 1,'_id':0}))[0]['chat_id']
        # Inserts into collection
        conversations.insert_one({
            'conversation_id': conversation_id,
            'datetime': date[0] + ' ' + hour[0],
            'message': message[0],
            'user_id': userid,
            'chat_id': chatid
            })
    print('Conversations have been created in conversation collection')
    return 'Conversations have been created in conversation collection'

@jsonErrorHandler
def insertMessagetoChat(chat,name,datetime,message):
    '''Inserts a message into conversations collection'''
    # Id generator
    if len(conversations.distinct('conversation_id')) == 0:
        conversation_id = 0
    else:
        conversation_id = len(conversations.distinct('conversation_id'))
    # Finds users and chats ids
    userid = list(users.find({'user_name':name}, {'user_id': 1,'_id':0}))[0]['user_id']
    chatid = list(chats.find({'chat_date':chat}, {'chat_id': 1,'_id':0}))[0]['chat_id']
    # Inserts into collection
    conversations.insert_one({
        'conversation_id': conversation_id,
        'datetime': datetime,
        'message': message,
        'user_id': userid,
        'chat_id': chatid
        })
    print(f'Message "{message}" has been inserted into conversations collection')
    return f'Message "{message}" has been inserted into conversations collection'
