# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 13:15:28 2019

@author: Phoenix
"""

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
superdir = os.path.dirname(currentdir)
if not currentdir in sys.path:
    sys.path.insert(0,currentdir)
if not superdir in sys.path:
    sys.path.insert(0,superdir)

#print(sys.path)

from goc.Master import Master
import Global

print("Starting.")

master=Master(sys.argv)
Global.init(master)
Global.run()

print("Done.")