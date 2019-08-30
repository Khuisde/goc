# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 16:11:22 2019

@author: Phoenix
"""

import os, math
import pygame

from .GoCObject import GoCObject
from ..util import physics, constants

import Global

class Player(GoCObject):
    
    def __init__(self):
        GoCObject.__init__(self)
        self.images = ["image/units/player/player_idle_1.png",
                    "image/units/player/player_idle_2.png",
                    "image/units/player/player_idle_3.png",
                    "image/units/player/player_idle_4.png",
                    "image/units/player/player_idle_5.png",
                    "image/units/player/player_jump_1.png",
                    "image/units/player/player_jump_2.png",
                    "image/units/player/player_jump_3.png",
                    "image/units/player/player_jump_4.png",
                    "image/units/player/player_walk_1.png",
                    "image/units/player/player_walk_2.png",
                    "image/units/player/player_dash.png"]
        
        self.textures = []
        
        for i in self.images:
            index, width, height = Global.master.screen.loadImage(i)
            self.textures.append((index, width/400, height/300))
           
        self.animation = 0
        
        self.rot = [0,0,-1,0]
        self.frame = 0
        
        self.ch_direction = 1
        self.direction = 1
        
        self.position = [0,0]
        self.size = [0.2,0.2]
        self.hitbox_size = [0.05,0.14]
        self.sprite_offset = [0,0.03]
        self.velocity = [0,0]
        self.physicValue = 0
        
    def update(self,stage):
        
        keys = pygame.key.get_pressed()
        fast = False
        if keys[pygame.K_LSHIFT]:
            fast = True
        if keys[pygame.K_LEFT]:
            if self.physicValue == 1:
                #self.velocity[0] -= constants.runVelocity
                self.velocity[0] -= constants.runVelocity if fast else constants.slowVelocity 
            else:
                self.velocity[0] -= constants.airVelocity
        if keys[pygame.K_RIGHT]:
            if self.physicValue == 1:
                #self.velocity[0] += constants.runVelocity
                self.velocity[0] += constants.runVelocity if fast else constants.slowVelocity 
            else:
                self.velocity[0] += constants.airVelocity
        if keys[pygame.K_UP]:
            if self.physicValue == 1:
                self.velocity[1] += constants.jumpVelocity
                self.physicValue = 0
        if keys[pygame.K_z]:
            print(self.position,",phy=",self.physicValue)#," cam=",Global.master.screen.side_rot)
        if keys[pygame.K_w]:
            #self.position[1] += 0.1
            self.velocity[1] = 0.05
        if keys[pygame.K_s]:
            self.physicValue = 0
        #if keys[pygame.K_r]:
        #    Global.master.game.stage.initPlayer(self)
        #if keys[pygame.K_DOWN]:
        #    self.velocity[1] -= 0.01
            
        #self.velocity[0] *= 0.90
        #self.velocity[1] *= 0.90
        #self.position[0] += self.velocity[0]
        #self.position[1] += self.velocity[1]
        
        #self.physicValue = 0 # Overwrite test!
        prev_phys = self.physicValue
        pos, self.velocity, self.physicValue, wallhit = physics.apply(self.position, self.velocity, self.hitbox_size, self.physicValue, stage.map)
        
        
        #if keys[pygame.K_x]:
        #mx = int(self.position[0]/constants.blockScale)
        #my = int(self.position[1]/constants.blockScale)
        #mapxy = stage.map.get(mx,my)
        #if mapxy == 1:
        #    print(self.position," = ",[mx,my],":",mapxy)
        
        if self.velocity[0] != 0: self.ch_direction = self.velocity[0]
        if self.ch_direction > 0: 
            if self.direction < 1:
                self.direction += 0.2
            #if Global.master.screen.side_rot < 4:
            #    Global.master.screen.side_rot += 0.2
        elif self.ch_direction < 0:
            if self.direction > -1:
                self.direction -= 0.2
            #if Global.master.screen.side_rot > -4:
            #    Global.master.screen.side_rot -= 0.2
        
        #if self.direction > 0: self.rot[3] = 0.15
        #else:  self.rot[3] = -0.15
        
        if self.direction < 1: self.rot[2] = 1
        self.rot[0] = 180 * (0.5-self.direction/2)
        if self.physicValue == 1:
            self.rot[1] = 0
            self.rot[3] = 0
        elif self.physicValue == 0:
            if self.rot[0] > 0:
                if self.direction < 0:
                    self.rot[1] = -45 / self.rot[0] * abs(self.velocity[0]) / constants.maxVelocity
                    self.rot[3] = -45 / self.rot[0] * abs(self.velocity[0]) / constants.maxVelocity
                else:
                    self.rot[1] = 45 / self.rot[0] * abs(self.velocity[0]) / constants.maxVelocity
                    self.rot[3] = 45 / self.rot[0] * abs(self.velocity[0]) / constants.maxVelocity
                #print(self.rot)
            else:
                self.rot[0] = -45 * abs(self.velocity[0]) / constants.maxVelocity
                self.rot[1] = 0
                self.rot[2] = 0
                self.rot[3] = 1
        
        
        if prev_phys != self.physicValue: self.animation = 0
        if self.physicValue == 1:
            if abs(self.velocity[0]) < constants.minVelocity:
                self.animation = (self.animation + 1) % 25        
                if self.animation < 5: self.frame = 0
                elif self.animation < 10: self.frame = 1
                elif self.animation < 15: self.frame = 2
                elif self.animation < 20: self.frame = 3
                else: self.frame = 4
            else:
                self.animation = (self.animation + 1) % 40        
                if self.animation < 10: self.frame = 0
                elif self.animation < 20: self.frame = 9
                elif self.animation < 30: self.frame = 0
                else: self.frame = 10
        elif self.physicValue == 0:
            self.animation = (self.animation + 1) % 20        
            if self.animation < 5: self.frame = 5
            elif self.animation < 10: self.frame = 6
            elif self.animation < 15: self.frame = 7
            else: self.frame = 8
        #print(self.x/0.1,",",self.y/0.1)
        
    def setViewport(self):
        px,py,pz = Global.master.game.viewport
        px = self.position[0] # (px + self.x)*2/3
        py = self.position[1] #+self.size[1]/2 # (py + self.y)*2/3
        Global.master.game.viewport = [px,py,pz]
    
    def draw(self,screen):
        tex = self.textures[self.frame]
        z = constants.mue
        #emission = (0.01,0.01,1,1)
        #emission = (1,0,0,1)
        #screen.drawImageSimpleRot(tex[0],self.position[0],self.position[1],tex[1],tex[2],self.layer,(self.rot,0,0,1),(0,0),emission)
        
        #if self.direction >= 1: screen.draw_default(tex[0],self.position[0],self.position[1]+self.size[1]/2,layer*0.1)
        #else: 
        #    screen.draw_default_rot(tex[0],self.position[0],self.position[1]+self.size[1]/2,layer*0.1,self.rot)
        #screen.draw_default_rot(tex[0],self.position[0],self.position[1]+self.size[1]/2,z,self.rot)
        screen.draw_default_rot(tex[0],self.position[0]+self.sprite_offset[0],self.position[1]+self.sprite_offset[1],z,self.rot)