# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 14:01:13 2019

@author: Phoenix
"""

import os,sys,inspect,random
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
superdir = os.path.dirname(currentdir)
if not currentdir in sys.path:
    sys.path.insert(0,currentdir)
if not superdir in sys.path:
    sys.path.insert(0,superdir)

from graphics.ScreenGL import Screen
from game.Game import Game
import pygame

class Master:
    
    def __init__(self, args=None):
        
        self.id = str(random.random())
        self.dir = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
        self.arguments = args
             
    def init(self):
        pygame.init()
        
        try:
            
            self.screen = Screen()
            #self.screen.create_window((800,600)) #(1024,768))
            self.screen.create_window((1920,1080)) #(1024,768))
            
            self.game = Game()
            self.game.init()
            self.clock = pygame.time.Clock()
            
            self.continue_mainloop = True
            self.state = 0 # Main Menu / Game / etc
            
        except Exception as err:
             pygame.quit()
             raise err
        
    def quit(self):
        print("Quitting")
        self.continue_mainloop = False
        
    def main(self):
    
        try:
        
            # Main game Loop
            while self.continue_mainloop:
                
                self.update()
                
            pygame.quit()
            
        except Exception as err:
             pygame.quit()
             raise err

    def update(self):
        self.evaluate_events()
                
        # Do something
        if self.state == 0:
            self.game.update()
            
        if self.screen.active:
            self.screen.draw()
            
        self.clock.tick(60)
            
    def draw(self,screen):
        if self.game:
            self.game.draw(screen)
            
    def evaluate_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                self.continue_mainloop = False;
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o: # Layer up
                    self.game.playerLayerUp()
                if event.key == pygame.K_p: # Layer down
                    self.game.playerLayerDown()
                if event.key == pygame.K_q: # QUIT
                    self.continue_mainloop = False
                