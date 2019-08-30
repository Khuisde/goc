# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 14:02:23 2019

@author: Phoenix
"""

import pygame, os
from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.arrays.vbo as glvbo

import numpy as np
import numpy.random as rdn

from PIL import Image

import Global

class Screen:
    
    def __init__(self):
        self.active = False
        self.screen = None
        
        self.text_texture_id = None
        self.text_texture_base = None

        self.deg = 1
        self.dir = 1
        self.side_rot = 0 # Test
        self.scale_factor = 1
        
        self.view_pos = [0,0,2]
        self.box_pos = [0,0]
        
        self.text_image_buffer = {}
        
        self.texture_imagelist = {}
        self.textures = []
        # Uses ctypes.c_void_p(12) to state that for texture the first 3 FLoats are skipped!
        marr = [ 0.2,    0.2,    0.1,      1,      1, # Top right
                 0.2,   -0.2,    0.1,      1,      0, # Bottom right
                -0.2,   -0.2,    0.1,      0,      0, # Bottom left
                -0.2,    0.2,    0.1,      0,      1] # Top left
        
        blocks_arr = np.array(marr,dtype=np.float32)
        self.blo_count = blocks_arr.shape[0]
        self.blo_vbo = self.create_vbo(blocks_arr)
        
        default_array = \
               [ 0.1,    0.1,    0.0,      1,      1, # Top right
                 0.1,   -0.1,    0.0,      1,      0, # Bottom right
                -0.1,   -0.1,    0.0,      0,      0, # Bottom left
                -0.1,    0.1,    0.0,      0,      1 ] # Top left
        
        default_arr = np.array(default_array,dtype=np.float32)
        self.default_count = default_arr.shape[0]
        self.default_vbo = self.create_vbo(default_arr)
        
        ###
        #print("Dir is ",Global.master.dir)
        ###
        
        
    def wall(self): 
        glBegin(GL_QUADS)
        glTexCoord2f(0,0)
        glVertex3f(-4,-4,-16)
        glTexCoord2f(0,1)
        glVertex3f(-4,4,-16)
        glTexCoord2f(1,1)
        glVertex3f(4,4,-8)
        glTexCoord2f(1,0)
        glVertex3f(4,-4,-8)
        glEnd()
        
    def block(self): 
        glBegin(GL_QUADS)
        glTexCoord2f(0,0)
        glVertex3f(-4,-4,-8)
        glTexCoord2f(0,1)
        glVertex3f(-4,4,-8)
        glTexCoord2f(1,1)
        glVertex3f(4,4,-8)
        glTexCoord2f(1,0)
        glVertex3f(4,-4,-8)
        glEnd()
        
    def blockRot(self): 
        self.deg+=0.05 * self.dir
        if self.deg > 3: self.dir = -1
        elif self.deg < -3: self.dir = 1
        glPushMatrix() # Put a new position + rotation on the stack
        glTranslate(0, 0, -8); # Set center
        glRotatef(self.deg, 0, 0, 1) # Set rotation
        glBegin(GL_QUADS)
        glTexCoord2f(0,0)
        glVertex3f(-4,-4,0)
        glTexCoord2f(0,1)
        glVertex3f(-4,4,0)
        glTexCoord2f(1,1)
        glVertex3f(4,4,0)
        glTexCoord2f(1,0)
        glVertex3f(4,-4,0)
        glEnd()
        glPopMatrix() # Remove the position + rotation again
        
    def cube(self):
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.verticies[vertex])
        glEnd()
        
#    def drawSphere(self):
#       glPushMatrix()
#       glTranslatef(2.0, 0.0, 0.0)
#       glMaterialfv(GL_FRONT, GL_AMBIENT, [0.1745, 0.0, 0.1, 0.0])
#       glMaterialfv(GL_FRONT, GL_DIFFUSE,[0.1, 0.0, 0.6, 0.0])
#       glMaterialfv(GL_FRONT, GL_SPECULAR,[0.7, 0.6, 0.8, 0.0])
#       glutSolidSphere(1, 35, 35)
#       glPopMatrix()
        
    #def drawText(position, textString):     
    #    font = pygame.font.Font (None, 64)
    #    textSurface = font.render("TEST", True, (255,255,255,255), (0,0,0,255))     
    #    textData = pygame.image.tostring(textSurface, "RGBA", True)     
    #    glRasterPos3d(*position)     
    #    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)
        
    def create_window(self,size):
        self.size = size
        self.screen = pygame.display.set_mode(size, pygame.DOUBLEBUF|pygame.OPENGL)
        
        #gluPerspective(45, (self.size[0]/self.size[1]), 0.1, 50.0)
        #glTranslatef(0.0,0.0, -5)
        self.scale_factor = self.size[0]/self.size[1]
        #glLoadIdentity()
        #gluPerspective(45, self.scale_factor, 0.05, 100)
        ##glTranslatef(0, 0, -1)
        #glTranslatef(0, 0, -2)
        self.see_side = False
        
        self.active = True
      
        
        self.light_image_id, width, height = self.loadImage(os.path.join(Global.master.dir,"image/Light.png"))
        
        glEnable(GL_DEPTH_TEST)         # Use Depth!
        glEnable(GL_TEXTURE_2D)         # Use Textures!
        glEnable(GL_COLOR_MATERIAL)     # Use Colors (combine with textures)
        glEnable(GL_BLEND);             # Use Transperency of images
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        #glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ONE);
        
        self.setupLight()
        self.init_text('image/font.png',20,34)
        
        ## TEST
        #glRotatef(70,0,1,0) # Set rotation
        #glTranslatef(0, 0, -5)
        
    def create_vbo(self,data):
        return glvbo.VBO(data)
    
    def create_image_vbo(self,w,h):
        #obj_array = \
        #       [ w/2,    h/2,    0.0,      1,      1, # Top right
        #         w/2,   -h/2,    0.0,      1,      0, # Bottom right
        #        -w/2,   -h/2,    0.0,      0,      0, # Bottom left
        #        -w/2,    h/2,    0.0,      0,      1 ] # Top left
        w = w / 320
        h = h / 320
        obj_array = \
               [ w,    h,    0.0,      1,      1, # Top right
                 w,    0,    0.0,      1,      0, # Bottom right
                 0,    0,    0.0,      0,      0, # Bottom left
                 0,    h,    0.0,      0,      1 ] # Top left
        textures_arr = np.array(obj_array,dtype=np.float32)
        vbo_vec_count = textures_arr.shape[0]
        vbo = glvbo.VBO(textures_arr)
        return vbo, vbo_vec_count
    
    def create_vbo_3d(self,w,h,obj_array):
        #w = w / 320
        #h = h / 320
        #obj_array = \
        #       [ w,    h,    0.0,      1,      1, # Top right
        #         w,    0,    0.0,      1,      0, # Bottom right
        #         0,    0,    0.0,      0,      0, # Bottom left
        #         0,    h,    0.0,      0,      1 ] # Top left
        textures_arr = np.array(obj_array,dtype=np.float32)
        vbo_vec_count = textures_arr.shape[0]
        vbo = glvbo.VBO(textures_arr)
        return vbo, vbo_vec_count
    
    def gotoLayer(self,x,y,z):
        glPushMatrix() # Put a new position + rotation on the stack
        glTranslate(x, y, z)
        
    def goLayerBack(self):
        glPopMatrix() # Remove the position + rotation again
    
    def init_text(self,filename,w=20,h=34,scale=0.4):
        #img = pygame.image.load(os.path.join(self.master.dir,filename))
        #width = img.get_width()
        #height = img.get_height()
        #textureData = pygame.image.tostring(img, "RGBA", 1)            
        
        img = Image.open(os.path.join(Global.master.dir,filename))
        textureData = np.array(img)
        width = img.width
        height = img.height
        
        self.text_texture_id = glGenTextures(1)
        
        glBindTexture(GL_TEXTURE_2D, self.text_texture_id)
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST) #GL_LINEAR)
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST) #GL_LINEAR)
        glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
        glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        
        #glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        glTexImage2D( GL_TEXTURE_2D, 0, GL_ALPHA, width, height, 0, GL_ALPHA, GL_UNSIGNED_BYTE, textureData )
    
    
        # Generate display lists
        dx, dy = w/float(width), h/float(height)
        self.text_texture_base = glGenLists(8*16)
        for i in range(8*16): # THE X AND Y COORDINATES ARE TOO BIG -> use -1 to 1 instead of 0 to width !!
            c = chr(i)
            x = i%16
            y = i//16-2
            glNewList(self.text_texture_base+i, GL_COMPILE)
            if (c == '\n'):
                glPopMatrix( )
                #glTranslatef( 0, -h, 0 )
                #glTranslatef( 0, h, 0 )
                glTranslatef( 0, dy*scale, 0 )
                glPushMatrix( )
            elif (c == '\t'):
                #glTranslatef( 4*w, 0, 0 )
                glTranslatef( 4*dx*scale, 0, 0 )
            elif (i >= 32):
                glBegin( GL_QUADS )
                #glTexCoord2f( (x  )*dx, (y+1)*dy ), glVertex( 0, h ) # -height
                #glTexCoord2f( (x  )*dx, (y  )*dy ), glVertex( 0, 0 )
                #glTexCoord2f( (x+1)*dx, (y  )*dy ), glVertex( w, 0 )
                #glTexCoord2f( (x+1)*dx, (y+1)*dy ), glVertex( w, h ) # -height
                glTexCoord2f( (x  )*dx, (y  )*dy ), glVertex( 0, dy*scale ) # -height
                glTexCoord2f( (x  )*dx, (y+1)*dy ), glVertex( 0, 0 )
                glTexCoord2f( (x+1)*dx, (y+1)*dy ), glVertex( dx*scale, 0 )
                glTexCoord2f( (x+1)*dx, (y  )*dy ), glVertex( dx*scale, dy*scale ) # -height
                glEnd( )
                #glTranslatef( w, 0, 0 )
                glTranslatef( dx*scale, 0, 0 )
            glEndList( )
            
    def setupLight(self):
        self.lightx, self.lighty, self.lightz = -0.6, 0.06 , 0.9 #0, -1, 0
        #self.brightness = -0.8
        self.brightness = 5 #-0.5 #1
        #glLightfv( GL_LIGHT1, GL_AMBIENT, GLfloat_4(0.2, .2, .2, 1.0) );
        #glLightfv(GL_LIGHT1, GL_DIFFUSE, GLfloat_3(.8,.8,.8));
        #glLightfv(GL_LIGHT1, GL_POSITION, GLfloat_4(-2,0,3,1) );
        glLightfv( GL_LIGHT1, GL_AMBIENT, GLfloat_4(1, 1, 1, 1.0) ); # Color + Transparency
        glLightfv(GL_LIGHT1, GL_DIFFUSE, GLfloat_3(self.brightness,self.brightness,self.brightness)); # Brightness
        glLightfv(GL_LIGHT1, GL_POSITION, GLfloat_4(self.lightx, self.lighty, self.lightz,1.0) ); # Position
        
        
        #glLightfv( GL_LIGHT2, GL_AMBIENT, GLfloat_4(1, 1, 1, 1.0) ); # Color + Transparency
        #glLightfv(GL_LIGHT2, GL_DIFFUSE, GLfloat_3(0.5,0.5,0.5)); # Brightness
        #glLightfv(GL_LIGHT2, GL_POSITION, GLfloat_4(0,0,0,1.0) ); # Position
        
        glEnable( GL_LIGHTING )
        glDisable(GL_LIGHT0);
        glEnable(GL_LIGHT1);
        #glEnable(GL_LIGHT2);
    
    def loadImage(self,img_path):
        if img_path in self.texture_imagelist:
            return self.texture_imagelist[img_path]
        img = pygame.image.load(os.path.join(Global.master.dir,img_path))
        textureData = pygame.image.tostring(img, "RGBA", 1)            
        tex = glGenTextures(1)
    
        width = img.get_width()
        height = img.get_height()
        
        glBindTexture(GL_TEXTURE_2D, tex)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST) #GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST) #GL_LINEAR)
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        
        self.textures.append(tex)
        index = len(self.textures)-1
        self.texture_imagelist[img_path] = [index, width, height]
        
        return index, width, height
        
        
    def loadImageOther(self, image):
        textureSurface = pygame.image.load(image)
    
        textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    
        width = textureSurface.get_width()
        height = textureSurface.get_height()
    
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA,
            GL_UNSIGNED_BYTE, textureData)

        return texture, width, height
    
    
    def enableImageDepth(self):
        glEnable(GL_DEPTH_TEST)
        
    def disableImageDepth(self):
        glDisable(GL_DEPTH_TEST)
            
    def directStart(self):
        glDisable(GL_TEXTURE_2D)
        #glRotatef(10,0,0,1)
        
    def directEnd(self):
        glColor3fv((1,1,1))
        #glRotatef(-10,0,0,1)
        glEnable(GL_TEXTURE_2D)
    
    def drawImage(self, texture, x, y, z, w, h):
        #glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.textures[texture])
        glBegin(GL_QUADS)
        glTexCoord2f(0,0)
        glVertex3f(x,y,z)
        glTexCoord2f(0,1)
        glVertex3f(x,y+h,z)
        glTexCoord2f(1,1)
        glVertex3f(x+w,y+h,z)
        glTexCoord2f(1,0)
        glVertex3f(x+w,y,z)
        glEnd() 
    
    def drawImageSimple(self, texture, x, y, w, h, layer):
        #glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.textures[texture])
        glBegin(GL_QUADS)
        glTexCoord2f(0,0)
        glVertex3f(x,y,-0.1*layer)
        glTexCoord2f(0,1)
        glVertex3f(x,y+h,-0.1*layer)
        glTexCoord2f(1,1)
        glVertex3f(x+w,y+h,-0.1*layer)
        glTexCoord2f(1,0)
        glVertex3f(x+w,y,-0.1*layer)
        glEnd()
        
    def drawImageSimpleRot(self, texture, x, y, w, h, layer, rot, rot_center=None, emission=None):
        if x+w < -1 or x > 1 or y+h < -1 or y > 1: return
        #glActiveTexture(GL_TEXTURE1)
        glPushMatrix() # Put a new position + rotation on the stack
        #glLoadIdentity()
        #if self.side_rot != 0:
        #    glRotatef(self.side_rot,0,1,0)
        #    glPushMatrix() # Put a new position + rotation on the stack
        if not rot_center:
            glTranslate(x+w/2., y+h/2., 0.1*layer); # Set center
        else:
            glTranslate(rot_center[0], rot_center[1], 0.1*layer); # Set center
        glRotatef(rot[0], rot[1], rot[2], rot[3]) # Set rotation
        glBindTexture(GL_TEXTURE_2D, self.textures[texture])
        
        #glMaterialfv(GL_FRONT, GL_DIFFUSE, (0,0.8,0.8,1))
        #glMaterialfv(GL_FRONT, GL_SPECULAR, (0.8,0.8,0.8,1))
        #glMaterialfv(GL_FRONT, GL_SHININESS, 50)
        #glMaterialfv(GL_FRONT, GL_SHININESS, 100)
        if emission == None: glMaterialfv(GL_FRONT, GL_EMISSION, 0)
        else: glMaterialfv(GL_FRONT, GL_EMISSION, emission) #(10,10,100,1)
        
        glBegin(GL_QUADS)
        glTexCoord2f(0,0)
        glVertex3f(x,y,0.1*layer)
        glTexCoord2f(0,1)
        glVertex3f(x,y+h,0.1*layer)
        glTexCoord2f(1,1)
        glVertex3f(x+w,y+h,0.1*layer)
        glTexCoord2f(1,0)
        glVertex3f(x+w,y,0.1*layer)
        glEnd()
        glPopMatrix() # Remove the position + rotation again
        #if self.side_rot != 0:
        #    glPopMatrix() # Remove the position + rotation again
        
    #def drawImagePartFixed(self, texture, x, y, w, h, layer, rot, rot_center=(0,0), emission=None, horizontal_fixed=False, vertical_fixed=False):
    def drawImagePartFixed(self, texture, x, y, z, w, h, rot, rot_center=(0,0), emission=None, horizontal_fixed=False, vertical_fixed=False):
        #if x+w < -1 or x > 1 or y+h < -1 or y > 1: return
        if x+w < -2 or x > 2 or y+h < -2 or y > 2: return
        glPushMatrix() # Put a new position + rotation on the stack
        # z = layer*0.1
        #if not rot_center:
        #    glTranslate(x+w/2., y+h/2., 0.1*layer); # Set center
        #else:
        glTranslate(rot_center[0], rot_center[1], z); # Set center
        glTranslatef(self.view_pos[0], self.view_pos[1], self.view_pos[2]-2)
        glRotatef(rot[0], rot[1], rot[2], rot[3]) # Set rotation
        glBindTexture(GL_TEXTURE_2D, self.textures[texture])
        
        if emission == None: glMaterialfv(GL_FRONT, GL_EMISSION, 0)
        else: glMaterialfv(GL_FRONT, GL_EMISSION, emission) #(10,10,100,1)
        
        
        glBegin(GL_QUADS)
        glTexCoord2f(0,0)
        glVertex3f(x,y,z)
        glTexCoord2f(0,1)
        glVertex3f(x,y+h,z)
        glTexCoord2f(1,1)
        glVertex3f(x+w,y+h,z)
        glTexCoord2f(1,0)
        glVertex3f(x+w,y,z)
        glEnd()
        glPopMatrix() # Remove the position + rotation again
        
    def drawColorRect(self, color, x, y, w, h, layer, rot=None, rot_center=None, emission=None):
        if x+w < -1 or x > 1 or y+h < -1 or y > 1: return
        if rot is not None:
            glPushMatrix() # Put a new position + rotation on the stack
            if not rot_center:
                glTranslate(x+w/2., y+h/2., 0.1*layer); # Set center
            else:
                glTranslate(rot_center[0], rot_center[1], 0.1*layer); # Set center
            glRotatef(rot[0], rot[1], rot[2], rot[3]) # Set rotation
        
        if emission == None: glMaterialfv(GL_FRONT, GL_EMISSION, 0)
        else: glMaterialfv(GL_FRONT, GL_EMISSION, emission) #(10,10,100,1)
        
        glDisable(GL_TEXTURE_2D)
        glColor3fv(color)
        #glRectf(x, y, x+w, y+h)
        glBegin(GL_QUADS)
        glTexCoord2f(0,0)
        glVertex3f(x,y,0.1*layer)
        glTexCoord2f(0,1)
        glVertex3f(x,y+h,0.1*layer)
        glTexCoord2f(1,1)
        glVertex3f(x+w,y+h,0.1*layer)
        glTexCoord2f(1,0)
        glVertex3f(x+w,y,0.1*layer)
        glEnd()
        glEnable(GL_TEXTURE_2D)  
        glColor3fv((1,1,1))
        
        if rot is not None:
            glPopMatrix() # Remove the position + rotation again
            
    def directDrawColorRect(self, color, x, y, w, h, layer):
        if x+w < -1.12 or x > 1.12 or y+h < -0.85 or y > 0.85: return
        glColor3fv(color)
        glRectf(x, y, x+w, y+h)
#        glBegin(GL_QUADS)
#        glTexCoord2f(0,0)
#        glVertex3f(x,y,0.1*layer)
#        glTexCoord2f(0,1)
#        glVertex3f(x,y+h,0.1*layer)
#        glTexCoord2f(1,1)
#        glVertex3f(x+w,y+h,0.1*layer)
#        glTexCoord2f(1,0)
#        glVertex3f(x+w,y,0.1*layer)
#        glEnd()
        
    def directDrawColorRectNorm(self, color, x, y, w, h, layer):
        if x+w < -1 or x > 1 or y+h < -1 or y > 1: return
        glColor3fv(color)
        #glRectf(x, y, x+w, y+h)
        glBegin(GL_QUADS)
        glTexCoord2f(0,0)
        glVertex3f(x,y,0.1*layer)
        glTexCoord2f(0,1)
        glVertex3f(x,y+h,0.1*layer)
        glTexCoord2f(1,1)
        glVertex3f(x+w,y+h,0.1*layer)
        glTexCoord2f(1,0)
        glVertex3f(x+w,y,0.1*layer)
        glEnd()
        
    def draw_img(self, texture, x, y, w, h, layer, rot, rot_center=None, emission=None):
        #if x+w < -1 or x > 1 or y+h < -1 or y > 1: return
        #glActiveTexture(GL_TEXTURE1)
        glPushMatrix() # Put a new position + rotation on the stack
        #glLoadIdentity()
        #if self.side_rot != 0:
        #    glRotatef(self.side_rot,0,1,0)
        #    glPushMatrix() # Put a new position + rotation on the stack
        
        #if not rot_center:
        #    glTranslate(x+w/2., y+h/2., 0.1*layer); # Set center
        #else:
        #    glTranslate(rot_center[0], rot_center[1], 0.1*layer); # Set center
        #glRotatef(rot[0], rot[1], rot[2], rot[3]) # Set rotation
        
        glBindTexture(GL_TEXTURE_2D, self.textures[texture])
        
        #glMaterialfv(GL_FRONT, GL_DIFFUSE, (0,0.8,0.8,1))
        #glMaterialfv(GL_FRONT, GL_SPECULAR, (0.8,0.8,0.8,1))
        #glMaterialfv(GL_FRONT, GL_SHININESS, 50)
        #glMaterialfv(GL_FRONT, GL_SHININESS, 100)
        if emission == None: glMaterialfv(GL_FRONT, GL_EMISSION, 0)
        else: glMaterialfv(GL_FRONT, GL_EMISSION, emission) #(10,10,100,1)
        
        glTexCoord2f(0,0)
        glRectf(x, y, x+w, y+h)
        glPopMatrix() # Remove the position + rotation again
        #if self.side_rot != 0:
        #    glPopMatrix() # Remove the position + rotation again
        
    def draw_vbo(self, vbo, count, pos=None):
        glDisable(GL_TEXTURE_2D)
        if pos is not None:
           glPushMatrix()
           glTranslatef(pos[0],pos[1],pos[2])
           
        #glOrtho(-1, 1, 1, -1, -1, 1)
        #glMatrixMode(GL_PROJECTION)
        #glLoadIdentity()
        vbo.bind()
        glColor(0,0,0)
        
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(2, GL_FLOAT, 0, vbo)
        glDrawArrays( GL_TRIANGLES, 0, count)
        
        glColor(1,1,1)
        glDisableClientState(GL_VERTEX_ARRAY)
        glEnable(GL_TEXTURE_2D)
        if pos is not None:
           glPopMatrix()
        
    def draw_vbo_texture(self, texture, texbo, vbo, count, pos=None):
        glBindTexture(GL_TEXTURE_2D, self.textures[texture])
        #glDisable(GL_TEXTURE_2D)
        if pos is not None:
           glPushMatrix()
           glTranslatef(pos[0],pos[1],pos[2])
           
        #glOrtho(-1, 1, 1, -1, -1, 1)
        #glMatrixMode(GL_PROJECTION)
        #glLoadIdentity()
        vbo.bind()
        #glColor(0,0,0)
        
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)
        glTexCoordPointer(2, GL_FLOAT, 0, texbo)
        glVertexPointer(2, GL_FLOAT, 0, vbo)
        glDrawArrays( GL_TRIANGLES, 0, count)
        
        #glColor(1,1,1)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
        #glEnable(GL_TEXTURE_2D)
        if pos is not None:
           glPopMatrix()
        
    def draw_vbo_tex(self, texture, vbo, count):
        vbo.bind()
        glColor(1,1,0)
        
        glBindTexture(GL_TEXTURE_2D, self.textures[texture])
        glBindBuffer(GL_ARRAY_BUFFER, vbo);
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        
        glTexCoordPointer(2, GL_FLOAT, 20, ctypes.c_void_p(12)); # 5*4, 3*4
        
        #glVertexPointer(3, GL_FLOAT, 16, None); # !! Size of GL_FLOAT = 4, this is Num_elements * 4
        #glVertexPointer(3, GL_FLOAT, 20, None); # !! Size of GL_FLOAT seems to be 16
        glVertexPointer(3, GL_FLOAT, 20, self.default_vbo);
        
        glDrawArrays( GL_QUADS, 0, 4)
        #glDrawArrays( GL_TRIANGLES, 0, 3) #GL_TRIANGLES
        
        glColor(1,1,1)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        
    def draw_vbo_pos(self, position, texture, vbo, count):
        glPushMatrix() # Put a new position + rotation on the stack
        vbo.bind()
        glTranslate(position[0],position[1],position[2])
        #glColor(1,1,1)
        
        glBindTexture(GL_TEXTURE_2D, self.textures[texture])
        glBindBuffer(GL_ARRAY_BUFFER, vbo);
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        
        glTexCoordPointer(2, GL_FLOAT, 20, ctypes.c_void_p(12)); # 5*4, 3*4
        #glVertexPointer(3, GL_FLOAT, 16, None); # !! Size of GL_FLOAT = 4, this is Num_elements * 4
        #glVertexPointer(3, GL_FLOAT, 20, None); # !! Size of GL_FLOAT seems to be 16
        glVertexPointer(3, GL_FLOAT, 20, None); #self.default_vbo);
        
        glDrawArrays( GL_QUADS, 0, 4)
        #glDrawArrays( GL_TRIANGLES, 0, 3) #GL_TRIANGLES
        
        #glColor(1,1,1)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glPopMatrix() # Remove the position + rotation again
        
    def draw_default(self, texture, x, y, z):
        glPushMatrix() # Put a new position + rotation on the stack
        self.default_vbo.bind()
        glColor(1,1,1)
        glTranslate(x, y, z)
        
        glBindTexture(GL_TEXTURE_2D, self.textures[texture])
        glBindBuffer(GL_ARRAY_BUFFER, self.default_vbo);
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        
        glTexCoordPointer(2, GL_FLOAT, 20, ctypes.c_void_p(12)); # 5*4, 3*4
        
        #glVertexPointer(3, GL_FLOAT, 16, None); # !! Size of GL_FLOAT = 4, this is Num_elements * 4
        #glVertexPointer(3, GL_FLOAT, 20, None); # !! Size of GL_FLOAT seems to be 16
        glVertexPointer(3, GL_FLOAT, 20, self.default_vbo);
        
        glDrawArrays( GL_QUADS, 0, 4)
        #glDrawArrays( GL_TRIANGLES, 0, 3) #GL_TRIANGLES
        
        glColor(1,1,1)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glPopMatrix() # Remove the position + rotation again
        
    def draw_default_rot(self, texture, x, y, z, rot):
        glPushMatrix() # Put a new position + rotation on the stack
        self.default_vbo.bind()
        glColor(1,1,1)
        glTranslate(x, y, z)
        glRotatef(rot[0], rot[1], rot[2], rot[3])
        glBindTexture(GL_TEXTURE_2D, self.textures[texture])
        glBindBuffer(GL_ARRAY_BUFFER, self.default_vbo);
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        
        glTexCoordPointer(2, GL_FLOAT, 20, ctypes.c_void_p(12)); # 5*4, 3*4
        
        #glVertexPointer(3, GL_FLOAT, 16, None); # !! Size of GL_FLOAT = 4, this is Num_elements * 4
        #glVertexPointer(3, GL_FLOAT, 20, None); # !! Size of GL_FLOAT seems to be 16
        glVertexPointer(3, GL_FLOAT, 20, self.default_vbo);
        
        glDrawArrays( GL_QUADS, 0, 4)
        #glDrawArrays( GL_TRIANGLES, 0, 3) #GL_TRIANGLES
        
        glColor(1,1,1)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glPopMatrix() # Remove the position + rotation again
        
    def draw_default_rot_scaled(self, texture, x, y, z, rot, scale):
        glPushMatrix() # Put a new position + rotation on the stack
        self.default_vbo.bind()
        glColor(1,1,1)
        glScaled(scale[0],scale[1],1)
        glTranslate(x/scale[0], y/scale[1], z)
        #glTranslate(x, y, z)
        glRotatef(rot[0], rot[1], rot[2], rot[3])
        glBindTexture(GL_TEXTURE_2D, self.textures[texture])
        glBindBuffer(GL_ARRAY_BUFFER, self.default_vbo);
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        
        glTexCoordPointer(2, GL_FLOAT, 20, ctypes.c_void_p(12)); # 5*4, 3*4
        
        #glVertexPointer(3, GL_FLOAT, 16, None); # !! Size of GL_FLOAT = 4, this is Num_elements * 4
        #glVertexPointer(3, GL_FLOAT, 20, None); # !! Size of GL_FLOAT seems to be 16
        glVertexPointer(3, GL_FLOAT, 20, self.default_vbo);
        
        glDrawArrays( GL_QUADS, 0, 4)
        #glDrawArrays( GL_TRIANGLES, 0, 3) #GL_TRIANGLES
        
        glColor(1,1,1)
        glScaled(1,1,1)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glPopMatrix() # Remove the position + rotation again
    
    
            
    def drawText(self, position, textString):
        glPushMatrix( )
        
        ##glEnable( GL_DEPTH_TEST )
        ##glEnable( GL_BLEND ) # IMPORTANT!
        ##glEnable( GL_COLOR_MATERIAL )
        
        #glEnable( GL_TEXTURE_2D )
        
        #glOrtho(0, self.size[0], self.size[1], 0, -1, 1)
        glLoadIdentity()
        #glViewport( 0, 0, self.size[0], self.size[1] )
        #glTranslate( -1, -1920/1080, 0 )
        glTranslate( -1+position[0], -1+position[1], 0 ) 
        ##
        #TODO : Something is wrong, this should be equal to -1/self.scale, but is not
        ##
        
        #glClearColor(1,1,1,1)
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBindTexture( GL_TEXTURE_2D, self.text_texture_id )
        #glColor(0,0,0,1)
        #glColor(1,1,1,1)
        glPushMatrix( )
        glListBase( self.text_texture_base )
        glCallLists( [ord(c) for c in textString] )
        glPopMatrix( )
        #glColor(0,0,0,1)
        
        #glDisable( GL_TEXTURE_2D )
        #glDisable( GL_BLEND ) 
        
        glPopMatrix( )
        
    
    # Heck this is inefficient!!!
    def drawText_old(self, position, textString):  
        if textString in self.text_image_buffer:
            textData, width, height = self.text_image_buffer[textString]
            glRasterPos3d(*position)
            glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, textData)
        else:
            font = pygame.font.Font (None, 64)
            textSurface = font.render(textString, True, (255,255,255,255), (0,0,0,255))     
            textData = pygame.image.tostring(textSurface, "RGBA", True)
            width, height = textSurface.get_width(), textSurface.get_height()
            self.text_image_buffer[textString] = textData, width, height
            glRasterPos3d(*position)
            glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, textData)

    
    def draw(self):
        #self.screen.fill((0,0,0)) # Black
        #self.screen.blit(ball, ballrect)
        
        glClearColor(0,0,0,255)
        #glClearColor(1,1,1,255)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        keys=pygame.key.get_pressed()
        #if keys[pygame.K_LEFT]:
        #    #self.lightx -= 0.01
        #    #self.box_pos[0] -= 0.01
        #    self.view_pos[0] -= 0.01
        #if keys[pygame.K_RIGHT]:
        #    #self.lightx += 0.01
        #    #self.box_pos[0] += 0.01
        #    self.view_pos[0] += 0.01
        #if keys[pygame.K_UP]:
        #    #self.lighty += 0.01
        #    #self.box_pos[1] += 0.01
        #    self.view_pos[1] += 0.01
        #if keys[pygame.K_DOWN]:
        #    #self.lighty -= 0.01
        #    #self.box_pos[1] -= 0.01
        #    self.view_pos[1] -= 0.01
        ##if keys[pygame.K_a]:
        ##    self.lightz += 0.01
        ##if keys[pygame.K_s]:
        ##    self.lightz -= 0.01
        
        #if keys[pygame.K_1]:
        #    self.brightness += 0.1
        #if keys[pygame.K_2]:
        #    self.brightness -= 0.1
        
        if keys[pygame.K_n]:
            self.view_pos[2] -= 0.01
        if keys[pygame.K_m]:
            self.view_pos[2] += 0.01
            
        if keys[pygame.K_c]:
            self.side_rot -= 0.5
        if keys[pygame.K_v]:
            self.side_rot += 0.5
        if keys[pygame.K_b]:
            self.side_rot = 0
        if keys[pygame.K_j]:
            print(self.view_pos)
            
        #if keys[pygame.K_x]:
        #    print(self.view_pos)
         
        glLoadIdentity()
        gluPerspective(45, self.scale_factor, 0.05, 100)
        #gluPerspective(45, 1920/1080, 0.05, 100)
        
        glRotatef(self.side_rot,0,1,0)
        #glRotatef(self.side_rot,0,1,0)
        #glTranslatef(0, 0, -5)
        #glTranslatef(0, 0, -2)
        
        #self.view_pos
        glTranslatef(-self.view_pos[0], -self.view_pos[1], -self.view_pos[2])
            
        #if keys[pygame.K_z]:
        #    print(self.lightx,self.lighty,self.lightz,self.brightness)
                
                
        glLightfv(GL_LIGHT1, GL_AMBIENT, GLfloat_4(1, 1, 1, 1.0) ); # Color + Transparency
        glLightfv(GL_LIGHT1, GL_DIFFUSE, GLfloat_3(self.brightness,self.brightness,self.brightness)); # Brightness
        glLightfv(GL_LIGHT1, GL_POSITION, GLfloat_4(self.lightx, self.lighty, self.lightz,1.0) ); # Position
        
        if True:
            Global.master.draw(self) # MAIN DRAW LOOP, VERY IMPORTANT!!!
        
        if keys[pygame.K_x]:
            glLoadIdentity()
            #glTranslatef(0,0, -self.view_pos[2])
            for x in range(20):
                for y in range(20):
                    glRotatef(0.1,0,0,1)
                    self.drawText((x*0.095-1,y*0.095-1,-1),str(x)+","+str(y))
                    
        self.drawText((0,0),"Dies ist ein TEEEEEST!")
        self.drawText((0,0.1),"Zweite Zeile nach oben")
        self.drawText((0.2,0.2),"Dritte Zeile HOCH...")
        
        #self.drawImage(self.light_image_id,self.lightx, self.lighty, self.lightz-0.01,1,1)
        
        #self.drawColorRect((1,0,0),self.box_pos[0], self.box_pos[1], 0.2, 0.2, 1)
        #self.draw_img(self.light_image_id,self.box_pos[0], self.box_pos[1], 0.2, 0.2, 1, (0,0,0,0))
        
        # Draw a colored rectangle, fast
        #self.draw_vbo(self.blo_fvbo,self.blo_fcount)
        
        #########################################
        # Draw a textured rectangle, fast
        #self.draw_vbo_tex(self.light_image_id,self.blo_vbo,self.blo_count)
        #########################################
        
        #glRotatef(1, 3, 1, 1)
        #glRotatef(1, 1, 1, 1)
        
        #self.cube()
        #self.wall()
        #self.block()
        
        ##glActiveTexture(GL_TEXTURE1)
        #glBindTexture(GL_TEXTURE_2D, self.Texture1)
        ##glBindTexture(GL_TEXTURE_2D, self.Texture1)
        #self.blockRot()
        
        ##glActiveTexture(GL_TEXTURE0)
        ##glBindTexture(GL_TEXTURE_2D, self.Texture2)
        #self.drawImageSimple(self.Texture2,-.5,-.6,1,1,4)
        #self.drawImageSimple(self.Texture3,-.5,-.7,1,1,3)
        #self.drawImageSimple(self.Texture4,-.5,-.8,1,1,2)
        
        #pygame.time.wait(10)
            
        #Render Objects
        #fps = self.font.render(str(int(self.master.clock.get_fps())), True, pygame.Color('white'))
        #self.screen.blit(fps, (10, 10))
        
        pygame.display.flip()