# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 22:42:28 2019

@author: Phoenix
"""

from . import constants
import math

# physicstate:
# -1 - NONE
# 0 - fall
# 1 - ground
# 2 - climb
# 3 - fly
# ...

def orArray(x,y):
    res = []
    for i in range(len(x)):
        res.append(x[i] or y[i])
    return res

def collision(x,y,w,h,ox,oy,ow,oh):
    return x+w >= ox and x <= ox+ow and y+h >= oy and y <= oy+oh

# pos, velocity, size will overwrite values
def apply(pos,velocity,size,physicstate,map):
    if (abs(velocity[0]) > constants.maxVelocity): velocity[0] = math.copysign(constants.maxVelocity,velocity[0])
    if (abs(velocity[1]) > constants.maxVelocity): velocity[1] = math.copysign(constants.maxVelocity,velocity[1])
    if physicstate < 0: return pos,velocity,physicstate,[False,False,False,False,False]
    elif physicstate == 0: return calcFallPhysics(pos,velocity,size,physicstate,map)
    elif physicstate == 1: return calcGroundPhysics(pos,velocity,size,physicstate,map)
    elif physicstate == 2: return calcClimbPhysics(pos,velocity,size,physicstate,map)
    elif physicstate == 3: return calcFlyPhysics(pos,velocity,size,physicstate,map)
    else: return pos,velocity,physicstate,[False,False,False,False,False]


def calcFallPhysics(pos,velocity,size,physicstate,map):
    wallhit = [False,False,False,False,False]
    # 0 = right, 1 = top, 2 = left, 3 = bot, 4 = center
    
    if velocity[0] != 0 or velocity[1] != 0:
        tvx = velocity[0]
        tvy = velocity[1]
        while (abs(tvx) > constants.blockScale) or (abs(tvy) > constants.blockScale):
            # separate move in parts
            vx, vy = 0, 0
            if abs(tvx) > abs(tvy) :
                vx = math.copysign(constants.blockScale,tvx)
                if tvy != 0 : vy = tvx*vx/tvy
            else:
                vy = math.copysign(constants.blockScale,tvy)
                if tvx != 0 : vx = tvy*vy/tvx
            tvx -= vx
            tvy -= vy
            pos, [vxr,vyr], physicstate, wallhit_new = movePartialSized(pos,[vx,vy],size,physicstate,map)
            wallhit = orArray(wallhit,wallhit_new)
            if vx != vxr: 
                velocity[0] = 0 # Hit wall LR
                tvx = 0
            if vy != vyr: 
                velocity[1] = 0 # Hit wall UD
                tvy = 0
                if vy < 0: physicstate = 1 # Hit ground
            
        pos, velocity, physicstate, wallhit_new = movePartialSized(pos,velocity,size,physicstate,map)
        wallhit = orArray(wallhit,wallhit_new)
    
    #if physicstate == 0:
    velocity[1] += constants.defaultFallGravity
    velocity[0] *= constants.airFriction
    
    if abs(velocity[0]) < constants.minVelocity : velocity[0] = 0
    if abs(velocity[1]) < constants.minVelocity : velocity[1] = 0
    
    return pos,velocity,physicstate,wallhit


def calcGroundPhysics(pos,velocity,size,physicstate,map):
    wallhit = [False,False,False,False,False]
    # 0 = right, 1 = top, 2 = left, 3 = bot, 4 = center
    physicstate = 0
   
    if velocity[0] != 0 or velocity[1] != 0:
        tvx = velocity[0]
        tvy = velocity[1]
        while (abs(tvx) > constants.blockScale) or (abs(tvy) > constants.blockScale):
            # separate move in parts
            vx, vy = 0, 0
            if abs(tvx) > abs(velocity[1]) :
                vx = math.copysign(constants.blockScale,tvx)
                if tvy != 0 : vy = tvx*vx/tvy
            else:
                vy = math.copysign(constants.blockScale,tvy)
                if tvx != 0 : vx = tvy*vy/tvx
            tvx -= vx
            tvy -= vy
            pos, [vxr,vyr], physicstate, wallhit_new = movePartialSized(pos,[vx,vy],size,physicstate,map)
            wallhit = orArray(wallhit,wallhit_new)
            if wallhit < 0: wallhit = wallhit_new
            if vx != vxr: 
                velocity[0] = 0 # Hit wall LR
            if vy != vyr: 
                velocity[1] = 0 # Hit wall UD
                if vy > 0: physicstate = 1 # Hit ground
            
        pos, velocity, physicstate, wallhit_new = movePartialSized(pos,velocity,size,physicstate,map)
        wallhit = orArray(wallhit,wallhit_new)
    
    velocity[1] += constants.defaultFallGravity
    velocity[0] *= constants.groundFriction
    
    return pos,velocity,physicstate,wallhit


def calcClimbPhysics(pos,velocity,size,physicstate,map):
    wallhit = [False,False,False,False,False]
    # 0 = right, 1 = top, 2 = left, 3 = bot, 4 = center
    return pos,velocity,physicstate,wallhit



def calcFlyPhysics(pos,velocity,size,physicstate,map):
    wallhit = [False,False,False,False,False]
    # 0 = right, 1 = top, 2 = left, 3 = bot, 4 = center
    return pos,velocity,physicstate,wallhit



##########
    
def trunc(value):
    if value >= 0: return int(value)
    else: return int(value)-1

# Use single dot movement    
def movePartial(pos,velocity,size,physicstate,map):
    wallhit = -1 # 0 = right, 1 = top, 2 = left, 3 = bot
    
    if pos[0] < 0: x = -1; wallhit = 2
    else: x = int(pos[0]/constants.blockScale)
    if pos[1] < 0: y = -1; wallhit = 3
    else: y = int(pos[1]/constants.blockScale)
    if pos[0]+velocity[0] < 0: nx = -1; wallhit = 2
    else: nx = int((pos[0]+velocity[0])/constants.blockScale)
    if pos[1]+velocity[1] < 0: ny = -1; wallhit = 3
    else: ny = int((pos[1]+velocity[1])/constants.blockScale)
        
    om = map.get(x,y)
    if om == 1: # Error! push player?
        pass
    
    if nx != x: # First X (easier to land on platforms?)
        if map.get(nx,y) == 1:
            if velocity[0] > 0:
                velocity[0] = 0
                pos[0] = nx*constants.blockScale - constants.mue #constants.minScale # Rightmost
                wallhit = 0
            else:
                velocity[0] = 0
                pos[0] = x*constants.blockScale + constants.mue # Leftmost
                wallhit = 2
        else:
            x = nx
            pos[0]+=velocity[0]
    else:
        pos[0]+=velocity[0]
    if ny != y:
        if map.get(x,ny) == 1:
            if velocity[1] > 0:
                velocity[1] = 0
                pos[1] = ny*constants.blockScale - constants.mue #constants.minScale # Top
                wallhit = 1
            else:
                velocity[1] = 0
                pos[1] = y*constants.blockScale + constants.mue # Bottom
                physicstate = 1 # Landed!
                wallhit = 3
        else:
            pos[1]+=velocity[1]
    else:
        pos[1]+=velocity[1]
        
    return pos,velocity,physicstate,wallhit
    

# Use sized movement 
# Warning: Only 1 Block difference allowed!
def movePartialSized_OLD(pos,velocity,size,physicstate,map):
    wallhit = -1 # 0 = right, 1 = top, 2 = left, 3 = bot, 4 = center
    
    xl = trunc((pos[0]-size[0]/2)/constants.blockScale)
    xr = trunc((pos[0]+size[0]/2)/constants.blockScale)
    ydown = trunc((pos[1]-size[1]/2)/constants.blockScale)
    yup = trunc((pos[1]+size[1]/2)/constants.blockScale)
    
    for x in range(xl,xr+1):
        for y in range(ydown,yup+1):
            if map.get(x,y) == 1: # Error! push player?
                wallhit = 4
                return pos,velocity,physicstate,wallhit
    
    nxl = trunc((pos[0]+velocity[0]-size[0]/2)/constants.blockScale)
    nxr = trunc((pos[0]+velocity[0]+size[0]/2)/constants.blockScale)
    loopwall = False
    if nxl != xl or nxr != xr: # First X (easier to land on platforms?)
        if velocity[0] > 0:
            for y in range(ydown,yup+1):
                if map.get(nxr,y) == 1:
                    velocity[0] = 0
                    pos[0] = nxr*constants.blockScale - size[0]/2 - constants.mue #constants.minScale # Rightmost
                    wallhit = 0
                    loopwall = True
                    break
        else: # if velocity[0] < 0:
            for y in range(ydown,yup+1):
                if map.get(nxl,y) == 1:
                    velocity[0] = 0
                    pos[0] = xl*constants.blockScale + size[0]/2 + constants.mue # Leftmost
                    wallhit = 2
                    loopwall = True
                    break
        if not loopwall:
            pos[0]+=velocity[0]
    else:
            pos[0]+=velocity[0]
        
        
    xl = trunc((pos[0]-size[0]/2)/constants.blockScale)
    xr = trunc((pos[0]+size[0]/2)/constants.blockScale)
    nydown = trunc((pos[1]+velocity[1]-size[1]/2)/constants.blockScale)
    nyup = trunc((pos[1]+velocity[1]+size[1]/2)/constants.blockScale)
        
    loopwall = False
    if nyup != yup or nydown != ydown:
        if velocity[1] > 0:
            for x in range(xl,xr+1):
                if map.get(x,nyup) == 1:
                    velocity[1] = 0
                    pos[1] = nyup*constants.blockScale - size[1]/2 - constants.mue #constants.minScale # Top
                    wallhit = 1
                    loopwall = True
        else:
            for x in range(xl,xr+1):
                if map.get(x,nydown) == 1:
                    velocity[1] = 0
                    pos[1] = ydown*constants.blockScale + size[1]/2 + constants.mue # Bottom
                    wallhit = 3
                    loopwall = True
                    physicstate = 1 # Landed!!!!!!!!!!!!!!!!
        if not loopwall:
            pos[1]+=velocity[1]
    else:
        pos[1]+=velocity[1]
                
    return pos,velocity,physicstate,wallhit


# Use sized movement 
# Warning: Only 1 Block difference allowed!
def movePartialSized(pos,velocity,size,physicstate,map):
    wallhit = [False,False,False,False,False]
    # 0 = right, 1 = top, 2 = left, 3 = bot, 4 = center
    
    xl = trunc((pos[0]-size[0]/2)/constants.blockScale)
    xr = trunc((pos[0]+size[0]/2)/constants.blockScale)
    ydown = trunc((pos[1]-size[1]/2)/constants.blockScale)
    yup = trunc((pos[1]+size[1]/2)/constants.blockScale)
    
    moving_uphill = False
    moving_downhill = False
    
    # CHECK IF STUCK IN WALL !!!
    for x in range(xl,xr+1):
        for y in range(ydown,yup+1):
            if map.get(x,y) == constants.block_solid: # Error! push player?
                wallhit[4] = True
                return pos,velocity,physicstate,wallhit
            
            
    # If moving UPHILL or DOWNHILL over one block, ignore a solid block on bottom!!!
            
    nxl = trunc((pos[0]+velocity[0]-size[0]/2)/constants.blockScale)
    nxr = trunc((pos[0]+velocity[0]+size[0]/2)/constants.blockScale)
    
    if velocity[0] >= 0 and map.get(xr,ydown) == constants.block_uphill:# going uphill
        moving_uphill = True
        if nxr != xr:
            if velocity[1] <= 0:
                velocity[1] = 0
                physicstate = 1 # Landed!
                wallhit[3] = True
            ydown += 1
            pos[1] = ydown*constants.blockScale + size[1]/2 + constants.mue # Bottom
            yup = trunc((pos[1]+size[1]/2)/constants.blockScale)
            
    elif velocity[0] <= 0 and map.get(xl,ydown) == constants.block_downhill:# going downhill
        moving_downhill = True
        if nxl != xl:
            if velocity[1] <= 0:
                velocity[1] = 0
                physicstate = 1 # Landed!
                wallhit[3] = True
            ydown += 1
            pos[1] = ydown*constants.blockScale + size[1]/2 + constants.mue # Bottom
            yup = trunc((pos[1]+size[1]/2)/constants.blockScale)
    
    # Check for Walls LEFT and RIGHT !!!!!
    
    loopwall = False
    if nxl != xl or nxr != xr: # First X (easier to land on platforms?)
        if velocity[0] > 0:
            for y in range(ydown,yup+1):
                if map.get(nxr,y) in [constants.block_solid,constants.block_downhill]:
                    velocity[0] = 0
                    pos[0] = nxr*constants.blockScale - size[0]/2 - constants.mue #constants.minScale # Rightmost
                    wallhit[0] = True
                    loopwall = True
                    break
        else: # if velocity[0] <= 0:
            for y in range(ydown,yup+1):
                if map.get(nxl,y) in [constants.block_solid,constants.block_uphill]:
                    velocity[0] = 0
                    pos[0] = xl*constants.blockScale + size[0]/2 + constants.mue # Leftmost
                    wallhit[2] = True
                    loopwall = True
                    break
                
    # Execute X-Movement, but prevent UPHILL / DOWNHILL pushing you into WALLS
    # (The Y-part of UPHILL / DOWNHILL will be handled later)
                    
    if not loopwall:
        if moving_uphill:
            #tx = pos[0]+velocity[0]
            changed_yup = trunc((pos[1]+size[1]/2+velocity[0])/constants.blockScale)
            if changed_yup != yup:
                for x in range(nxl,nxr+1):
                    if map.get(x,changed_yup) == constants.block_solid:
                        velocity[0] = constants.blockScale - (pos[1]+size[1]/2) % constants.blockScale - constants.mue
                        wallhit[0] = True
                        break
            pos[0]+=velocity[0]
                
        elif moving_downhill:
            changed_yup = trunc((pos[1]+size[1]/2-velocity[0])/constants.blockScale)
            if changed_yup != yup:
                for x in range(nxl,nxr+1):
                    if map.get(x,changed_yup) == constants.block_solid:
                        velocity[0] = - ( constants.blockScale - (pos[1]+size[1]/2) % constants.blockScale - constants.mue )
                        wallhit[2] = True
                        break
            pos[0]+=velocity[0]
            
        else:
            pos[0]+=velocity[0]
        
    # Check for Walls UP and DOWN !!!!!!!
        
    xl = trunc((pos[0]-size[0]/2)/constants.blockScale)
    xr = trunc((pos[0]+size[0]/2)/constants.blockScale)
    nydown = trunc((pos[1]+velocity[1]-size[1]/2)/constants.blockScale)
    nyup = trunc((pos[1]+velocity[1]+size[1]/2)/constants.blockScale)
        
    loopwall = False
    
    # Check hitting ceilings (UP)
    
    if velocity[1] > 0:
        if nyup != yup: # Only relevant if block is changed
            for x in range(xl,xr+1):
                if map.get(x,nyup) == constants.block_solid:
                    velocity[1] = 0
                    pos[1] = nyup*constants.blockScale - size[1]/2 - constants.mue #constants.minScale # Top
                    wallhit[1] = True
                    loopwall = True
                    break
    else: #if velocity[1] <= 0: # Consider uphill, downhill and platforms
        
        # If in a UPHILL / DOWNHILL / PLATFORM, push the Y-Coordinate to the correct level
        
        for x in range(xl,xr+1): # Movement in same block part
            mpv = map.get(x,ydown)
            if mpv == constants.block_platform or (x!=xr and mpv == constants.block_uphill) or (x!=xl and mpv == constants.block_downhill): # push up platform
                velocity[1] = 0
                pos[1] = (ydown-1)*constants.blockScale + size[1]/2 + constants.mue
                wallhit[3] = True
                loopwall = True
                physicstate = 1
                break # overrules others
            elif mpv == constants.block_uphill: # x == xr           
                diff = (pos[0]+size[0]/2) % constants.blockScale  
                maxy = (ydown)*constants.blockScale + diff + size[1]/2 + constants.mue # Bottom 
                if pos[1]+velocity[1] <= maxy:
                    pos[1] = maxy 
                    wallhit[3] = True
                    loopwall = True
                    physicstate = 1
                    velocity[1] = 0
                    break # xr is the last to check, so this is ok here
            elif mpv == constants.block_downhill: # x == xl
                diff = constants.blockScale - (pos[0]-size[0]/2) % constants.blockScale  
                maxy = (ydown)*constants.blockScale + diff + size[1]/2 + constants.mue # Bottom 
                if pos[1]+velocity[1] <= maxy:
                    pos[1] = maxy
                    wallhit[3] = True
                    loopwall = True
                    physicstate = 1
                    velocity[1] = 0
                    # No "break" here because this may get overwritten!
        
        # Move on top of Blocks
        
        if not loopwall and nydown != ydown: # Moevement into other block part
            for x in range(xl,xr+1): # Movement in same block part
                mpv = map.get(x,nydown)
                if mpv in [constants.block_platform,constants.block_solid] or (x!=xr and mpv == constants.block_uphill) or (x!=xl and mpv == constants.block_downhill): # push up platform
                    velocity[1] = 0
                    pos[1] = (ydown)*constants.blockScale + size[1]/2 + constants.mue
                    wallhit[3] = True
                    loopwall = True
                    physicstate = 1
                    break # overrules others
                elif mpv == constants.block_uphill: # x == xr           
                    diff = (pos[0]+size[0]/2) % constants.blockScale  
                    maxy = (nydown)*constants.blockScale + diff + size[1]/2 + constants.mue # Bottom 
                    if pos[1]+velocity[1] <= maxy:
                        pos[1] = maxy 
                        wallhit[3] = True
                        loopwall = True
                        physicstate = 1
                        velocity[1] = 0
                        break # xr is the last to check, so this is ok here
                elif mpv == constants.block_downhill: # x == xl
                    diff = constants.blockScale - (pos[0]-size[0]/2) % constants.blockScale  
                    maxy = (nydown)*constants.blockScale + diff + size[1]/2 + constants.mue # Bottom 
                    if pos[1]+velocity[1] <= maxy:
                        pos[1] = maxy
                        wallhit[3] = True
                        loopwall = True
                        physicstate = 1
                        velocity[1] = 0
                        # No "break" here because this may get overwritten!
                        
    # Execute Y-Movement if not hitting anything !!!
    
    if not loopwall:
        pos[1]+=velocity[1]
                
    return pos,velocity,physicstate,wallhit