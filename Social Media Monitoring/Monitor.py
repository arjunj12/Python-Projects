import tkinter as tk

from bs4 import BeautifulSoup
import requests
import lxml


import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#colors
bgColor='#8854d0'
buttonColor = '#58e4d9'
labelColor = '#ff2727'
fnButton = '#7efff5'


def show_frame(frame):
    frame.tkraise()

#################SENTIMENT FUNCTIONS##############################
# PreProcessing
def cleanTxt(text):
    text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
    text = re.sub('#', '', text) # Removing '#' hash tag
    text = re.sub('RT[\s]+', '', text) # Removing RT
    text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
    return text

def getAnalysis(score):
    if score < 0:
      return 'Negative'
    elif score == 0:
      return 'Neutral'
    else:
      return 'Positive'


def ml_process(entry):
    consumerKey = '#'
    consumerSecret = '#'
    accessToken = '#'
    accessTokenSecret = '#'

    # Create the authentication object
    authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret) 
    # Set the access token and access token secret
    authenticate.set_access_token(accessToken, accessTokenSecret) 
    # Creating the API object while passing in auth information
    api = tweepy.API(authenticate, wait_on_rate_limit = True)

    tag = "#" + entry
    hashtag = tag
    query = tweepy.Cursor(api.search, q=hashtag).items(150)
    posts = [{'Tweets':tweet.text} for tweet in query]
    df = pd.DataFrame.from_dict(posts)

     # Clean the tweets
    df['Tweets'] = df['Tweets'].apply(cleanTxt)

    # Create a function to get the subjectivity
    def getSubjectivity(text):
        return TextBlob(text).sentiment.subjectivity

    # Create a function to get the polarity
    def getPolarity(text):
        return  TextBlob(text).sentiment.polarity

    # Create two new columns 'Subjectivity' & 'Polarity'
    df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
    df['Polarity'] = df['Tweets'].apply(getPolarity)
    df['Analysis'] = df['Polarity'].apply(getAnalysis)

    # Print the percentage of positive tweets
    ptweets = df[df.Analysis == 'Positive']
    ptweets = ptweets['Tweets']
    round( (ptweets.shape[0] / df.shape[0]) * 100 , 1)

    ntweets = df[df.Analysis == 'Negative']
    ntweets = ntweets['Tweets']
    round( (ntweets.shape[0] / df.shape[0]) * 100, 1)

    polar = df['Analysis'].value_counts()
   
    try:
        neg = polar.loc['Negative'].item()
    except:
        neg=0

    try:
        pos = polar.loc['Positive'].item()
    except:
        pos=0

    try:
        neu = polar.loc['Neutral'].item()
    except:
        neu=0


    print(f"Positive:{pos} Negative:{neg} Neutral:{neu}")
    if pos>neg and pos>neu:
        label2.config(text="POSITIVE")
        l_frame.config(background="#3ae374")
    elif neg>pos and neg>neu:
        label2.config(text="NEGATIVE")
        l_frame.config(background="#ff3838")
    else:
        label2.config(text="NEUTRAL")
        l_frame.config(background="#fff943")



    def cloud():
        # word cloud visualization
        allWords = ' '.join([twts for twts in df['Tweets']])
        wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)
        plt.imshow(wordCloud, interpolation="bilinear")
        plt.axis('off')
        plt.show()

    def scatterPlot():
        # Plotting 
        plt.figure(figsize=(8,6)) 
        for i in range(0, df.shape[0]):
            plt.scatter(df["Polarity"][i], df["Subjectivity"][i], color='Blue') 
        # plt.scatter(x,y,color)   
        plt.title('Sentiment Analysis') 
        plt.xlabel('Polarity') 
        plt.ylabel('Subjectivity') 
        plt.show()

    def barGraph():
        # Plotting and visualizing the counts
        plt.title('Sentiment Analysis')
        plt.xlabel('Sentiment')
        plt.ylabel('Counts')
        df['Analysis'].value_counts().plot(kind = 'bar')
        plt.show()

    cloudbutton = tk.Button(sentimentScreen, text="Word Cloud ",bg=buttonColor,command=lambda: cloud())
    cloudbutton.place(relx=0.01,rely=0.1, relheight=0.1, relwidth=0.08)

    barbutton = tk.Button(sentimentScreen, text="Bar Graph ",bg=buttonColor,command=lambda: barGraph())
    barbutton.place(relx=0.01,rely=0.3, relheight=0.1, relwidth=0.08)

    plotbutton = tk.Button(sentimentScreen, text="Scatter Plot ",bg=buttonColor,command=lambda: scatterPlot())
    plotbutton.place(relx=0.01,rely=0.5, relheight=0.1, relwidth=0.08)
