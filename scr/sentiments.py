from nltk.sentiment.vader import SentimentIntensityAnalyzer
from bson.json_util import dumps
from classifier import *

'''Trying two different methods to analyze the sentiment of a conversations. 

The first one is with nltk.sentiment.vader, wich provides more information about the analysis, 
but it works poorly with spanish language. I've tried to translate the conversations first with TextBlob
and Google's API, but the translation doesn't work propertly as there are expressions and different 
ways to write in spanish.

The second method is with simple-senti-py, which is specifically made to analyze in spanish. It only
provides one measure'''

class Sent:
    def sentimentAnalysis(self,mI,chat):
        '''Returns an analysis of sentiments for specified chat'''
        sid = SentimentIntensityAnalyzer()
        sentiments = []
        self.messages = []
        # Analyze each sentence from chat
        for i in range(len(mI)):
            message = mI[i]['message']
            self.messages.append(message)
            analysis = sid.polarity_scores(str(message))
            sentiments.append(analysis)
        # Exclude missing data and calculate an average of each sentiment
        neg = [x['neg'] for x in sentiments if x['neg']+x['neu']+x['pos']+x['compound'] != 0.0]
        neu = [x['neu'] for x in sentiments if x['neg']+x['neu']+x['pos']+x['compound'] != 0.0]
        pos = [x['pos'] for x in sentiments if x['neg']+x['neu']+x['pos']+x['compound'] != 0.0]
        compound = [x['compound'] for x in sentiments if x['neg']+x['neu']+x['pos']+x['compound'] != 0.0]
        # Established an 0.05 value by convention to compare results
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
    def sentimentAnalysisSpanish(self):
        '''Returns an analysis of sentiments for specified spanish chat'''
        clf = SentimentClassifier()
        sentiments = []
        # Re-use messages from specified chat to make other sentiment analysis
        for message in self.messages:
            analysis = clf.predict(message)
            sentiments.append(analysis)
        average = sum(sentiments)/len(sentiments)
        # Values from 0 to 1, asignated as personal standard
        if average <= 0.3:
            return 'Chat Overall Rated As NEGATIVE'
        elif average >= 0.7:
            return 'Chat Overall Rated As POSITIVE'
        else:
            return 'Chat Overall Rated As NEUTRAL'

s = Sent()