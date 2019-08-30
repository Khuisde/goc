# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 13:56:55 2019

@author: Phoenix
"""

from .stage.WaterStage import WaterStage
from .stage.RoomStage import RoomStage
from .stage.Lv_Tower_1 import Lv_Tower_1

from .entity.Player import Player
from graphics.Background import Background
from graphics.WaterBackground import WaterBackground

import Global

# Layer
#
# 0.
#
#
#
#


class Game:
    
    def __init__(self, arguments=None):
        
        self.arguments = arguments
        
        
    def init(self):
        
        self.viewport = [0,0,2]
        
        #self.background = WaterBackground()
        self.background = Background("image/background.png")
        
        self.stages = []
        self.stages.append([-2.0,WaterStage()])
        self.stages.append([-1.6,WaterStage()])
        self.stages.append([-1.2,WaterStage()])
        self.stages.append([-0.8,WaterStage()])
        self.stages.append([-0.4,Lv_Tower_1()])
        #self.stages.append([0,WaterStage()])
        self.stages.append([0,RoomStage()])
        
        
        self.stage = self.stages[-1][1]
        self.player = Player()
        self.player_layer = -1
        
        self.stage.addPlayer(self.player)
        self.stage.initPlayer(self.player)
        self.stage.initViewport()
        
        
        #self.layers = reversed(range(10))
        self.layers = range(10)
        
        
    def playerLayerUp(self):
        if len (self.stages) > 1:
            self.stages[self.player_layer][1].delPlayer()
            self.player_layer = (self.player_layer + len(self.stages) - 1) % len(self.stages)
            self.stage = self.stages[self.player_layer][1]
            self.stage.addPlayer(self.player)
            self.stage.initPlayer(self.player)
            self.stage.initViewport()
        
    def playerLayerDown(self):
        if len (self.stages) > 1:
            self.stages[self.player_layer][1].delPlayer()
            self.player_layer = (self.player_layer + 1) % len(self.stages)
            self.stage = self.stages[self.player_layer][1]
            self.stage.addPlayer(self.player)
            self.stage.initPlayer(self.player)
            self.stage.initViewport()
        
    def update(self):
        
        if self.background:
            self.background.update()
        
        if self.stage:
            #self.stage.update()
            self.stage.setViewport() # Wait, what?
            
        
        for z, stage in self.stages:
            if stage.active:
                stage.update()
                stage.do_draw_vbo = stage == self.stage
            
        if self.player:
            self.player.update(self.stage)
        
        Global.master.screen.view_pos = self.viewport
        
        
    def draw(self, screen):
        
        if self.background:
            self.background.draw(screen)
        
        for z, stage in self.stages:
            screen.gotoLayer(0,0,z)
            stage.draw(screen)
            screen.goLayerBack()
            if stage.player is not None:  # Draw up to the point where the player is
                break
        
        #if self.stage:
        #    #self.stage.drawBackground(screen)
        #    self.stage.draw(screen)
        
        #for layer in self.layers:
        #
        #    if self.stage:
        #        self.stage.drawLayer(screen,layer)
        #    #if self.player and self.player.layer == layer:
        #    #    self.player.draw(screen)
        
        #self.stage.drawLayer(screen,5)
        #if self.stage:
        #    self.stage.draw(screen)