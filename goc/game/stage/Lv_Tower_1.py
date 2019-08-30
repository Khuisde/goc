# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 01:06:19 2019

@author: Phoenix
"""

import os
from .Stage import Stage
from .Map import Map

import Global

class Lv_Tower_1(Stage):
    
    def __init__(self):
        Stage.__init__(self)
        self.active = True
        
        self.id = "Test Tower Level"
        
        self.images = ["image/Tower_bot_bg.png",
                    "image/Tower_bot_fg.png"]
        self.textures = []
        
        self.unordered_draw = True
        
        for i in self.images:
            index, width, height = Global.master.screen.loadImage(i)
            vbo, vbo_count = Global.master.screen.create_image_vbo(width,height)
            self.textures.append((index, width, height, vbo, vbo_count))
        
        self.map = Map.createFromLevel(os.path.join(Global.master.dir,"image/lv_tower.png"))
        
        self.do_draw_vbo = False
        
    def update(self):
        Stage.update(self)
            
    def draw(self, screen):
        if self.unordered_draw:
            screen.disableImageDepth()
        screen.draw_vbo_pos((0,0,-0.1),self.textures[0][0],self.textures[1][3],self.textures[0][4])
        screen.draw_vbo_pos((0,0,0),self.textures[1][0],self.textures[1][3],self.textures[1][4])
        if self.do_draw_vbo:
            self.map.drawVbo(screen)
        self.drawUnits(screen)
        if self.player is not None:
            self.player.draw(screen)
        if self.unordered_draw:
            screen.enableImageDepth()