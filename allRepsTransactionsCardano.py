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
cardano2021 = pd.read_csv('cardanoHistoricalData2021_2022.csv', usecols = useCols)
cardano2021['Date'] = pd.to_datetime(cardano2021.Date)
cardano2021['Price'] = cardano2021['Price'].replace(',','',regex = True)
cardano2021['Price'] = cardano2021['Price'].values.astype(float)
# print(cardano2021)
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
    if('Cardano') in temp:
        reps, investments, transaction_date, amount, typeList = appendRep(reps, investments, temp, df, i, transaction_date, amount, typeList)
    elif('ADA') in temp:
        reps, investments, transaction_date, amount, typeList = appendRep(reps, investments, temp, df, i, transaction_date, amount, typeList)
   
        
# Create dataframes
cryptoDf = pd.DataFrame({'Representative':reps, 'Date':transaction_date, 'Investment':investments, 'Type': typeList, 'Amount':amount})
# cryptoDf.to_csv('cryptoDf.csv')
adaDf = (cryptoDf[cryptoDf['Investment'].str.contains('Cardano') == True]).reset_index(drop=True)


# Graph cardano
pio.renderers.default='browser'
ada2021Graph = px.line(data_frame = cardano2021, title = 'Cardano Value by Date vs Representatives', x = 'Date', y = 'Price')
for i in range(0,len(adaDf['Date'])):
    currentDate = str(adaDf.at[i,'Date'])
    indexCurrent = cardano2021.index[cardano2021['Date']==currentDate].tolist()
    yv = cardano2021.at[indexCurrent[0],'Price']
    amountList = (adaDf.at[i,"Amount"]).split()
    amount1 = (amountList[0])
    amount2 = (amountList[2])
    amount1 = (amount1.replace('$',''))
    amount2 = (amount2.replace('$',''))
    amount1 = (amount1.replace(',',''))
    amount2 = (amount2.replace(',',''))
    amount1 = int(amount1)
    amount2 = int(amount2)
    amount = (amount1 + amount2)/2
    rep = adaDf.at[i,"Representative"]
    if (adaDf.at[i,'Type'] == 'purchase'):
        ada2021Graph.add_annotation(x = adaDf.at[i,'Date'], y = yv,text = f'{rep} bought', showarrow = True, font=dict(family="sans serif",size=12,color="green"))
        ada2021Graph.add_annotation(x = adaDf.at[i,'Date'], y = yv,text = f'${amount}', showarrow = False, yshift = 20,font=dict(family="sans serif",size=12,color="green"))
    elif (adaDf.at[i,'Type'] == 'sale_full'):
        ada2021Graph.add_annotation(x = adaDf.at[i,'Date'], y = yv,text = f'{rep} sold all', showarrow = True, font=dict(family="sans serif",size=12,color="red"))
        ada2021Graph.add_annotation(x = adaDf.at[i,'Date'], y = yv,text = f'${amount}', showarrow = False, yshift = 20,font=dict(family="sans serif",size=12,color="red"))
    else:
        ada2021Graph.add_annotation(x = adaDf.at[i,'Date'], y = yv,text = f'{rep} sold partial', showarrow = True, font=dict(family="sans serif",size=12,color="red"))
        ada2021Graph.add_annotation(x = adaDf.at[i,'Date'], y = yv,text = f'${amount}', showarrow = False, yshift = 20,font=dict(family="sans serif",size=12,color="red"))
ada2021Graph.add_annotation(text='Approximate values graphed are the following ranges($): <br>8,000.5:    1,001 - 15,000<br>32,500.5:    15,001 - 50,000<br>175,000.5:    100,001 - 250,000', 
                    align='left',
                    font=dict(family="sans serif",size=10,color="black"),
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=1,
                    y=1,
                    bordercolor='black',
                    borderwidth=2)
# ada2021Graph.show()





                
