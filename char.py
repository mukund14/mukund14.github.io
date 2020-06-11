#!/usr/bin/env python
# coding: utf-8


import newsapi
from newsapi import NewsApiClient

api_key='0ce8b6189282441e91727a812dc0f110'
newsapi = NewsApiClient(api_key=api_key)
from pandas.io.json import json_normalize
import pandas as pd
pd.set_option('display.max_colwidth', -1)
import pprint as pp
import requests
from bs4 import BeautifulSoup





import yfinance as yf
import streamlit as st
from yahoo_fin import stock_info as si
import re 
import pandas as pd
import plotly.express as px
table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df=table[0]
newdf=df[["Symbol","Security"]]
dic=newdf.set_index('Symbol')['Security'].to_dict()


import datetime
#datetime.datetime.now().date()
from datetime import datetime, timedelta
def date(base):
    date_list=[]
    yr=datetime.today().year
    if (yr%400)==0 or ((yr%100!=0) and (yr%4==0)):
        numdays=366
        date_list.append([base - timedelta(days=x) for x in range(366)])
    else:
        numdays=365
        date_list.append([base - timedelta(days=x) for x in range(365)])
    newlist=[]
    for i in date_list:
        for j in sorted(i):
            newlist.append(j)
    return newlist

def last_30(base):

    date_list=[base - timedelta(days=x) for x in range(30)]
    #newlist=[]
    #for i in sorted(date_list):
    #    newlist.append(j)
    return sorted(date_list)


def from_dt(x):
    from_dt=[]
    for i in range(len(x)):
        from_dt.append(last_30(datetime.today())[i-1].date())
        #to_dt=date(datetime.today())[i+1].date()
    return from_dt
        
def to_dt(x):
    to_dt=[]
    for i in range(len(x)):
        #from_dt=date(datetime.today())[i].date()
        to_dt.append(last_30(datetime.today())[i].date())
    return to_dt
from_list=from_dt(last_30(datetime.today()))
to_list=to_dt(last_30(datetime.today()))
import wordcloud
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


def func(query):
    newdf=pd.DataFrame()
    #query=match.groups()[0]
    for (from_dt,to_dt) in zip(from_list,to_list):
        all_articles = newsapi.get_everything(q=query,language='en',sort_by='relevancy',    from_param=from_dt,to=to_dt)
        d=json_normalize(all_articles['articles'])
        newdf=newdf.append(d)
            
    return newdf
df1=pd.DataFrame(func('indian economy'))


def text_from_urls(query):
    newd={}
    for (from_dt,to_dt) in zip(from_list,to_list):
        all_articles = newsapi.get_everything(q=query,language='en',sort_by='relevancy',    from_param=from_dt,to=to_dt)
        d=json_normalize(all_articles['articles'])
        newdf=d[["url","publishedAt","source.name","author"]]
        newdf=newdf.head(1)
        #print(newdf.head())
        dic=newdf.set_index(["source.name","publishedAt","author"])["url"].to_dict()
        #print(dic)
        for (k,v) in dic.items():
            #print(str(k[0])+str(k[1][5:10]))
            page = requests.get(v)
            html = page.content
            soup = BeautifulSoup(html, "lxml")
            text = soup.get_text()
            d2=soup.find_all("p")
            #for a in d2:
            newd[k]=re.sub(r'<.+?>',r'',str(d2)) 
    return newd
    
def wordcld(dictionary):        
    newd={}    
    for (k,v) in dictionary.items():        
        if v!='[]':            
            wordcloud = WordCloud().generate(str(dictionary[k]))                
            fig, axes= plt.subplots(figsize=(20,12),clear=True)                     
            plt.imshow(wordcloud, interpolation='bilinear')            
            plt.show()                 
        else:            
            print(str(k[0])+"_"+str(k[1][5:10])+"_"+str(k[1][11:13])              
            +"_"+str(k[1][14:16]) +"_"+str(k[1][17:19])+"_"+str(k[2]))             
            print("Wordcloud Not applicable")


import pyttsx3
engine = pyttsx3.init()
engine.getProperty('voices')
engine.setProperty('voice', '1')

engine.say("Hi")

st.write("""
# Simple Stock Price App
Shown are the stock **closing price** and ***volume*** of Google!
""")


#x = st.slider('x')  #  this is a widget

def tick():
    user_input = st.text_input("Enter stock symbol: ", 'AAPL')
    
    return user_input

tickerSymbol = str(tick())
#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)
import numpy as np
dic=func(tickerData.get_info()['longName'])
st.write(text_from_urls(tickerData.get_info()['longName']))


st.write("Current Stock Price of "+str(tickerSymbol)+" is: "+str(np.round(si.get_live_price(tickerSymbol),2)))

st.write("Here's the complete Closing Price trend: "+str(tickerSymbol))

def stock_trend_complete(tickerSymbol):
    s=tickerSymbol
    d=pd.DataFrame()
    try:
        for (k,v) in dic.items():
            if re.compile(s.lower()).match(v.lower()):
                d=d.append(yf.Ticker(k).history(period='max',interval='1d').reset_index())
            elif re.compile(s.lower()).match(k.lower()):
                d=d.append(yf.Ticker(k).history(period='max',interval='1d').reset_index())
        fig = px.line(d, x="Date", y="Close",
                      labels={'Close':'Closing Stock Price'}, 
                      template='plotly_dark',
                     color_discrete_sequence=[ "aqua"],
                      title="Closing Stock Price for the Current Year for "+str(s)
                     )
        return st.write(fig)
    except Exception as e: # work on python 3.x
        engine.say(str(e))  

stock_trend_complete(tickerSymbol)


st.write("Dividends of "+str(tickerSymbol))

st.write(st.dataframe(tickerData.dividends))
st.write("Analyst Recommendations of "+str(tickerSymbol))
st.write(tickerData.get_recommendations())
st.write("Calendar of "+str(tickerSymbol))

st.write(tickerData.calendar)

st.write("Major Holders of "+str(tickerSymbol))

st.write(tickerData.major_holders)

st.write("Actions of "+str(tickerSymbol))


st.write(tickerData.actions)



#get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')
# Open	High	Low	Close	Volume	Dividends	Stock Splits
st.write("""
## Closing Price
""")
st.line_chart(tickerDf.Close)
st.write("""
## Volume
""")
st.line_chart(tickerDf.Volume)






