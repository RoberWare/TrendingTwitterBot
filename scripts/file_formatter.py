# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 13:36:23 2019

@author: rober
"""

import os,json, emoji
from scripts import file_chooser

def json_to_txt(filename=None, show_username=True):
    if filename==None:
        filename=file_chooser.by_folder("./data", [".json"])
    with open(filename) as json_file:
        my_trends = json.load(json_file)
    text=""
    for trend in my_trends.keys():
        for twit in my_trends[trend]["twits"]:
            if show_username:
                text = text+"@"+twit["user"]+": "
            text=text+twit["text"]+ "\n"
    
    text = emoji.demojize(text)
    
    filen, file_extension = os.path.splitext(filename)
    filename=filen+".txt"
    
    with open(filename, "w", encoding='utf-8') as file:
        file.write(text)
    print ("\ndone.")
    
    return filename

if __name__ == '__main__':
    json_to_txt()