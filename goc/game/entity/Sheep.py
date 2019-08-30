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

class Sheep(GoCObject):
    
    def __init__(self,pos=[0,0]):
        GoCObject.__init__(self)
        self.images = ["image/units/monster/sheep/dead.png",
                    "image/units/monster/sheep/idle.png",
                    "image/units/monster/sheep/walk_1.png",
                    "image/units/monster/sheep/walk_2.png",
                    "image/units/monster/sheep/walk_3.png"]
        
        self.textures = []
        
        for i in self.images:
            index, width, height = Global.master.screen.loadImage(i)
            self.textures.append((index, width/400, height/300))
           
        self.animation = 0
        
        self.rot = [0,0,-1,0]
        self.frame = 0
        
        self.ch_direction = 1
        self.direction = 1
        
        self.position = pos
        self.size = [0.2,0.1] #[0.2,0.2]
        self.hitbox_size = [0.12,0.1]
        self.sprite_offset = [0,0]
        self.velocity = [0,0]
        self.physicValue = 0
        
    def update(self,stage):
        
        if self.physicValue == 1:
            self.velocity[0] += self.direction * constants.enemyWalkVelocity
        
        #self.physicValue = 0 # Overwrite test!
        prev_phys = self.physicValue
        pos, self.velocity, self.physicValue, wallhit = physics.apply(self.position, self.velocity, self.hitbox_size, self.physicValue, stage.map)
        
                
        #if self.velocity[0] != 0: self.ch_direction = self.velocity[0]
        if wallhit[0]: self.ch_direction = -1
        elif wallhit[2]: self.ch_direction = 1
        
        if self.ch_direction > 0: 
            if self.direction < 1:
                self.direction += 0.2
        elif self.ch_direction < 0:
            if self.direction > -1:
                self.direction -= 0.2
                
        
        #if self.direction > 0: self.rot[3] = 0.15
        #else:  self.rot[3] = -0.15
        
        if self.direction < 1: self.rot[2] = 1
        self.rot[0] = 180 * (0.5-self.direction/2)
        self.rot[1] = 0
        self.rot[3] = 0
        
        if prev_phys != self.physicValue: self.animation = 0
        if self.physicValue == 1:
            if abs(self.velocity[0]) < constants.minVelocity:
                self.frame = 1
            else:
                self.animation = (self.animation + 1) % 40        
                if self.animation < 10: self.frame = 1
                elif self.animation < 20: self.frame = 2
                elif self.animation < 30: self.frame = 3
                else: self.frame = 4
        elif self.physicValue == 0:
            self.frame = 1
        #print(self.x/0.1,",",self.y/0.1)
    
    def draw(self,screen):
        tex = self.textures[self.frame]
        z = constants.mue
        #emission = (0.01,0.01,1,1)
        #emission = (1,0,0,1)
        #screen.drawImageSimpleRot(tex[0],self.position[0],self.position[1],tex[1],tex[2],self.layer,(self.rot,0,0,1),(0,0),emission)
        
        #if self.direction >= 1: screen.draw_default(tex[0],self.position[0],self.position[1]+self.size[1]/2,layer*0.1)
        #else: 
        #    screen.draw_default_rot(tex[0],self.position[0],self.position[1]+self.size[1]/2,layer*0.1,self.rot)
        screen.draw_default_rot(tex[0],self.position[0]+self.sprite_offset[0],self.position[1]+self.sprite_offset[1],z,self.rot)