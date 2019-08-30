# goc 

I'm building a game in my free time.
I'll try to combine sections of 
- Layered 2d j&r
- Pseudo 3d adventure
- 2d topdown roleplay


## Requires

- Python3
- pygame
- pyopengl
- PIL
- numpy

I'm using Anaconda3 and Spyder for programming.

## Contributing

If somebody wants to contribute, feel free to.
Please ask if you have questions

Also feel free to use my code.
MIT Licence for convenience.

## pyopengl

If somebody looks at my code to learn something about opengl in python:

- Rendering is handled by goc/graphics/ScreenGL.py
- goc/Master.py uses ScreenGL.Screen() as self.screen
-- ScreenGL.Screen() and ScreenGL.Screen.create_window() are called (I seperate that because I use a Global.py class to get hold of my main structure from everywhere)
- goc/Master.py draws everything by calling self.screen.draw()  (ScreenGL.Screen.draw)
-- ScreenGL.Screen.draw will init viewport etc and call Master.draw()
--- Master.draw -> Game.draw will draw all stages and objects
- Each object (e.g. Player.py) has a draw function that gets the ScreenGL.Screen as parameter and will draw the object with functions of ScreenGL.Screen.

## TODO

- Transitions between different stages
- 2d j&r : Life, Enemy behavior, Bosses, Powerups, Weapons/Attacks
- 2d physic : Downhill walk for low velocity
- 3d room : Room transitions, borders, interactible objects
- dialog
- Sound (if I find something that I can use)
- ...