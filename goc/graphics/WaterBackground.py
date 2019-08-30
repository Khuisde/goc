# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 15:37:14 2019

@author: Phoenix
"""

import math
import Global
from .Background import Background

class WaterBackground(Background):
    
    def __init__(self):
        
        self.images = ["image/Wasser_1.png",
                    "image/Wasser_2.png",
                    "image/Wasser_3.png",
                    "image/Wasser_4.png"]
        self.textures = []
        
        for i in self.images:
            index, width, height = Global.master.screen.loadImage(i)
            self.textures.append((index, width, height))
            
        # Image ID, Layer, X, Y, Degrees, Amplitude, Deg_Speed, img_x, img_y, rotation_ang, rotation_dir
        #self.water_coords=[[0,1,0,0,0,10,2,0,0,1,1,0.01],
        #                   [1,2,0,100,180,15,5,0,100,2,1,0.02],
        #                   [2,3,0,200,270,17,5,0,200,0,1,0.03],
        #                   [3,4,0,300,90,20,5,0,300,-1,1,0.04],
        #                   [0,5,0,400,45,20,5,0,400,-2,1,0.05]]
        #self.water_coords=[[0,1, -2,-1.1 ,0   ,0.010,2, 0,0 , 1,1,0.05],
        #                   [1,2, -2,-1.4 ,180 ,0.015,5, 0,0 , 2,1,0.04],
        #                   [2,3, -2,-1.7 ,270 ,0.017,5, 0,0 , 0,1,0.03],
        #                   [3,4, -2,-2.0 ,90  ,0.020,5, 0,0 ,-1,1,0.02],
        #                   [0,5, -2,-2.3 ,45  ,0.020,5, 0,0 ,-2,1,0.01]]
        self.water_coords=[[0,1, -2,-1.22 ,0   ,0.010,2, 0,0 , 1,1,0.05],
                           [1,2, -2,-1.49 ,180 ,0.015,5, 0,0 , 2,1,0.04],
                           [2,3, -2,-1.76 ,270 ,0.017,5, 0,0 , 0,1,0.03],
                           [3,4, -2,-2.03 ,90  ,0.020,5, 0,0 ,-1,1,0.02],
                           [0,5, -2,-2.30 ,45  ,0.020,5, 0,0 ,-2,1,0.01]]
        
    def update(self):
        for i in self.water_coords:
            i[4] = (i[4] + i[6]) % 360
            i[7] = i[2] + i[5] * math.cos(math.radians(i[4]))
            i[8] = i[3] + i[5] * math.sin(math.radians(i[4]))
            i[9] = i[9] + i[10] * 0.1
            if i[9] > 1.3 : i[10] = -0.5
            elif i[9] < -1.3 : i[10] = 0.5
        
        
    def draw(self,screen):
        screen.disableImageDepth()
        for part in self.water_coords:
            image_num = part[0]
            z = part[11]
            x = part[7] 
            y = part[8] 
            #x = part[7]/800. -0.5
            #y= -part[8]/600. -0.5
            w = 2
            h = 2
            rot = part[9]
            emission = None
            #if layer % 2 == 1: emission = (10,10,100,1) #(100,50,50,1)
            #else: emission = None
            
            screen.drawImagePartFixed(self.textures[image_num][0],x,y,z,w,h,(rot,0,0,1),(0,0),emission)
            screen.drawImagePartFixed(self.textures[image_num][0],x+w,y,z,w,h,(rot,0,0,1),(0,0),emission)
            #screen.drawImagePartFixed(self.textures[image_num][0],x-w,y,z,w,h,(rot,0,0,1),(0,0),emission)
            
            #screen.drawImagePartFixed(self.textures[image_num][0],x,y,z,w,h,(rot,0,0,1),(0,0),emission)
            #screen.drawImagePartFixed(self.textures[image_num][0],x-w,y,w,h,layer,(rot,0,0,1),(0,0),emission)#(x+w/2,y+h/2))
            #screen.drawImagePartFixed(self.textures[image_num][0],x+w,y,w,h,layer,(rot,0,0,1),(0,0),emission)#(x+w/2,y+h/2))
        screen.enableImageDepth()