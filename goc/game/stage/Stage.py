# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 16:14:22 2019

@author: Phoenix
"""

import Global

class Stage:
    
    def __init__(self):
        self.active = True
        self.map = None
        self.player = None
        self.id = None
        #self.background = None
        
    def addPlayer(self,player):
        self.player = player
        #if self.map is not None:
        #    player.position[0] = 14*0.1
        #    player.position[1] = (self.map.height-40)*0.1
            
    def delPlayer(self):
        self.player = None
        
    def initPlayer(self,player):
        if self.map is not None:
            #player.position[0] = 14*0.1
            #player.position[1] = (self.map.height-40)*0.1
            self.map.init_player(player)
        
    def update(self):
        
        if self.map is not None:
            self.map.update(self)
        
        #if self.background is not None:
        #    self.background.update()
            
    def initViewport(self):
        if self.player is not None:
            self.player.setViewport()
        
    def setViewport(self):
        if self.player is not None:
            self.player.setViewport()
            
    #def draw(self, screen):
    #    self.drawBackground(screen)
    #    self.drawVbo(screen)
    #    self.drawUnits(screen)
        
    def drawUnits(self,screen):
        if self.map is not None:
            self.map.drawUnits(screen)
        
    #def drawVbo(self,screen):
    #    layer = 4
    #    if self.map is not None:
    #        screen.draw_vbo(self.map.vbo,self.map.vbo_vec_count,(0,0,layer*0.1))
    #        #screen.directStart()
    #        #for y in range(self.height):
    #        #    for x in range(self.width):
    #        #        if self.map[x,y] == 1:
    #        #            screen.directDrawColorRect((0,0,0),x*0.05+screen.box_pos[0], y*0.05+screen.box_pos[1], 0.05, 0.05, 3)
    #        #        #else:
    #        #        #    screen.directDrawColorRect((1,1,1),x*0.05+screen.box_pos[0], y*0.05+screen.box_pos[1], 0.05, 0.05, 3)
    #        #screen.directEnd()
            
    #def drawBackground(self,screen):
    #    if self.background is not None:
    #        self.background.draw(screen)