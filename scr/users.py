from mongoConnection import users, chats
from errorHandler import jsonErrorHandler
import pandas as pd

@jsonErrorHandler
def createUsers(data):
    '''Creates users in our database in MongoDB from the dataset cleaned'''
    # Extract users from dataset
    users_list = list(data['users'].value_counts().keys())
    # Insert users in our users collection
    for user in users_list:
        # Id generator
        if len(users.distinct('user_id')) == 0:
            users_id = 0
        else:
            users_id = len(users.distinct('user_id'))
        # Inserts into collection
        users.insert_one({
            'user_id': users_id,
            'user_name': user
            })
    print('Users names have been created in users collection')
    return 'Users names have been created in users collection'

@jsonErrorHandler
def insertUser(name):
    '''Inserts an user into users collection'''
    # Checks if introduced name already exists
    names = (users.distinct('user_name'))
    if name in names:
        print('Name already exists')
        return 'Name already exists'
    else:
        # Id generator
        if len(users.distinct('user_id')) == 0:
            users_id = 0
        else:
            users_id = len(users.distinct('user_id'))
        # Inserts into collection
        users.insert_one({
            'user_id': users_id,
            'user_name': name
            })
        print(f'User "{name}" has been inserted into users collection')
        return f'User "{name}" has been inserted into users collection'

@jsonErrorHandler
def insertUsertoChat(chat,name):
    '''Inserts an user into created chat'''
    # Cheks if introduced user already exists in indicated chat
    chats_list = list(chats.find({'user_name':name}, {'chat_date': 1,'_id':0}))
    user_chats = []
    for i in chats_list:
        user_chats.append(i['chat_date'])
    if chat in user_chats:
        print('User already exists in specified chat')
        return 'User already exists in specified chat'
    else:
        # Finds users and chats ids
        chatid = list(chats.find({'chat_date':chat}, {'chat_id': 1,'_id':0}))[0]['chat_id']
        userid = list(users.find({'user_name':name}, {'user_id': 1,'_id':0}))[0]['user_id']
        # Inserts into collection
        chats.insert_one({
            'chat_id': chatid,
            'chat_date': chat,
            'user_id': userid,
            })
        print(f'User "{name}" has been inserted into chat "{chat}" in chats collection')
        return f'User "{name}" has been inserted into chat "{chat}" in chats collection'
