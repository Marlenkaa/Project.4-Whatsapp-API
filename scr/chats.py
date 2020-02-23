from mongoConnection import chats, users
from errorHandler import jsonErrorHandler
import pandas as pd
from datetime import datetime

@jsonErrorHandler
def createChats(data):
    '''Creates chats in our database in MongoDB from the dataset cleaned'''
    # Extracts dates from dataset, as each date conversation will be a single chat
    dates = list(data['date'].value_counts().keys())
    for date in dates:
        # Extracts users that participated in each chat conversation (each date)
        filtered_df = data[data['date'] == date]
        users_list = list(filtered_df['users'].value_counts().keys())
        # Id generator
        if len(chats.distinct('chat_id')) == 0:
            chat_id = 0
        else:
            chat_id = len(chats.distinct('chat_id'))
        chat = []
        for user in users_list:
            participants = {}
            # Finds id of every user
            user_info = (users.find({'user_name':user},{'user_id':1}))
            # Includes all the info into each chat
            participants['chat_id'] = chat_id
            participants['chat_date'] = date
            participants['user_id'] = user_info[0]['user_id']
            chat.append(participants)
        # Inserts into collection
        chats.insert_many(chat)
    print('Chats have been created in chats collection')
    return 'Chats have been created in chats collection'

@jsonErrorHandler
def insertChat(name):
    '''Inserts a chat into chats collection'''
    today = datetime.today().strftime('%d-%m-%Y')
    # Id generator
    if len(chats.distinct('chat_id')) == 0:
        chat_id = 0
    else:
        chat_id = len(chats.distinct('chat_id'))
    # Finds id of indicated user
    user_info = (users.find({'user_name':name},{'user_id':1}))
    # Inserts info into collection
    chats.insert_one({
            'chat_id': chat_id,
            'chat_date': today,
            'user_id': user_info[0]['user_id'],
            })
    print(f'Chat with date "{today}" has been inserted into chats collection')
    return f'Chat with date "{today}" has been inserted into chats collection'