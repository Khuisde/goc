# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 15:49:54 2019

@author: Phoenix
"""

master = None
 
def init(new_master):
    global master
    master = new_master
    master.init()
   
def run():
    global master
    if master is not None:
        master.main()
    
def quit():
    global master
    if master is not None:
        master.quit()
       