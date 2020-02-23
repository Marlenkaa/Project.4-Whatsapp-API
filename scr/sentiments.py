from nltk.sentiment.vader import SentimentIntensityAnalyzer
from bson.json_util import dumps
from textblob import TextBlob

def sentimentAnalysis(mI,chat):
    '''Returns an analysis of sentiments for specified chat'''
    sid = SentimentIntensityAnalyzer()
    sentiments = []
    # Translate to english and analyze each sentence from chat
    for i in range(len(mI)):
        message = mI[i]['message']
        analysis = sid.polarity_scores(str(message))
        sentiments.append(analysis)
    # Exclude missing data and calculate an average of each sentiment
    neg = [x['neg'] for x in sentiments if x['neg']+x['neu']+x['pos']+x['compound'] != 0.0]
    neu = [x['neu'] for x in sentiments if x['neg']+x['neu']+x['pos']+x['compound'] != 0.0]
    pos = [x['pos'] for x in sentiments if x['neg']+x['neu']+x['pos']+x['compound'] != 0.0]
    compound = [x['compound'] for x in sentiments if x['neg']+x['neu']+x['pos']+x['compound'] != 0.0]
    if sum(compound)/len(compound) >= 0.05: 
        overall = 'POSITIVE'
    elif sum(compound)/len(compound) <= -0.05: 
        overall = 'NEGATIVE'
    else: 
        overall = 'NEUTRAL'
    return dumps({'Positivity': f'{round((sum(pos)/len(pos))*100,2)}%',
                  'Negativity': f'{round((sum(neg)/len(neg))*100,2)}%',
                  'Neutrality': f'{round((sum(neu)/len(neu))*100,2)}%',
                  'Overall': overall
                  })
    

