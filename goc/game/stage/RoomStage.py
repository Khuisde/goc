# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 11:50:37 2019

@author: Phoenix
"""

from .Stage import Stage
from .Map import Map
from ..util import constants

import Global

class RoomStage(Stage):
    
    def __init__(self):
        Stage.__init__(self)
        self.active = True
        self.images = ["image/textures/white_border.png",
                       "image/textures/gray_border.png",
                       "image/textures/grayscale.png",
                       "image/textures/black.png",
                       "image/textures/r_bg_1.png",
                       "image/textures/r_side_door.png",
                       "image/textures/r_platform.png",
                       "image/textures/r_cable.png"]
        self.textures = []
        
#        self.width = 10 #20
#        self.height = 4 #13
#        self.depth = 4 #10
        self.width = 20 #20
        self.height = 4 #13
        self.depth = 4 #10
        
        self.position = (0,0,0.2) #(0,0,0.4)
        #z = max(1,max(self.width,self.height)*0.07)
        # 10 0.9
        # 15 1.2
        # 20 1.5
        # 30 2.2
        # 40 2.9
        self.default_viewport = ((self.width * constants.blockScale)/2,(self.height* constants.blockScale)/2,1.4) #2
        
        for i in self.images:
            index, width, height = Global.master.screen.loadImage(i)
            vbo, vbo_count = Global.master.screen.create_image_vbo(width,height)
            self.textures.append((index, width, height, vbo, vbo_count))
            #self.textures.append((index, width, height))
            
        self.unordered_draw = True
            
        self.room_vbos = []
        # 0 = bottom floor
        # 1 = right wall
        # 2 = top ceiling
        # 3 = left wall
        # 4 = back wall
        
        self.map = Map.createEmpty(self.width,self.height)
        self.gen_room_coordinates()
        
    def gen_room_coordinates(self):
        #w = self.width * constants.blockScale
        #h = self.height * constants.blockScale
        #d = self.depth * constants.blockScale
        w = 10 * constants.blockScale
        h = 4 * constants.blockScale
        d = 4 * constants.blockScale
        
#        coordinates = self.createRoom(w,h,d,[1,2,3,5,4])
#        dx = -w
#        dy = 0
#        dz = 0
#        coordinates += self.createRoom(w,h,d,[6,5,3,2,2],dx,dy,dz)
#        coordinates += self.createImage(w/5,0,w*0.15,h*0.7,d*0.7,7,dx,dy,dz)
        
        coordinates = self.createRoom(w,h,d,[6,5,3,2,2])
        coordinates += self.createRoom(w,h,d,[1,2,3,5,4],dx=w+constants.mue)
        coordinates += self.createImage(w/5,0,w*0.15,h*0.7,d*0.7,7)
               
        for c,tx in coordinates:
            vbo, vbo_count = Global.master.screen.create_vbo_3d(w,h,c)
            self.room_vbos.append((w,h,vbo, vbo_count, tx))

    def createRoom(self,w,h,d,textures,dx=0,dy=0,dz=0):
        # Bottom, right, top, left, back
        return [
               ([w+dx,    0+dy,    -d+dz,       1,      1, # Top right
                 w+dx,    0+dy,    0+dz,        1,      0, # Bottom right
                 0+dx,    0+dy,    0+dz,        0,      0, # Bottom left
                 0+dx,    0+dy,    -d+dz,       0,      1 ],textures[0]), # Top left
               ([w+dx,    h+dy,    0+dz,        1,      1,   # UR
                 w+dx,    0+dy,    0+dz,        1,      0,  # DR
                 w+dx,    0+dy,    -d+dz,       0,      0,  # DL
                 w+dx,    h+dy,    -d+dz,       0,      1 ],textures[1]), # UL
               ([0+dx,    h+dy,    -d+dz,       1,      1,   # UR
                 0+dx,    h+dy,    0+dz,        1,      0,  # DR
                 w+dx,    h+dy,    0+dz,        0,      0,  # DL
                 w+dx,    h+dy,    -d+dz,       0,      1 ],textures[2]), # UL
               ([0+dx,    h+dy,    -d+dz,       1,      1,   # UR
                 0+dx,    0+dy,    -d+dz,       1,      0,  # DR
                 0+dx,    0+dy,    0+dz,        0,      0,  # DL
                 0+dx,    h+dy,    0+dz,        0,      1 ],textures[3]), # UL
               ([w+dx,    h+dy,    -d+dz,       1,      1,   # UR
                 w+dx,    0+dy,    -d+dz,       1,      0,  # DR
                 0+dx,    0+dy,    -d+dz,       0,      0,  # DL
                 0+dx,    h+dy,    -d+dz,       0,      1 ],textures[4]) # UL
               ]
        
       
    def createImage(self,x,y,w,h,d,texture,dx=0,dy=0,dz=0):
        # Bottom, right, top, left, back 
        return [
               ([x+w+dx,  y+h+dy,  -d+dz,       1,      1,   # UR
                 x+w+dx,  y+dy,    -d+dz,       1,      0,  # DR
                 x+dx,    y+dy,    -d+dz,       0,      0,  # DL
                 x+dx,    y+h+dy,  -d+dz,       0,      1 ],texture) # UL
               ]
        
    def update(self):
        Stage.update(self)
        
    def initViewport(self):
        Global.master.game.viewport = [self.default_viewport[0],self.default_viewport[1],self.default_viewport[2]]
        
    def setViewport(self):
        pass
        #px,py,pz = Global.master.game.viewport
        #Global.master.game.viewport = [self.default_viewport[0],self.default_viewport[1],pz]
            
    def draw(self, screen):
            
        for box in self.room_vbos:
            screen.draw_vbo_pos(self.position,self.textures[box[4]][0],box[2],box[3])
        #screen.draw_vbo_pos((0,0,-0.4),self.textures[0][0],self.room_vbos[0][2],self.room_vbos[0][3])
        #screen.draw_vbo_pos((0,0,-0.4),self.textures[0][0],self.textures[0][3],self.textures[0][4]
        #if self.unordered_draw:
        #    screen.disableImageDepth()
            
        if self.player is not None:
            self.player.draw(screen)
            
        #if self.unordered_draw:
        #    screen.enableImageDepth()