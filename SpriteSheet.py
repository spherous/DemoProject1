import pygame
from settings import *

BLACK = (0, 0, 0)
#Build SpriteSheet class
class SpriteSheet(object):  
    #Constuctor - pass in the file name of the sprites sheet
    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()
        
    def get_image(self, x, y, width, height):
        #get a single image out of sprite sheet
        #Pass in x, y, height and width of new sprite
        
        image = pygame.Surface([width,height]).convert()#Create a new blank image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height)) #copy sprite from sheet to small new image
        image.set_colorkey(BLACK) #assuming black works as transparent color
        #self.size = image.get_size()
        #new_image = pygame.transform.scale(image, (int(self.size[0]), int(self.size[1])))
        #image = new_image
        return image #return new sprite image
    
    