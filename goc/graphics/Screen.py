# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 14:02:23 2019

@author: Phoenix
"""

import pygame

class Screen:
    
    def __init__(self, master):
        self.master = master
        
        self.active = False
        self.screen = None
        self.font = pygame.font.Font(None, 30)
        
    def create_window(self,size):
        self.size = size
        self.screen = pygame.display.set_mode(size, pygame.DOUBLEBUF)
        self.active = True
        
    def draw(self):
        self.screen.fill((0,0,0)) # Black
        ##self.screen.blit(ball, ballrect)
        
        self.master.draw(self)
            
        #Render Objects
        fps = self.font.render(str(int(self.master.clock.get_fps())), True, pygame.Color('white'))
        self.screen.blit(fps, (10, 10))
        
        pygame.display.flip()