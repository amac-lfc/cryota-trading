# Created By Alex Kelley
#import modules
import pandas as pd
import tweepy
from datetime import datetime
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from sentimentFunction import sentiment


colsList = ['Id:', 'text','date','retweets','likes']
elonTweets1 = pd.read_csv('moreElonTweetsInfo.csv', usecols = colsList)
elonTweets2 = pd.read_csv('moreElonMusk2Info.csv', usecols = colsList)
elonTweets = pd.concat([elonTweets1, elonTweets2], ignore_index=True)
elonTweets = elonTweets.reset_index(drop=True)
# print(elonTweets)
colsListBTC = ["Date","Close"]
allTimeBitcoin = pd.read_csv('coin_Bitcoin.csv', usecols = colsListBTC)
elonTweets['date'] = pd.to_datetime(elonTweets.date)

for i in range(13,20):
    allTimeBitcoin = allTimeBitcoin[allTimeBitcoin['Date'].str.contains(f'20{i}-') == False]
allTimeBitcoin = allTimeBitcoin[allTimeBitcoin['Date'].str.contains('2020-') == False]
for i in range(1,3):
    allTimeBitcoin = allTimeBitcoin[allTimeBitcoin['Date'].str.contains(f'2021-0{i}') == False]
    j = i + 6
    if(j<10):
        allTimeBitcoin = allTimeBitcoin[allTimeBitcoin['Date'].str.contains(f'2021-0{j}') == False]
allTimeBitcoin = allTimeBitcoin[allTimeBitcoin['Date'].str.contains('2021-07-') == False]

allTimeBitcoin['Date'] = allTimeBitcoin['Date'].str[:-9]
allTimeBitcoin['Date'] = (allTimeBitcoin['Date']).values.astype(str)
elonTweets['date'] = elonTweets['date'].values.astype(str)
elonTweets['likes'] = elonTweets['likes'].values.astype(int)
elonTweets['date'] = elonTweets['date'].str[:-19]
allTimeBitcoin = allTimeBitcoin.reset_index(drop=True)
elonTweets = elonTweets.reset_index(drop=True)

sentList = sentiment(elonTweets)
# print(sentList)
x = str(sentList)
x = x.replace("'","")
x = x.replace(':','')
x = x.replace("{",'')
x = x.replace("[",'')
x = x.replace("}",'')
x = x.replace("]",'')
x = x.replace(",",'')
y = x.split()
sentTemp = []
sentProb = []
for i in  range(1,len(y),4):
    j = i + 2
    sentTemp.append(y[i])
    sentProb.append(y[j])
# print(sentTemp)
# print(sentProb)
elonTweets['sentiment'] = sentTemp
elonTweets['probability'] = sentProb
elonTweets['probability'] = elonTweets['probability'].values.astype(float)

#Find number of tweets per day and total likes
date = []
numTweetDate = []
numRTDate = []
countTweets = 1
netSent = []
averageProb = []
positive = 0
negative = 0
neutral = 0
for i in range(0,len(elonTweets['date'])):
    countlikes = elonTweets.at[i,'likes']
    if (elonTweets.at[i,'sentiment'] == 'POSITIVE'):
        positive +=1
    elif(elonTweets.at[i,'sentiment'] == 'NEGATIVE'):
        negative +=1
    else: neutral +=1
    prob = elonTweets.at[i,'probability']
    for n in range(i+1,len(elonTweets['date'])):
        if (elonTweets.at[i,'date'] == elonTweets.at[n,'date']):
            countTweets += 1
            countlikes += (elonTweets.at[n,'likes'])
            prob += elonTweets.at[n,'probability']
            if (elonTweets.at[n,'sentiment'] == 'POSITIVE'):
                positive +=1
            elif(elonTweets.at[n,'sentiment'] == 'NEGATIVE'):
                negative +=1
            else: neutral +=1
        else:
            date.append(elonTweets.at[i,'date'])
            numTweetDate.append(countTweets)
            numRTDate.append(countlikes)
            if(positive > negative):
                netSent.append('positive')
            elif(negative > positive):
                netSent.append('negative')
            else: netSent.append('neutral')
            aProb = prob / countTweets
            averageProb.append(aProb)
            prob = 0
            countTweets = 1
            positive = 0
            negative = 0
            neutral = 0
            break
# print(elonTweets['sentiment'])
# print(averageProb)
# print(netSent)
# print(date)
tbd = pd.DataFrame({'date':date, 'tweets':numTweetDate, 'likes':numRTDate, 'sentiment':netSent,'probability':averageProb}) 
tbd = tbd.drop_duplicates(subset=['date'], keep='first')      
tbd = tbd.reset_index(drop=True) 
# print(tbd)

pio.renderers.default='browser'
elon2021BTCLine = px.line(data_frame = allTimeBitcoin, title = 'Bitcoin Value by Date vs Elon Musk likes', x = 'Date', y = 'Close')
for i in range(0,len(tbd['date'])):
    currentDate = tbd.at[i,'date']
    try:
        indexCurrent = allTimeBitcoin.index[allTimeBitcoin['Date']==currentDate].tolist()
        yv = allTimeBitcoin.at[indexCurrent[0],'Close']
        if (tbd.at[i,'sentiment'] == 'neutral'):
            elon2021BTCLine.add_annotation(x = tbd.at[i,'date'], y = yv,text = f'{tbd.at[i,"tweets"]} tweets {tbd.at[i,"likes"]} likes', showarrow = True, font=dict(family="sans serif",size=12,color="black"))
        elif (tbd.at[i,'sentiment'] == 'positive'):
            elon2021BTCLine.add_annotation(x = tbd.at[i,'date'], y = yv,text = f'{tbd.at[i,"tweets"]} tweets {tbd.at[i,"likes"]} likes', showarrow = True, font=dict(family="sans serif",size=12,color="green"))
            dates1 = elonTweets.index[elonTweets['date'] == currentDate].tolist()
            # print(f'\n',currentDate)
            # print(elonTweets.at[dates1[0],'text'])
            # print(elonTweets.iloc[dates1[0],13])
            # if (len(dates1) > 2):
                # print(elonTweets.at[dates1[1],'text'])
                # print(elonTweets.iloc[dates1[1],13])
                # print(elonTweets.at[dates1[2],'text'])
                # print(elonTweets.iloc[dates1[2],13])    
        elif (tbd.at[i,'sentiment'] == 'negative'):
            elon2021BTCLine.add_annotation(x = tbd.at[i,'date'], y = yv,text = f'{tbd.at[i,"tweets"]} tweets {tbd.at[i,"likes"]} likes', showarrow = True, font=dict(family="sans serif",size=12,color="red"))
            dates = elonTweets.index[elonTweets['date'] == currentDate].tolist()
            # print(f'\n',currentDate)
            # print(elonTweets.at[dates[0],'text'])
            # print(elonTweets.iloc[dates[0],13])
            # print(elonTweets.at[dates[1],'text'])
            # print(elonTweets.iloc[dates[1],13])
    except IndexError:
        x=0
elon2021BTCLine.add_annotation(text='Sentiment Analysis:<br>Red = Negative Tweet <br>Green = Positive Tweet<br>Black = Neutral Tweet', 
                    align='left',
                    font=dict(family="sans serif",size=10,color="black"),
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=1,
                    y=1,
                    bordercolor='black',
                    borderwidth=2)
   
# elon2021BTCLine.show()