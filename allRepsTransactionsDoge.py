# Created By Alex Kelley
#import files
import urllib.request, json 
import pandas as pd
import plotly.express as px
import plotly.io as pio
from datetime import datetime, date

def removeC(x):
    x = x.replace("'","")
    x = x.replace(':','')
    x = x.replace("{",'')
    x = x.replace("[",'')
    x = x.replace("}",'')
    x = x.replace("]",'')
    x = x.replace(",",'')
    return(x)

def appendRep(reps, investments, temp, df, i, transaction_date, amount, typeList):
    reps.append(df.at[i,'representative'])
    transaction_date.append(df.at[i,'transaction_date'])
    amount.append(df.at[i,'amount'])
    typeList.append(df.at[i,'type'])
    investments.append(temp)
    return reps, investments, transaction_date, amount, typeList

#Gat data
useCols = ['Date','Price']
doge2021 = pd.read_csv('dogeHistoricalData2021_2022.csv', usecols = useCols)
doge2021['Date'] = pd.to_datetime(doge2021.Date)
doge2021['Price'] = doge2021['Price'].replace(',','',regex = True)
doge2021['Price'] = doge2021['Price'].values.astype(float)
# print(doge2021)
with urllib.request.urlopen("https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json") as url:
    data = json.loads(url.read().decode())
    df = pd.DataFrame(data)
# print(df.at[0,'asset_description'])
# for col in df.columns:
#     print(col)
# disclosure_year
# disclosure_date
# transaction_date
# owner
# ticker
# asset_description
# type
# amount
# representative
# district
# ptr_link
# cap_gains_over_200_usd

reps = []
investments = []
transaction_date = []
amount = []
typeList = []
for i in range(0,len(df['representative'])):
    temp = str(df.at[i,'asset_description'])
    if ('Doge') in temp:
        reps, investments, transaction_date, amount, typeList = appendRep(reps, investments, temp, df, i, transaction_date, amount, typeList)

        
# Create dataframes
cryptoDf = pd.DataFrame({'Representative':reps, 'Date':transaction_date, 'Investment':investments, 'Type': typeList, 'Amount':amount})
# cryptoDf.to_csv('cryptoDf.csv')
dDf = (cryptoDf[cryptoDf['Investment'].str.contains('Doge') == True]).reset_index(drop=True)

# Graph doge
pio.renderers.default='browser'
d2021Graph = px.line(data_frame = doge2021, title = 'Doge Value by Date vs Representatives', x = 'Date', y = 'Price')
for i in range(0,len(dDf['Date'])):
    currentDate = str(dDf.at[i,'Date'])
    indexCurrent = doge2021.index[doge2021['Date']==currentDate].tolist()
    yv = doge2021.at[indexCurrent[0],'Price']
    amountList = (dDf.at[i,"Amount"]).split()
    amount1 = (amountList[0])
    amount2 = (amountList[2])
    amount1 = (amount1.replace('$',''))
    amount2 = (amount2.replace('$',''))
    amount1 = (amount1.replace(',',''))
    amount2 = (amount2.replace(',',''))
    amount1 = int(amount1)
    amount2 = int(amount2)
    amount = (amount1 + amount2)/2
    rep = dDf.at[i,"Representative"]
    if (dDf.at[i,'Type'] == 'purchase'):
        d2021Graph.add_annotation(x = dDf.at[i,'Date'], y = yv,text = f'{rep} bought', showarrow = True, font=dict(family="sans serif",size=12,color="green"))
        d2021Graph.add_annotation(x = dDf.at[i,'Date'], y = yv,text = f'${amount}', showarrow = False, yshift = 20,font=dict(family="sans serif",size=12,color="green"))
    elif (dDf.at[i,'Type'] == 'sale_full'):
        d2021Graph.add_annotation(x = dDf.at[i,'Date'], y = yv,text = f'{rep} sold all', showarrow = True, font=dict(family="sans serif",size=12,color="red"))
        d2021Graph.add_annotation(x = dDf.at[i,'Date'], y = yv,text = f'${amount}', showarrow = False, yshift = 20,font=dict(family="sans serif",size=12,color="red"))
    else:
        d2021Graph.add_annotation(x = dDf.at[i,'Date'], y = yv,text = f'{rep} sold partial', showarrow = True, font=dict(family="sans serif",size=12,color="red"))
        d2021Graph.add_annotation(x = dDf.at[i,'Date'], y = yv,text = f'${amount}', showarrow = False, yshift = 20,font=dict(family="sans serif",size=12,color="red"))
d2021Graph.add_annotation(text='Approximate values graphed are the following ranges($): <br>8,000.5:    1,001 - 15,000<br>32,500.5:    15,001 - 50,000<br>175,000.5:    100,001 - 250,000', 
                    align='left',
                    font=dict(family="sans serif",size=10,color="black"),
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=1,
                    y=1,
                    bordercolor='black',
                    borderwidth=2)
# d2021Graph.show()





                
