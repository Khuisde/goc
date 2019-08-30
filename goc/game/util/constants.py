# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 22:52:30 2019

@author: Phoenix
"""

# Map Sizes
blockScale = 0.1
minScale = 0.001
#mue = 0.000001
mue = 0.00003

#Blocks
block_solid = 1
block_platform = 2
block_uphill = 3
block_downhill = 4
block_water = 5


# Physic
maxVelocity = 0.1 #0.2
minVelocity = 0.001

defaultFallGravity = -0.002

airFriction = 0.90
groundFriction = 0.80

# Player values
#jumpVelocity = 0.05
#runVelocity = 0.003
#airVelocity = 0.002

jumpVelocity = 0.03
runVelocity = 0.002
airVelocity = 0.0008

slowVelocity = 0.001

# Enemy values
enemyWalkVelocity = 0.0008
