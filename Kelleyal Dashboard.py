# Created By Alex Kelley
#import files
import dash
import dash_core_components as dcc
import dash_html_components as html
from allRepsTransactionsBtc import btc2021Graph
from allRepsTransactionsEth import eth2021Graph
from allRepsTransactionsDoge import d2021Graph
from allRepsTransactionsCardano import ada2021Graph
from ElonLikesCopy import elon2021BTCLine
from aantonopLikesCopy import aantonop2021BTCLine
from BitBoy_CryptoLikesCopy import BitBoy_Crypto2021BTCLine
from SaylorLikesCopy import Saylor2021BTCLine

# Create the Dash app
app = dash.Dash(__name__)

app.layout = html.Div(
    dcc.Tabs([
        dcc.Tab(label='Politics',
            children=[
                # Add a H1
                html.H1('House of Representatives Crypto Transactions'),
                html.H3('Created by Alex Kelley'),
                html.H3('Consulted by Dr. Arthur Bousquet'),
                # Add graphs
                dcc.Graph(id='horBtc', figure=btc2021Graph),
                dcc.Graph(id='horEth', figure=eth2021Graph),
                dcc.Graph(id='horDoge', figure = d2021Graph),
                dcc.Graph(id='horAda', figure = ada2021Graph)
                ]),
        dcc.Tab(label='Twitter Influencers', 
            children=[
                # Add a H2
                html.H1("Twitter Influencers Effect on Crypto"),
                html.H3('Created by Alex Kelley'),
                html.H3('Consulted by Dr. Arthur Bousquet'),
                # add graphs
                dcc.Graph(id='ElonLikesCopy', figure = elon2021BTCLine),
                dcc.Graph(id='SaylorLikesCopy', figure = Saylor2021BTCLine),
                dcc.Graph(id='aantonopLikesCopy', figure = aantonop2021BTCLine),
                dcc.Graph(id='Bitboy_Crypto',figure = BitBoy_Crypto2021BTCLine)
                ])
    ])    
)

# Set the app to run in development mode
if __name__ == '__main__':
    app.run_server(debug=True)