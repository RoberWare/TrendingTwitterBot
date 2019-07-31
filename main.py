# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 14:42:58 2019

@author: rober
"""

import os,sys
from scripts import configure, gui, file_chooser, twitter_api, sort_twits, file_formatter, text_generator

class MainApp():
    def __init__(self):
        self.config = configure.init()
        self.myTextGenRnn=None

    def trending_twit_maker(self):
        gui.out("Retrieving twits...")
        filename=None

        myTwitterAPI=twitter_api.TwitterAPI()
        filename = myTwitterAPI.get_trending_twits()
        sort_twits.sort_by_retweets(filename)
        filename=file_formatter.json_to_txt(filename)

        self.myTextGenRnn=text_generator.TextGenRnn()
        self.train(filename) 

        return
    
    def user_twit_maker(self):
        myTwitterAPI=twitter_api.TwitterAPI()
        username=gui.inp("username > ")
        status,filename = myTwitterAPI.get_twits_from_user(username)
        if status>100:
            filename=file_formatter.json_to_txt(filename,show_username=False)

            self.myTextGenRnn=text_generator.TextGenRnn()
            self.train(filename)
        elif status >1:
            gui.out("we couldn't retrieve all the tweets, or they aren't enough (they were %s)"%(status))
        else:
            gui.out("please, try again.")
        return
    
    def new(self):
        header = """\n=== TwitterTrendingBot === 
        [0] Trending twits
        [1] By username
        [2] Back
        """
        flag=1
        while flag:
            gui.out(header)
            i=gui.inp("> ")
            try:
                mode = int(i)
                if mode in [0,1,2]:flag=0
            except:
                gui.out("<%s> no es un número válido."%(i))
        
        if mode == 0:
            self.trending_twit_maker()
        if mode == 1:
            self.user_twit_maker()
        else:
            sys.exit()
        return  
        
    def load(self):
        header = """\n=== TwitterTrendingBot === 
        Load
        [0] From twits file
        [1] From a previous trained model
        [2] Back
        """ 
        flag=1
        while flag:
            gui.out(header)
            i=gui.inp("> ")
            try:
                mode = int(i)
                if mode in [0,1,2]:flag=0
            except:
                gui.out("<%s> no es un número válido."%(i))
        
        if mode == 0:
            filename = file_chooser.by_folder("./data",[".txt"])
            file, file_extension = os.path.splitext(filename)
            if file_extension == ".json":
                sort_twits.sort_by_retweets(filename)
                filename=file_formatter.json_to_txt(filename)
            self.myTextGenRnn=text_generator.TextGenRnn()
            self.train(filename)
        elif mode == 1:
            filename = file_chooser.by_folder("./trained_models",[".hdf5"])
            self.myTextGenRnn=text_generator.TextGenRnn()
            self.myTextGenRnn.load_model(filename)
            
            mode=0 
            header = """\n=== TwitterTrendingBot === 
            Model loaded.
            [0] Train
            [1] Generate
            [2] Back
            """
            main_flag=1
            while main_flag:
                flag=1
                while flag:
                    gui.out(header)
                    i=gui.inp("> ")
                    try:
                        mode = int(i)
                        if mode in [0,1,2]:flag=0
                    except:
                        gui.out("<%s> no es un número válido."%(i))
                
                if mode == 0:
                    gui.out("choose a file to train with.")
                    filename = file_chooser.by_folder("./data",[".txt"])
                    self.train(filename)

                if mode == 1:
                    self.myTextGenRnn.textgen.generate()
                else:
                    main_flag=0
        return
        
    def train(self,filename):
        num_epochs=int(gui.inp("num_epochs: "))
        save_epochs=int(gui.inp("save_epochs: "))
        self.myTextGenRnn.train_from_file(filename,num_epochs,save_epochs)
        return

    def run(self):
        mode=0 
        header = """\n=== TwitterTrendingBot === 
        [0] New
        [1] Load model
        [2] Exit
        """
        while True:
            flag=1
            while flag:
                gui.out(header)
                i=gui.inp("> ")
                try:
                    mode = int(i)
                    if mode in [0,1,2]:flag=0
                except:
                    gui.out("<%s> no es un número válido."%(i))
            
            if mode == 0:
                self.new()
            if mode == 1:
                self.load()
            else:
                sys.exit()        

if __name__ == "__main__":
    myMainApp=MainApp()
    myMainApp.run()