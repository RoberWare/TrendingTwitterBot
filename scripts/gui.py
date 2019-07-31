# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 12:44:02 2019

@author: rober
"""

modes={"terminal":0, "telegram":1}

mode=modes["terminal"]

def out(text):
    if mode == modes["terminal"]:
        print(text)

def inp(text):
    if mode == modes["terminal"]:
        out=input(text)
    return out