##################KEYWORD FINDER FUNCTIONS########################
def get_Keyword(entry):
    #keyword = input("Enter keyword -> ")
    url = "http://google.com/search?q=" + entry
    source = requests.get(url).text
    soup = BeautifulSoup(source,'lxml')


    description = []
    for articles in soup.find_all('div',class_='ZINbbc'):
        for summary in articles.find_all('div',class_='BNeawe'):
            description.append(summary.text)
    #print(description)

    stopword_list = ['in','the','yes','no','these','this',
                    'is','or','a','<','>',',','"','am','an','›','-','_','.',
                    'i','on','at','My','can','to','...','$','&','for','·','|','1','2','3',
                    '4','5','6','7','8''9','0','was','his','him','her','he',
                    'Thiruvananthapuram','Trivandrum','wikipedia','-']

    words = []
    for value in description:
        for word in value.split(' '):
            words.append(word)
    #print(words)

    count = {}
    for val in words:
        if val in count:
            count[val]=count[val]+1
        else:
            count[val]=1
    #print(count)

    Final_keyword = []
    for x in count.items(): 
        if x[1]>=3:
            if x[0].lower() not in stopword_list:
                Final_keyword.append(x[0])
                #print(x[0])
                #print()


    label.config(text=("\n".join(Final_keyword)))


window = tk.Tk()

window.state('zoomed')
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
window.title('Social Media Monitoring')



#Frame Decleration
mainScreen = tk.Frame(window,bg=bgColor)
keywordscreen = tk.Frame(window)
sentimentScreen = tk.Frame(window)


for frame in (mainScreen,keywordscreen,sentimentScreen):
    frame.grid(row=0,column=0,sticky='nsew')

#mainScreen Frame Code
mainScreen_Button1 = tk.Button(mainScreen,text='Keyword Finder',bg=buttonColor,font=50,command=lambda:show_frame(keywordscreen))
mainScreen_Button1.config(height=10,width=40)
mainScreen_Button1.place(relx = 0.7, rely = 0.66, anchor = 'ne')

mainScreen_Button2 = tk.Button(mainScreen,text='Sentiment Analysis',bg=buttonColor,font=50,command=lambda:show_frame(sentimentScreen))
mainScreen_Button2.config(height=10,width=40)
mainScreen_Button2.place(relx = 0.56, rely = 0.5, anchor = 'center')

title = tk.Label(mainScreen,text='Socail media Monitoring',bg=labelColor,font=100,fg='#fff')
title.place(relx=0.2, rely=0.15, relwidth=0.6, relheight=0.1)


#keywordScreen Frame Code
frameInside = tk.Frame(keywordscreen,bg=bgColor,width=1000,height=800)
frameInside.place(relx=0.5, rely=0.5, anchor='center')

entry = tk.Entry(frameInside)
entry.place(relwidth=0.4, relheight=0.2)

button = tk.Button(frameInside, text="Enter Keyword",bg=fnButton, font=40,command=lambda: get_Keyword(entry.get()))
button.place(relx=0.7, relheight=0.2, relwidth=0.2)

lower_frame = tk.Frame(frameInside, bg='black', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

label = tk.Label(lower_frame)
label.place(relwidth=1, relheight=1)

button = tk.Button(frameInside, text="BACK", bg=fnButton,font=40,command=lambda:show_frame(mainScreen))
button.place(relx=0.9,rely=0.8, relheight=0.1, relwidth=0.1)

#sentimentScreen Frame Code
entry = tk.Entry(sentimentScreen, font=40)
entry.place(relx=0.2, relheight=0.2, relwidth=0.2)

button = tk.Button(sentimentScreen, text="Find Sentiment",bg=fnButton, font=40,command=lambda: ml_process(entry.get()))
button.place(relx=0.6, relheight=0.2, relwidth=0.2)

l_frame = tk.Frame(sentimentScreen, bg=bgColor, bd=10)
l_frame.place(relx=0.1, rely=0.25, relwidth=0.75, relheight=0.6)

label2 = tk.Label(l_frame)
label2.place(relx=0.3,rely=0.4,relheight=0.3, relwidth=0.3)

button = tk.Button(sentimentScreen, text="BACK",bg=fnButton, font=40,command=lambda:show_frame(mainScreen))
button.place(relx=0.9,rely=0.8, relheight=0.1, relwidth=0.1)


show_frame(mainScreen)
window.mainloop()