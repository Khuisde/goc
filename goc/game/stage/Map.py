# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 23:50:49 2019

@author: Phoenix
"""

import numpy as np
from PIL import Image

import Global
from ..util import constants

from ..entity.Sheep import Sheep

class Map:
    
    # Blocks:
    # 0 = Air / Empty
    # 1 = Wall
    # 2 = Platform
    # 3 = Uphill
    # 4 = Downhill
    # 5 = Water
    
    def __init__(self):
        self.width, self.height = 0,0
        self.offset = [0,0]
        self.data = []
        self.units = []
        #self.outside = [1,1,1,0]
        
        self.textures = []
        self.images = ["image/blocks/block_1.png",
                       "image/blocks/water_1.png"]     
        self.player_init_pos = []
        
        self.layer_forward_zones = []
        self.layer_backward_zones = []
        
        for i in self.images:
            index, width, height = Global.master.screen.loadImage(i)
            self.textures.append((index, width, height))
        
    def createFromLevel(file,scale=0.1):
        cmap = Map()
        cmap.loadLevel(file,scale)
        return cmap
    
    def createEmpty(width, height, offset=[0,0]):
        cmap = Map()
        cmap.width = width
        cmap.height = height
        cmap.data = np.zeros((width,height),dtype=np.uint8)
        cmap.offset = offset
        return cmap
    
    def loadLevel(self,file,scale=0.1):
        try:
            image_file = Image.open(file)
            self.width, self.height = image_file.size
            self.data = np.zeros((self.width,self.height),dtype=np.uint8)
            blocks_vec = []
            textures_vec = []
            for y in range(self.height):
                for x in range(self.width):
                    #self.map[0][x,y],self.map[1][x,y],self.map[2][x,y] = image_file.getpixel((x,y))
                    mapy = self.height-y-1 # invert Y
                    ax=x*scale
                    bx=ax+scale
                    ay=self.height*scale-y*scale
                    by=ay-scale
                    try:
                        r,g,b = image_file.getpixel((x,y))
                    except ValueError:
                        r,g,b,a = image_file.getpixel((x,y))
                    #print(r,g,b)
                    self.data[x,mapy] = 0
                    
                    if r == 0 and g == 0 and b == 0: # Block
                        self.data[x,mapy] = 1
                        blocks_vec += [ax,ay,bx,ay,ax,by,ax,by,bx,by,bx,ay]
                        textures_vec += [0,0, 1,0, 0,1, 0,1, 1,1, 1,0] # TODO TEXTURES DON'T workthis way!!! put them together with blocks into 1 array!!!!!!!!
                    elif r == 128 and g == 128 and b == 128: # Platform
                        #self.data[x,self.height-y-1] = 2
                        pass
                    elif r == 70 and g == 0 and b == 0: # Uphill
                        self.data[x,mapy] = 3
                        blocks_vec += [bx,ay,ax,by,bx,by]
                        textures_vec += [1,0, 0,1, 1,1]
                    elif r == 0 and g == 0 and b == 70: # Downhill
                        self.data[x,mapy] = 4
                        blocks_vec += [ax,ay,bx,by,ax,by]
                        textures_vec += [0,0, 1,1, 0,1]
                        #textures_vec += [0,1, 1,1, 0,1]
                    elif r == 0 and g == 0 and b == 255: # Water
                        self.data[x,mapy] = 5
                        #blocks_vec += [ax,ay,bx,by,ax,by]
                    elif r == 255 and g == 0 and b == 0: # Enemy Sheep
                        #print("sheep: (",rx,",",ry,")")
                        self.units.append(Sheep([ax,ay]))
                    elif r == 255 and g == 255 and b == 0: # Player init
                        self.player_init_pos.append([ax,ay])
                    elif r == 128 and g == 0 and b == 255: # Layer Forward
                        self.layer_forward_zones.append([x,mapy])
                    elif r == 255 and g == 0 and b == 255: # Layer Backward
                        self.layer_backward_zones.append([x,mapy])
                        
            blocks_arr = np.array(blocks_vec,dtype=np.float32)
            textures_arr = np.array(textures_vec,dtype=np.float32)
            self.vbo_vec_count = blocks_arr.shape[0]
            self.vbo = Global.master.screen.create_vbo(blocks_arr)
            self.texbo = Global.master.screen.create_vbo(textures_arr)
            #print(self.map[0])
        except IOError:
            pass
        
    def init_player(self,player):
        if len(self.player_init_pos) > 0:
            player.position = self.player_init_pos[0] # The values here will be overwritten by the player as they are used as references!!!!
            # To not overwrite them, use:
            #player.position = [ x for x in self.player_init_pos[0]]
        else:
            #player.position = [1.4, 1.4]
            player.position = [self.offset[0]+(self.width/2)*constants.blockScale, self.offset[1]+(self.height/2)*constants.blockScale]
        
    def get(self,x,y):
        x -= self.offset[0]
        y -= self.offset[1]
        if x < 0: return 1#self.outside[2]
        if x >= self.width: return 1#self.outside[0]
        if y < 0: return 1#self.outside[1]
        if y >= self.height: return 1#self.outside[3]
        try:
            return self.data[x,y]
        except:
            return 1
        
    def getFree(self,x,y):
        x -= self.offset[0]
        y -= self.offset[1]
        if x < 0: return 0#self.outside[2]
        if x >= self.width: return 0#self.outside[0]
        if y < 0: return 0#self.outside[1]
        if y >= self.height: return 0#self.outside[3]
        try:
            return self.data[x,y]
        except:
            return 1
        
    def checkLayerForward(self,x,y,w,h):
        xl = constants.trunc((x-w/2) / constants.blockScale)
        xr = constants.trunc((x+w/2) / constants.blockScale)
        yd = constants.trunc((y-h/2) / constants.blockScale)
        yu = constants.trunc((y+h/2) / constants.blockScale)
        for px,py in self.layer_forward_zones:
            if xl <= px and px <= xr and yd <= py and py <= yu:
                return True
        return False
        
    def checkLayerBackward(self,x,y,w,h):
        xl = constants.trunc((x-w/2) / constants.blockScale)
        xr = constants.trunc((x+w/2) / constants.blockScale)
        yd = constants.trunc((y-h/2) / constants.blockScale)
        yu = constants.trunc((y+h/2) / constants.blockScale)
        for px,py in self.layer_backward_zones:
            if xl <= px and px <= xr and yd <= py and py <= yu:
                return True
        return False
        
    def update(self,stage):
        for unit in self.units:
            unit.update(stage)
    
    def drawUnits(self,screen):
        for unit in self.units:
            unit.draw(screen)
            
    def drawVbo(self,screen):
        if self.vbo is not None:
            #screen.draw_vbo(self.vbo,self.vbo_vec_count,(0,0,self.layer*0.1))
            screen.draw_vbo_texture(self.textures[0][0],self.texbo,self.vbo,self.vbo_vec_count,(0,0,0))
            