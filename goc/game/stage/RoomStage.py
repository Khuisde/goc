# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 11:50:37 2019

@author: Phoenix
"""

from .Stage import Stage
from .Map import Map
from ..util import constants, physics

import Global

class RoomStage(Stage):
    
    def __init__(self):
        Stage.__init__(self)
        
        self.id = "Test Room Stage"
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
        
        self.width = 10 #20
        self.height = 4 #13
        self.depth = 4 #10
        
        
        # Default room size
        w = 10 * constants.blockScale
        h = 4 * constants.blockScale
        d = 4 * constants.blockScale
        self.rooms_values = [
                (0,0,w,h,d,[6,5,3,2,2],None),
                (w,0,w,h,d,[1,5,3,5,4],[(w/5,0,w*0.15,h*0.7,d*0.7,7)]),
                (w,h,w,h,d,[1,5,3,5,2],None),
                (w,2*h,w,h*1.5,d,[1,5,3,5,3],None),
                ]
        # The first array are the number of the textures
        # it's ordered: [bottom floor, right wall, top ceiling, left wall, back wall]
        # The numbers there are the indexes of the textures of self.images (5 is the door r_side_door.png)
        
        self.rooms = []
        self.maps = []
        self.current_room = 0
        
        self.room_transitions = [
                [0,[.99,0,.01,.4],1,[.05,0]],
                [1,[.01,0,.01,.4],0,[.95,0]],
                [1,[.99,0,.01,.4],2,[.95,0]],
                [2,[.01,0,.01,.4],3,[.05,0]],
                [2,[.99,0,.01,.4],1,[.95,0]],
                [3,[.01,0,.01,.4],2,[.05,0]],
                [3,[.99,0,.01,.4],"Test Tower Level",None],
                ]
        
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
        
        #self.map = Map.createEmpty(self.width,self.height)
        self.gen_room_coordinates()
        
    def gen_room_coordinates(self):        
        self.rooms = []
        self.maps = []
        for x,y,w,h,d,wall_textures,images in self.rooms_values:
            myroom = []
            coordinates = self.createRoom(w-constants.mue,h-constants.mue,d-constants.mue,wall_textures,dx=x,dy=y)
            if images is not None:
                for xi,yi,wi,hi,di,ti in images:
                    coordinates += self.createImage(xi,yi,wi,hi,di,ti)
            for c,tx in coordinates:
                vbo, vbo_count = Global.master.screen.create_vbo_3d(w,h,c)
                #self.room_vbos.append((w,h,vbo, vbo_count, tx))
                myroom.append((w, h, vbo, vbo_count, tx))
            self.rooms.append([x,y,w,h,myroom])
            self.maps.append(Map.createEmpty(constants.trunc(w/constants.blockScale),constants.trunc(h/constants.blockScale),[constants.trunc(x/constants.blockScale),constants.trunc(y/constants.blockScale)]))
        
        self.map = self.maps[0]
        #coordinates = self.createRoom(w,h,d,[6,5,3,2,2])
        #coordinates += self.createRoom(w,h,d,[1,2,3,5,4],dx=w+constants.mue)
        #coordinates += self.createImage(w/5,0,w*0.15,h*0.7,d*0.7,7)
        #       
        #for c,tx in coordinates:
        #    vbo, vbo_count = Global.master.screen.create_vbo_3d(w,h,c)
        #    self.room_vbos.append((w,h,vbo, vbo_count, tx))

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
        
        if self.player is not None:
            if self.player.temp_enter and self.player.temp_delay <= 0:
                for rid,[x,y,w,h],orid,oposition in self.room_transitions:
                    if rid == self.current_room:
                        crx,cry,crw,crh,cmyroom = self.rooms[self.current_room]
                        if physics.collision(self.player.position[0]-self.player.hitbox_size[0]/2,
                                             self.player.position[1]-self.player.hitbox_size[1]/2,
                                             self.player.hitbox_size[0],self.player.hitbox_size[1],
                                             x+crx,y+cry,w,h):
                            if type(orid) is str: # Level transition
                                # TODO
                                Global.master.game.transitionTo(orid)
                            else: # Room transition
                                # Move player to orid !
                                self.current_room = orid
                                rx,ry,rw,rh,myroom = self.rooms[self.current_room]
                                self.map = self.maps[self.current_room]
                                #self.player.vx = 0
                                if oposition[0] + rx > self.player.position[0] == self.player.velocity[0] < 0: self.player.velocity[0] *= -1 # Turn player if required
                                self.player.position[0] = oposition[0] + rx
                                self.player.position[1] = oposition[1] + ry + self.player.hitbox_size[1]/2
                                self.player.temp_enter = False
                                break
        
    def initViewport(self):
        Global.master.game.viewport = [self.default_viewport[0],self.default_viewport[1],self.default_viewport[2]]
        
    def setViewport(self):
        px,py,pz = Global.master.game.viewport
        crx,cry,crw,crh,cmyroom = self.rooms[self.current_room]
        shouldx, shouldy, shouldz = crx + crw/2, cry + crh/2, 1.4
        #px + (shouldx - px) * 2/3 = px*3/3-(px*2/3)+shouldx*2/3 = px/3 + cshouldx*2/3
        npx = px *2/3 + shouldx /3  
        npy = py *2/3 + shouldy /3
        npz = pz *2/3 + shouldz /3
        Global.master.game.viewport = [npx,npy,npz]
            
    def draw(self, screen):
            
        ##cur_room = self.rooms_values[self.current_room]
        ##screen.translate(-cur_room[0],-cur_room[1],0)
        
        #for box in self.room_vbos:
        for x,y,w,h,myroom in self.rooms:
            for box in myroom:
                screen.draw_vbo_pos(self.position,self.textures[box[4]][0],box[2],box[3])
        #screen.draw_vbo_pos((0,0,-0.4),self.textures[0][0],self.room_vbos[0][2],self.room_vbos[0][3])
        #screen.draw_vbo_pos((0,0,-0.4),self.textures[0][0],self.textures[0][3],self.textures[0][4]
        #if self.unordered_draw:
        #    screen.disableImageDepth()
        
        ##screen.popTranslation()
            
        if self.player is not None:
            self.player.draw(screen)
            
        #if self.unordered_draw:
        #    screen.enableImageDepth()