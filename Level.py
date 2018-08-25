import pygame
from settings import *
vec = pygame.math.Vector2

#Define the Map class
#This class takes in a filename, opens that file, and creates the set that holds that map instance
class Map:
    #Constructor takes filename
    def __init__(self, filename):
        #Create empty data set
        self.data = []
        
        #Open file with the file name
        with open(filename, "rt") as f:
            #Loop through each line
            for line in f:
                #On each line, append that line to data set
                self.data.append(line.strip())
                
        #The tile width is the lenght of data[0]        
        self.tilewidth = len(self.data[0])
        #The tile height is the length of data
        self.tileheight = len(self.data)
        
        #set the width and height by the map
        self.width = self.tilewidth * TILESIZE        
        self.height = self.tileheight * TILESIZE

#When a new wall is created
class Wall(pygame.sprite.Sprite):
    #Constructor requires the game object, an x, and a y of which map grid it's in
    def __init__(self, game, x, y):
        #Create the groups needed, the active sprite list and the list of walls
        self.groups = game.active_sprite_list, game.walls
        #Construct pygame sprite with groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        #The game object
        self.game = game
        
        self.type = "Wall"
        
        #Create the image to be displayed, use tilesize for width and length to fit on grid
        #TODO: Change this to a sprite with many wall posibilities
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        #Color the wall
        self.image.fill(PINK)
        #Get the wal rect
        self.rect = self.image.get_rect()
        
        #Set the x and y coordinates and draw the rect to the proper grid location
        self.pos = vec(x, y)
        self.rect.x = self.pos.x * TILESIZE
        self.rect.y = self.pos.y * TILESIZE
        
        #self.game.qt.insert(self)
        
    def get_rect(self):
        return self.rect
class Chunk():
    pass