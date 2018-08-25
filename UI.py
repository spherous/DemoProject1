import pygame
from settings import *

#Define UI elements here

#Define Camera here
#The Camera is the section of the map with the player object centered that is being displayed to the player
class Camera(object):
    #Construct with width and height of the map
    def __init__(self, width, height):
        #Make the camera rect beginning at 0, 0 with the width and height of the map
        self.camera = pygame.Rect(0, 0, width, height)
        #self.rect = self.camera.get_rect()
        self.rect = self.camera
        
        #Set the width and height
        self.width = width
        self.height = height
    
    #When the camera is applied, give it the entity you wish to focus on
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    
    #Update the camera at a target object, typically the player
    def update(self, target):
        self.x = -target.rect.centerx + int(WIDTH / 2)
        self.y = -target.rect.centery + int(HEIGHT / 2)

        self.x = min(0, self.x)
        self.y = min(0, self.y)
        
        self.x = max(-(self.width - WIDTH), self.x)
        self.y = max(-(self.height - HEIGHT), self.y)
        
        #Update the camera rect to proper location calculated
        self.camera = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.rect = self.camera
        
#Define Hitbar
#Pass this class any entity that has: x, y, currentHealth and maxHealth
#It will then draw a hitbar above that entity
class Hitbar(pygame.sprite.Sprite):
    #Constructor takes entity
    def __init__(self, entity):
        super().__init__()
        #Set the entity
        self.entity = entity
        self.lengthMod = 1
        
        #Build and display the bar with update call
        self.update()  
    
    #Update the hitbar each frame
    def update(self):
        #Set the bar's x and y coords, offset by half the tilesize from settings
        self.x = self.entity.pos.x
        self.y = self.entity.pos.y - TILESIZE * 1.5
        
        #Calculate what percent 0.0-1.0
        self.healthPercent = self.entity.currentHealth / self.entity.maxHealth
        #Create the surface as tilesie multiplied by healthPercent
        #Current fixed height of 10
        #TODO make height dynamic
        if self.healthPercent < 0:
            self.healthPercent = 0
        self.image = pygame.Surface([(TILESIZE * self.lengthMod * self.healthPercent), 10])
        
        #If the entity this hitbar is on is a Player, color it green, if enemy, red
        if self.entity.type == "Player":
            self.image.fill(GREEN)
        elif self.entity.type == "Enemy":
            self.image.fill(RED)
        
        #Get the hitbar rec
        self.rect = self.image.get_rect()
        
        #Draw the hitbar at updated coordinates
        self.rect.centerx = self.x     
        self.rect.centery = self.y
        
        
    def get_rect(self):
        return self.rect
        
        
