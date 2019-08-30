# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 16:14:52 2019

@author: Phoenix
"""

import os
from .Stage import Stage
from .Map import Map

import Global

class WaterStage(Stage):
    
    def __init__(self):
        Stage.__init__(self)
        self.active = True
        
        self.id = "Test 2d Level"
        
        self.images = ["image/Wasser_1.png",
                    "image/Wasser_2.png",
                    "image/Wasser_3.png",
                    "image/Wasser_4.png",
                    "image/Level1Final.png"]
        self.textures = []
        
        self.unordered_draw = True
        
        for i in self.images:
            index, width, height = Global.master.screen.loadImage(i)
            vbo, vbo_count = Global.master.screen.create_image_vbo(width,height)
            self.textures.append((index, width, height, vbo, vbo_count))
        
        self.map = Map.createFromLevel(os.path.join(Global.master.dir,"image/level.bmp"))
        
        self.do_draw_vbo = False
        
    def update(self):
        Stage.update(self)
            
    def draw(self, screen):
        if self.unordered_draw:
            screen.disableImageDepth()
        #screen.drawImageSimple(self.textures[4][0],0,0,5,5,-3)
        #screen.drawImageSimple(self.textures[11][0],0,0,self.textures[11][1]*6/1920,self.textures[11][2]*6/1920,-4+constants.mue)#-2)
        screen.draw_vbo_pos((0,0,0),self.textures[4][0],self.textures[4][3],self.textures[4][4])
        #screen.draw_vbo_pos((0,0,-4+constants.mue),self.textures[11][0],self.textures[11][3],self.textures[11][4])
        
        #self.drawVbo(screen)
        if self.do_draw_vbo:
            self.map.drawVbo(screen)
        self.drawUnits(screen)
        if self.player is not None:
            self.player.draw(screen)
        if self.unordered_draw:
            screen.enableImageDepth()