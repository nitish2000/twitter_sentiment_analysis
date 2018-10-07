from flask import Flask,render_template,request
import flask
import json
from textblob import TextBlob

from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
from credentials import *
import datetime


auth = OAuthHandler(consumer_api_key, consumer_api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)



app = Flask(__name__)
global l
l=[]
@app.route('/')
def addbook():
 	return render_template('interface.html')

@app.route('/<tagname>/<time_frame>',methods=['GET'])
def add(tagname,time_frame):
	l.append('#'+tagname)
	l.append(time_frame)
	positive=0
	negative=0
	neutral=0

	for tweet in tweepy.Cursor(api.search,q=l[0],count=1000,lang="en",since='2018-01-01').items(1000):

		analysis=TextBlob(tweet.text)
		print (type(analysis))
		if analysis.sentiment.polarity>0:
			positive+=1
		elif analysis.sentiment.polarity<0:
			negative+=1
		else:	
				neutral+=1

	s=positive+negative+neutral
	if s=0:
		s+=1
	positive=(positive/s)*100
	negative=(negative/s)*100
	neutral=(neutral/s)*100	 

	return render_template('interface.html',positive=positive,negative=negative,neutral=neutral)
if __name__=='__main__':
	app.run(debug=True,host='0.0.0.0')
