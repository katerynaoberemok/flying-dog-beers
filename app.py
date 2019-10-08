import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import matplotlib
import datetime as dt
import os
import time
import base64
import json
import psycopg2
import pandas.io.sql as sqlio

from dash.dependencies import Output
from dash.dependencies import Input



# dependencies
dbname='videodetect_db01'
user='videodetect01'
password='VideoDetect01!'
host='172.31.38.224'
# port=8050
good_photos_folder_name = 'photos_good'
schedule_json_name = 'schedule.json'

with open(schedule_json_name, 'r') as f:
    schedule_dict = json.load(f)

schedule_dict = {pers: dt.datetime.strptime(x, '%H:%M').time() for pers,x in schedule_dict.items()}

def get_week_label(series):
    
    start_day = series.min().day
    end_date = series.min() + dt.timedelta(days=6)
    end_day = end_date.day
    month = end_date.month
    year = end_date.year

    return '{}-{}.{}.{}'.format(start_day, end_day, month, year)

# connect to DB and read a DataFrame from DB
conn = psycopg2.connect(dbname=dbname, 
						user=user, 
                        password=password, 
                        host=host)
cursor = conn.cursor()

sql = "select * from users_aggregate;"
df = sqlio.read_sql_query(sql, conn)
conn = None



########### Define your variables
beers=['Chesapeake Stout', 'Snake Dog IPA', 'Imperial Porter', 'Double Dog IPA']
ibu_values=[35, 60, 85, 75]
abv_values=[5.4, 7.1, 9.2, 4.3]
color1='lightblue'
color2='darkgreen'
mytitle='Beer Comparison'
tabtitle='beer!'
myheading='Flying Dog Beers'
label1='IBU'
label2='ABV'
githublink='https://github.com/austinlasseter/flying-dog-beers'
sourceurl='https://www.flyingdog.com/beers/'

########### Set up the chart
bitterness = go.Bar(
    x=beers,
    y=ibu_values,
    name=label1,
    marker={'color':color1}
)
alcohol = go.Bar(
    x=beers,
    y=abv_values,
    name=label2,
    marker={'color':color2}
)

beer_data = [bitterness, alcohol]
beer_layout = go.Layout(
    barmode='group',
    title = mytitle
)

beer_fig = go.Figure(data=beer_data, layout=beer_layout)


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout
app.layout = html.Div(children=[
    html.H1(myheading),
    dcc.Graph(
        id='flyingdog',
        figure=beer_fig
    ),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A('Data Source', href=sourceurl),
    ]
)

if __name__ == '__main__':
    app.run_server()
