# -*- coding: utf-8 -*-

import configparser
from scripts import gui

def init():
    config = configparser.ConfigParser()
    if not config.read('./config/config.ini'):
        gui.out(" === RNN CONFIG === ")
        num_epochs=gui.inp("num_epochs: ")
        save_epochs=gui.inp("save_epochs: ")
        config["RNN"]={}
        config["RNN"]["num_epochs"]=num_epochs
        config["RNN"]["save_epochs"]=save_epochs
        
        gui.out(" === TWITTER CONFIG === ")
        consumer_key=gui.inp("consumer_key: ")
        consumer_secret=gui.inp("consumer_secret: ")
        access_token=gui.inp("access_token: ")
        access_token_secret=gui.inp("access_token_secret: ")
        COUNTRY_WOE_ID=gui.inp("COUNTRY_WOE_ID (by default 753692): ")
        include_promoted_tweets=gui.inp("include_promoted_tweets (0 or 1): ")
        max_trends_number =gui.inp("max_trends_number (recommended 5): ")
        config["TWITTER"] = {}
        config["TWITTER"]["consumer_key"]=consumer_key
        config["TWITTER"]["consumer_secret"]=consumer_secret
        config["TWITTER"]["access_token"]=access_token
        config["TWITTER"]["access_token_secret"]=access_token_secret
        if COUNTRY_WOE_ID == "": COUNTRY_WOE_ID=753692
        config["TWITTER"]["COUNTRY_WOE_ID"]=COUNTRY_WOE_ID
        config["TWITTER"]["include_promoted_tweets"]=include_promoted_tweets
        config["TWITTER"]["max_trends_number "]=max_trends_number 
        with open('./config.ini', 'w') as configfile:
            config.write(configfile)
    return config