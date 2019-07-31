# -*- coding: utf-8 -*-

from pathlib import Path
import os
from scripts import configure, file_chooser, gui
from textgenrnn import textgenrnn

class TextGenRnn():
    def __init__(self):
        self.textgen = textgenrnn()
       
        self.config = configure.init()
        
    def train_from_file(self,filename=None, num_epochs=None, save_epochs=None):
        #config_folder = Path("textgenrnn_config.json")#"textgenrnn_config.json"
        self.textgen = textgenrnn()
        if filename==None:
            filename=file_chooser.by_folder("./data",".txt")
        if num_epochs==None or num_epochs=="": num_epochs=int(self.config["RNN"]["num_epochs"])
        if save_epochs==None or save_epochs=="": save_epochs=int(self.config["RNN"]["save_epochs"])
        self.textgen.train_from_file(filename, num_epochs=num_epochs, save_epochs=save_epochs)
        self.textgen.generate()
        filen, file_extension = os.path.splitext(filename)
        self.textgen.save("./trained_models/%s.hdf5"%(os.path.basename(filen)))

    def train_from_previous_model(self,filename=None,model=None):
        self.textgen = textgenrnn(config_path="./textgenrnn_config.json",weights_path="./textgenrnn_weights.hdf5",vocab_path="./textgenrnn_vocab.json")
        if filename==None:
            filename=file_chooser.by_folder("./data",".txt")
        self.textgen.train_from_file(filename, self.config["RNN"]["num_epochs"], self.config["RNN"]["save_epochs"])
        output = self.textgen.generate()
        return output
        
    def load_model(self,modelfile):
        self.textgen.load(modelfile)
    
    def save_model(self,modelname):
        self.textgen.save(modelname)
    
if __name__ == '__main__':
    myTextGenRnn=TextGenRnn()
    myTextGenRnn.train_from_file()