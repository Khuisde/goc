# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 18:13:47 2019

@author: Phoenix
"""

import os
import Global

class Dialog():
    
    def __init__(self,x,y,text,size=None):
        
        self.enabled = False
        self.autoresize = size is None
        
        self.selector = None
        self.selector_enabled = False
        
        sz = Global.master.screen.size
        self.x = (x / sz[0]) *2 -1
        self.y = (y / sz[1]) *2 -1
        self.z = 1
        if size is not None:
            self.width = size[0] / sz[0] *2
            self.height = size[1] / sz[1] *2
        else:
            self.width = 0
            self.height = 0
        
        self.font_size = [20 / sz[0] *2 ,34 / sz[1] *2]
        self.padding = [5 / sz[0] *2 , 5 / sz[1] *2] 
        self.fns = [self.font_size[0]+self.padding[0],self.font_size[1]+self.padding[1]]
        
        self.spacing = [30 / sz[0] *2 , 30 / sz[1] *2] 
        
        self.text =  []
        
        self.top = self.y + self.height
        self.left = self.x
        self.right = self.x + self.width
        self.bottom = self.y
        
        if type(text) is str:
            self.text.append([self.spacing[0],0,text-self.spacing[1]])
        if type(text) is list:
            index = 1
            for line in text:
                self.text.append([self.spacing[0],-self.spacing[1]-self.fns[1]*index,line])
                index+=1
        
        self.graphic_file = os.path.join(Global.master.dir,"image/Box_transp.png")
        self.box_tex, self.box_width, self.box_height = Global.master.screen.loadImage(self.graphic_file)
        #print(self.text)
        
        if size is None:
            self.fitToText()
        
    def transformPixToRelative(self,x,y):
        x = (x / Global.master.screen.size[0]) *2 -1
        y = (y / Global.master.screen.size[1]) *2 -1
        return x,y
    
    def getText(self):
        text = []
        for line in self.text:
            text.append(line[2])
        return text
    
    def setText(self, text):
        self.text =  []
        if type(text) is str:
            self.text.append([self.spacing[0],0,text-self.spacing[1]])
        if type(text) is list:
            index = 1
            for line in text:
                self.text.append([self.spacing[0],-self.spacing[1]-self.fns[1]*index,line])
                index+=1
        if self.autoresize:
            self.fitToText()
        #if type(text) is str:
        #    self.text.append([self.left+self.spacing[0],self.top,text-self.spacing[1]])
        #if type(text) is list:
        #    index = 1
        #    for line in text:
        #        self.text.append([self.left+self.spacing[0],self.top-self.spacing[1]-self.fns[1]*index,line])
        #        index+=1
        
    def setSelector(self,index):
        if index is not None and index >= 0 and index < len(self.text):
            text = self.text[index]
            self.selector = [text[0]-self.spacing[0]/2,text[1]-self.padding[1]/2,self.width-self.spacing[0],self.font_size[1]+self.padding[1]*2]
            self.selector_enabled = True  
        else:
            self.selector = None
            self.selector_enabled = False
                    
        
    def addLine(self,text):
        index = len(self.text) +1
        self.text.append([self.left,self.top-self.fns[1]*index,text])
        
    def fitToText(self):
        maxline = self.font_size[0]
        for line in self.text:
            if len(line[2]) > maxline: 
                maxline = len(line[2])
        self.width = self.spacing[0]*2 + self.fns[0]*maxline - self.padding[0]
        self.height = self.spacing[1]*2 + self.fns[1]*len(self.text) - self.padding[1]
        self.right = self.x + self.width
        self.top = self.y + self.height
        #self.y = self.top - self.height # top ancor
        
    def draw(self,screen):
        if self.enabled:
            screen.drawInterfaceImage(self.box_tex,self.x,self.y,self.z,self.width,self.height)
            if self.selector_enabled and self.selector is not None:
                screen.drawInterfaceImage(self.box_tex,self.left+self.selector[0],self.top+self.selector[1],self.z,self.selector[2],self.selector[3])
            for line in self.text:
                screen.drawText((self.left+line[0],self.top+line[1]),line[2])