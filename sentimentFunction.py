# Created by Alex Kelley 
#import modules
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
from transformers import pipeline

# # NLTK set up
# # nltk.download('stopwords')
# # nltk.download('punkt')
# # nltk.download('wordnet')
# # nltk.download('omw-1.4')
# stopwords = nltk.corpus.stopwords.words("english")
# regexp = RegexpTokenizer('\w+')
# wordnet_lem = WordNetLemmatizer()
# analyzer = SentimentIntensityAnalyzer()
def sentiment(df):
    # df['text_token']=df['text'].apply(regexp.tokenize)
    # df['text_token'] = df['text_token'].apply(lambda x: [item for item in x if item not in stopwords])
    # df['text_string'] = df['text_token'].apply(lambda x: ' '.join([item for item in x if len(item)>2]))
    # all_words = ' '.join([word for word in df['text_string']])
    # tokenized_words = nltk.tokenize.word_tokenize(all_words)
    # fdist = FreqDist(tokenized_words)
    # df['text_string_fdist'] = df['text_token'].apply(lambda x: ' '.join([item for item in x if fdist[item] >= 1 ]))
    # df['text_string_lem'] = df['text_string_fdist'].apply(wordnet_lem.lemmatize)
    # df['is_equal']= (df['text_string_fdist']==df['text_string_lem'])
    # df['polarity'] = df['text_string_lem'].apply(lambda x: analyzer.polarity_scores(x))
    # df = pd.concat([df.drop(['polarity'], axis=1), df['polarity'].apply(pd.Series)], axis=1)
    # df['sentiment'] = df['compound'].apply(lambda x: 'positive' if x >0 else 'neutral' if x==0 else 'negative')
    sentiment_pipeline = pipeline("sentiment-analysis")
    data = []
    sentScore = []
    for i in range(0,len(df)):
        data.append(df.at[i,'text'])
        # print(df.at[i,'text'])
        sentScore.append(sentiment_pipeline(data[i]))
    return(sentScore)

