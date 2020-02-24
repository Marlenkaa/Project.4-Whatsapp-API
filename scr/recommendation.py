from mongoConnection import users, conversations
import requests
from classifier import *
import pandas as pd
from scipy.spatial.distance import pdist, squareform

def recommendUser(name):
    '''Returns a serie with descending order of similar users for specified user'''
    clf = SentimentClassifier()
    # Extracts a list of registered users in our database using our API
    users_list = requests.get('http://localhost:5000//get/info/users').json()
    total_users = []
    # Extracts all messages for each user using our API
    for user in users_list:
        user_score = {}
        messages_list = requests.get(f'http://localhost:5000//get/messages/{user}').json()
        scores = []
        # Extracts all the metrics raised from sentiment analysis for each message for each user
        for message in messages_list:
            analysis = clf.predict(message['message'])
            scores.append(analysis)
        # Get an average of sentiment results for each user and create a DataFrame
        user_score[user] = sum(scores)/len(scores)
        total_users.append(user_score)
    data = {}
    # Adapt the result to get a propertly DataFrame
    for result in total_users:
        data.update(result)
    df = pd.DataFrame(data,index=['Scores']).T
    # Compare each user with every user using euclidean metric
    matrix = pd.DataFrame(1/(1 + squareform(pdist(df, 'euclidean'))),
                         index=df.index, columns=df.index)
    similarities = matrix[name].sort_values(ascending=False)[1:]
    return similarities
