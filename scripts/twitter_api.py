# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 10:31:57 2019

@author: rober
"""

import datetime
import tweepy
import json
from scripts import gui, configure
 
# Where On Earth ID for Brazil is 23424768.
SPAIN_WOE_ID = 753692

class TwitterAPI():
    def __init__(self):
        self.my_trends = {}
        self.config = configure.init()
        auth = tweepy.OAuthHandler(self.config["TWITTER"]["consumer_key"], self.config["TWITTER"]["consumer_secret"])
        auth.set_access_token(self.config["TWITTER"]["access_token"], self.config["TWITTER"]["access_token_secret"])
        self.api = tweepy.API(auth)

    def get_trending_twits(self):
        filename=filename='./data/trends_%s.json'%(datetime.datetime.now().strftime("%d%m%y"))
        
        COUNTRY_WOE_ID=self.config["TWITTER"]["COUNTRY_WOE_ID"]
        country_trends = self.api.trends_place(COUNTRY_WOE_ID)
        trends = json.loads(json.dumps(country_trends, indent=1))    

        num=1
        for trend in trends[0]["trends"]:
            if num <= int(self.config["TWITTER"]["max_trends_number"]):
                if (not self.config["TWITTER"]["include_promoted_tweets"] and not trend["promoted_content"]) or (self.config["TWITTER"]["include_promoted_tweets"]):
                    trend_name = (trend["name"]).strip("#")
                    trend_url = trend["url"]
                    
                    self.my_trends[trend_name]={}
                    self.my_trends[trend_name]["url"]=trend_url
                    
                    gui.out(">>> "+trend_name+" <<<")
                    gui.out((num,self.config["TWITTER"]["max_trends_number"]))
                    
                    querry="%s -filter:retweets"%(trend_name)
                    search = tweepy.Cursor(self.api.search, q=querry, lang="es", tweet_mode='extended', wait_on_rate_limit=True).items(200)
                    self.my_trends[trend_name]["twits"]=[]
                    for item in search:
                        if (not item.retweeted) and ('RT @' not in item.full_text):
                            twit_dict = {}
                            twit_dict["user"]=item.user.name
                            twit_dict["created_at"]=str(item.created_at)
                            twit_dict["text"]=item.full_text
                            twit_dict["retweet_count"]=item.retweet_count
                            self.my_trends[trend_name]["twits"].append(twit_dict)
                            #print (" <@user> "+item.user.name)
                            #print (item.created_at)
                            #print (item.text)
                            #print (item.retweet_count)
                    num+=1 
        with open(filename, 'w') as json_file:
            json.dump(self.my_trends, json_file) 
        gui.out("done.")
        return filename
        
    def get_twits_from_user(self, username):
        tweets = tweepy.Cursor(self.api.user_timeline, id=username, tweet_mode='extended', wait_on_rate_limit=True).items()
        # Empty Array 
        fake_trends={}
        fake_trends[username]={}
        fake_trends[username]["twits"]=[]
        fake_trends[username]["url"]=username
        num_tweets=0
        for item in tweets:
            twit_dict = {}
            twit_dict["user"]=item.user.name
            twit_dict["created_at"]=str(item.created_at)
            twit_dict["text"]=item.full_text
            twit_dict["retweet_count"]=item.retweet_count            
            fake_trends[username]["twits"].append(twit_dict)
            num_tweets+=1
        filename='./data/%s_%s.json'%(username,datetime.datetime.now().strftime("%d%m%y"))
        with open(filename, 'w') as json_file:
            json.dump(fake_trends, json_file) 
            gui.out("done.")    

        status=None
        if tweets: status=1      
        return num_tweets,filename
            
        