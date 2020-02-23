def sentimentAnalysis(mI,chat):
    '''Returns an analysis of sentiments for specified chat'''
    sid = SentimentIntensityAnalyzer()
    sentiments = []
    # Analyze each sentence from chat
    for i in range(len(mI)):
        message = mI[i]['message']
        analysis = sid.polarity_scores(message)
        sentiments.append(analysis)
    # Exclude missing data and calculate an average of each sentiment
    neg = [x['neg'] for x in sentiments if x['neg']+x['neu']+x['pos']+x['compound'] != 0.0]
    neu = [x['neu'] for x in sentiments if x['neg']+x['neu']+x['pos']+x['compound'] != 0.0]
    pos = [x['pos'] for x in sentiments if x['neg']+x['neu']+x['pos']+x['compound'] != 0.0]
    compound = [x['compound'] for x in sentiments if x['neg']+x['neu']+x['pos']+x['compound'] != 0.0]
    averages = f'''Chat on date {chat} was rated as: 
                                        {round((sum(pos)/len(pos))*100,2)}% Positive, 
                                        {round((sum(neg)/len(neg))*100,2)}% Negative, 
                                        {round((sum(neu)/len(neu))*100,2)}% Neutral'''
    if sum(compound)/len(compound) >= 0.05: 
        return print(averages, '\nChat Overall Rated As POSITIVE')
    elif sum(compound)/len(compound) <= - 0.05: 
        return print(averages, '\nChat Overall Rated As NEGATIVE')
    else: 
        return print(averages, '\nChat Overall Rated As NEUTRAL')