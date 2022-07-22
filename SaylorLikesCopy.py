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
aantonopTweets = pd.read_csv('SaylorTweetsInfo.csv', usecols = colsList)
aantonopTweets = aantonopTweets.reset_index(drop=True)
# print(aantonopTweets)
colsListBTC = ["Date","Close"]
allTimeBitcoin = pd.read_csv('coin_Bitcoin.csv', usecols = colsListBTC)
aantonopTweets['date'] = pd.to_datetime(aantonopTweets.date)

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
aantonopTweets['date'] = aantonopTweets['date'].values.astype(str)
aantonopTweets['likes'] = aantonopTweets['likes'].values.astype(int)
aantonopTweets['date'] = aantonopTweets['date'].str[:-19]
allTimeBitcoin = allTimeBitcoin.reset_index(drop=True)
aantonopTweets = aantonopTweets.reset_index(drop=True)

sentList = sentiment(aantonopTweets)
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
aantonopTweets['sentiment'] = sentTemp
aantonopTweets['probability'] = sentProb
aantonopTweets['probability'] = aantonopTweets['probability'].values.astype(float)

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
for i in range(0,len(aantonopTweets['date'])):
    countlikes = aantonopTweets.at[i,'likes']
    if (aantonopTweets.at[i,'sentiment'] == 'POSITIVE'):
        positive +=1
    elif(aantonopTweets.at[i,'sentiment'] == 'NEGATIVE'):
        negative +=1
    else: neutral +=1
    prob = aantonopTweets.at[i,'probability']
    for n in range(i+1,len(aantonopTweets['date'])):
        if (aantonopTweets.at[i,'date'] == aantonopTweets.at[n,'date']):
            countTweets += 1
            countlikes += (aantonopTweets.at[n,'likes'])
            prob += aantonopTweets.at[n,'probability']
            if (aantonopTweets.at[n,'sentiment'] == 'POSITIVE'):
                positive +=1
            elif(aantonopTweets.at[n,'sentiment'] == 'NEGATIVE'):
                negative +=1
            else: neutral +=1
        else:
            date.append(aantonopTweets.at[i,'date'])
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
# print(aantonopTweets['sentiment'])
# print(averageProb)
# print(netSent)
# print(date)
tbd = pd.DataFrame({'date':date, 'tweets':numTweetDate, 'likes':numRTDate, 'sentiment':netSent,'probability':averageProb}) 
tbd = tbd.drop_duplicates(subset=['date'], keep='first')      
tbd = tbd.reset_index(drop=True) 
# print(tbd)

pio.renderers.default='browser'
aantonop2021BTCLine = px.line(data_frame = allTimeBitcoin, title = 'Bitcoin Value by Date vs Saylor likes', x = 'Date', y = 'Close')
for i in range(0,len(tbd['date'])):
    currentDate = tbd.at[i,'date']
    try:
        indexCurrent = allTimeBitcoin.index[allTimeBitcoin['Date']==currentDate].tolist()
        yv = allTimeBitcoin.at[indexCurrent[0],'Close']
        if (tbd.at[i,'sentiment'] == 'neutral'):
            aantonop2021BTCLine.add_annotation(x = tbd.at[i,'date'], y = yv,text = f'{tbd.at[i,"tweets"]} tweets {tbd.at[i,"likes"]} likes', showarrow = True, font=dict(family="sans serif",size=12,color="black"))
        elif (tbd.at[i,'sentiment'] == 'positive'):
            aantonop2021BTCLine.add_annotation(x = tbd.at[i,'date'], y = yv,text = f'{tbd.at[i,"tweets"]} tweets {tbd.at[i,"likes"]} likes', showarrow = True, font=dict(family="sans serif",size=12,color="green"))
            dates1 = aantonopTweets.index[aantonopTweets['date'] == currentDate].tolist()
            # print(f'\n',currentDate)
            # print(aantonopTweets.at[dates1[0],'text'])
            # print(aantonopTweets.iloc[dates1[0],13])
            # if (len(dates1) > 2):
                # print(aantonopTweets.at[dates1[1],'text'])
                # print(aantonopTweets.iloc[dates1[1],13])
                # print(aantonopTweets.at[dates1[2],'text'])
                # print(aantonopTweets.iloc[dates1[2],13])    
        elif (tbd.at[i,'sentiment'] == 'negative'):
            aantonop2021BTCLine.add_annotation(x = tbd.at[i,'date'], y = yv,text = f'{tbd.at[i,"tweets"]} tweets {tbd.at[i,"likes"]} likes', showarrow = True, font=dict(family="sans serif",size=12,color="red"))
            dates = aantonopTweets.index[aantonopTweets['date'] == currentDate].tolist()
            # print(f'\n',currentDate)
            # print(aantonopTweets.at[dates[0],'text'])
            # print(aantonopTweets.iloc[dates[0],13])
            # print(aantonopTweets.at[dates[1],'text'])
            # print(aantonopTweets.iloc[dates[1],13])
    except IndexError:
        x=0
aantonop2021BTCLine.add_annotation(text='Sentiment Analysis:<br>Red = Negative Tweet <br>Green = Positive Tweet<br>Black = Neutral Tweet', 
                    align='left',
                    font=dict(family="sans serif",size=10,color="black"),
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=1,
                    y=1,
                    bordercolor='black',
                    borderwidth=2)
Saylor2021BTCLine = aantonop2021BTCLine
# Saylor2021BTCLine.show()