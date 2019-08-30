# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 15:37:14 2019

@author: Phoenix
"""

import Global

class Background:
    
    def __init__(self,picturepath):
        self.image = picturepath
        self.texture, self.width, self.height = Global.master.screen.loadImage(picturepath)
        
    def update(self):
        pass
        
        
    def draw(self,screen):
        screen.disableImageDepth()
        screen.drawImagePartFixed(self.texture,-1.6,-1,0,3.2,2,(0,0,0,0),horizontal_fixed=True,vertical_fixed=True)
        screen.enableImageDepth()