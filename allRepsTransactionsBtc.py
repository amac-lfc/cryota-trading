# Created By Alex Kelley
#import files
import dash
import dash_core_components as dcc
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
bitcoin2021 = pd.read_csv('BitcoinHistoricalData2021_2022.csv', usecols = useCols)
bitcoin2021['Date'] = pd.to_datetime(bitcoin2021.Date)
bitcoin2021['Price'] = bitcoin2021['Price'].replace(',','',regex = True)
bitcoin2021['Price'] = bitcoin2021['Price'].values.astype(float)
# print(bitcoin2021)
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
    if ('Bitcoin') in temp:
        reps, investments, transaction_date, amount, typeList = appendRep(reps, investments, temp, df, i, transaction_date, amount, typeList)
    elif('BTC') in temp:
        reps, investments, transaction_date, amount, typeList = appendRep(reps, investments, temp, df, i, transaction_date, amount, typeList)
    elif('Ethereum') in temp:
        reps, investments, transaction_date, amount, typeList = appendRep(reps, investments, temp, df, i, transaction_date, amount, typeList)
    elif('ETH') in temp:
        reps, investments, transaction_date, amount, typeList = appendRep(reps, investments, temp, df, i, transaction_date, amount, typeList)
    elif('Doge') in temp:
        reps, investments, transaction_date, amount, typeList = appendRep(reps, investments, temp, df, i, transaction_date, amount, typeList)
    elif('Cardano') in temp:
        reps, investments, transaction_date, amount, typeList = appendRep(reps, investments, temp, df, i, transaction_date, amount, typeList)
    elif('ADA') in temp:
        reps, investments, transaction_date, amount, typeList = appendRep(reps, investments, temp, df, i, transaction_date, amount, typeList)
    elif('Polkadot') in temp:
        reps, investments, transaction_date, amount, typeList = appendRep(reps, investments, temp, df, i, transaction_date, amount, typeList)
    elif('DOT') in temp:
        reps, investments, transaction_date, amount, typeList = appendRep(reps, investments, temp, df, i, transaction_date, amount, typeList)
        
# Create dataframes
cryptoDf = pd.DataFrame({'Representative':reps, 'Date':transaction_date, 'Investment':investments, 'Type': typeList, 'Amount':amount})
# cryptoDf.to_csv('cryptoDf.csv')
btcDf = (cryptoDf[cryptoDf['Investment'].str.contains('Bitcoin') == True]).reset_index(drop=True)
ethDf = cryptoDf[cryptoDf['Investment'].str.contains('Eth') == True]
ethDf = (ethDf.append(cryptoDf[cryptoDf['Investment'].str.contains('ETH') == True], ignore_index = True)).reset_index(drop=True)
adaDf = (cryptoDf[cryptoDf['Investment'].str.contains('Cardano') == True]).reset_index(drop=True)
dogeDf = (cryptoDf[cryptoDf['Investment'].str.contains('Doge') == True]).reset_index(drop=True)

# Graph Bitcoin
pio.renderers.default='browser'
btc2021Graph = px.line(data_frame = bitcoin2021, title = 'Bitcoin Value by Date vs Representatives', x = 'Date', y = 'Price')
for i in range(0,len(btcDf['Date'])):
    currentDate = str(btcDf.at[i,'Date'])
    indexCurrent = bitcoin2021.index[bitcoin2021['Date']==currentDate].tolist()
    yv = bitcoin2021.at[indexCurrent[0],'Price']
    amountList = (btcDf.at[i,"Amount"]).split()
    amount1 = (amountList[0])
    amount2 = (amountList[2])
    amount1 = (amount1.replace('$',''))
    amount2 = (amount2.replace('$',''))
    amount1 = (amount1.replace(',',''))
    amount2 = (amount2.replace(',',''))
    amount1 = int(amount1)
    amount2 = int(amount2)
    amount = (amount1 + amount2)/2
    rep = btcDf.at[i,"Representative"]
    if (btcDf.at[i,'Type'] == 'purchase'):
        btc2021Graph.add_annotation(x = btcDf.at[i,'Date'], y = yv,text = f'{rep} bought', showarrow = True, font=dict(family="sans serif",size=12,color="green"))
        btc2021Graph.add_annotation(x = btcDf.at[i,'Date'], y = yv,text = f'${amount}', showarrow = False, yshift = 20,font=dict(family="sans serif",size=12,color="green"))
    elif (btcDf.at[i,'Type'] == 'sale_full'):
        btc2021Graph.add_annotation(x = btcDf.at[i,'Date'], y = yv,text = f'{rep} sold all', showarrow = True, font=dict(family="sans serif",size=12,color="red"))
        btc2021Graph.add_annotation(x = btcDf.at[i,'Date'], y = yv,text = f'${amount}', showarrow = False, yshift = 20,font=dict(family="sans serif",size=12,color="red"))
    else:
        btc2021Graph.add_annotation(x = btcDf.at[i,'Date'], y = yv,text = f'{rep} sold partial', showarrow = True, font=dict(family="sans serif",size=12,color="red"))
        btc2021Graph.add_annotation(x = btcDf.at[i,'Date'], y = yv,text = f'${amount}', showarrow = False, yshift = 20,font=dict(family="sans serif",size=12,color="red"))
btc2021Graph.add_annotation(text='Approximate values graphed are the following ranges($): <br>8,000.5:    1,001 - 15,000<br>32,500.5:    15,001 - 50,000<br>175,000.5:    100,001 - 250,000', 
                    align='left',
                    font=dict(family="sans serif",size=10,color="black"),
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=1,
                    y=1,
                    bordercolor='black',
                    borderwidth=2)
# btc2021Graph.show()
# Set up the layout with a single graph

# app = dash.Dash(__name__)

# app.layout = [dcc.Graph(
#   id='BTCReps',
#   # Insert the line graph
#   figure=btc2021Graph),

# if __name__ == '__main__':
#     app.run_server(debug=True)




                
