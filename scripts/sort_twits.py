# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 12:21:27 2019

@author: rober
"""

import json
from scripts import file_chooser
from operator import itemgetter

def sort_by_retweets(filename=None):
    if filename==None:
        filename=file_chooser.by_folder("./data")
    
    with open(filename) as json_file:
        my_trends = json.load(json_file)
    for trend_name in my_trends.keys():
        my_trends[trend_name]["twits"] = sorted(my_trends[trend_name]["twits"], key = itemgetter('retweet_count'), reverse=True)
    with open(filename, 'w') as json_file:
        json.dump(my_trends, json_file) 
    print ("sorted.")
    
if __name__ == '__main__':
    sort_by_retweets()