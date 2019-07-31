# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 13:44:20 2019

@author: rober
"""

import os

def by_folder(foldername, filter=[".json"]):
    flag=1
    while flag:
        n=0
        files=[]
        for r,d,f in os.walk(foldername):
            for file in f:
                filename, file_extension = os.path.splitext(file)
                if file_extension in filter:
                    files.append(file)
                    print ("[%i] %s"%(n, file))
                    n+=1
        filenumber=input("> ")
        try:
            filename=files[int(filenumber)]
            flag=0
        except:
            print("<%s> no es un número válido."%(filenumber))
    
    return foldername+"/"+filename