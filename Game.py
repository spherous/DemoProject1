import pygame
import sys
import random
from os import path
from settings import *
from Player import *
from Level import *
from Enemy import *
from UI import *
from Quadtree import *

#This is the Game class
#Where the magic begins
class Game:
    def __init__(self):
        #Constuctor for the game object
        pygame.init() #Initilize pygame
        
        #Set the screen to a window size from settings
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT)) 
        
        #Set window caption from title in settings
        pygame.display.set_caption(TITLE)
        
        #create the clock
        self.clock = pygame.time.Clock()
        
        #Cal load_data function
        self.load_data()
        
    #load_data is where we define what map is opened
    def load_data(self):
        game_folder = path.dirname(__file__)
        #create new Map object with parameters of the current map's file.
        self.map = Map(path.join(game_folder, "map2.txt"))
        
    
    #When new instance
    def new(self):
        #create sprite groups------------------------------------------------
        self.active_sprite_list = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        
        #Setup QuadTree-------------------------------------------------------
        #self.boundry = Rectangle(self.map.width / 2, self.map.height / 2, self.map.width / 2, self.map.height / 2)
        #self.qt = QuadTree(self.boundry)
        
        #Loop throught map and create level------------------------------------
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    self.wall = Wall(self, col, row)
                if tile == "P":  
                    self.player = Player(self, col, row)
        
        #Generate random enemies------------------------------------------------
        #TODO: Expand enemy generation, decide on how many to spawn, packs, packsize, types of, and level of the enemies for scaling
        for i in range(10):
            x = random.randint(0, self.map.width)
            y = random.randint(0, self.map.height)
            self.enemy = Enemy(self, x, y)
        
        #Creates the camera from Camera class with parameters of the map's width  and height
        self.camera = Camera(self.map.width, self.map.height)
        
     
    #Game loop. Set self.playing to False to end the game
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000 #Current delta time
            self.events() #Call events
            self.update() #Call updates
            self.draw() #Draw screen
    
    #When game is quit
    def quit(self):
        pygame.quit()
        sys.exit()
        
    #Define what needs to be updated each frame    
    def update(self):        
        
        #Update all active sprites
        self.active_sprite_list.update()
        
        #Update the camera
        self.camera.update(self.player)
        
        self.tree = Quadtree(0, pygame.Rect(0,0,self.map.width,self.map.height), self.active_sprite_list)
        self.tree.update()
        #self.onScreen = []
        #self.onScreen = self.tree.query(self.camera, self.onScreen)
        
       
    #Draw the grid - not for final project.
    #TODO: create toggle in UI for testing enabled
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    
    #Define how the game is going to draw
    def draw(self):
        #Fill the screen with a background color set in settings
        self.screen.fill(BGCOLOR)
        
        if DRAWGRID:
            self.draw_grid()
            
        self.tree.draw(self.camera, self.screen)
        
        #Loop through sprites in the active sprite list
        for sprite in self.active_sprite_list:
            #Draw that sprite to sceen at the location set by the camera
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            
            
        #Flip to next frame
        pygame.display.flip()
    
    #Main event listener
    def events(self):
        #For each event returned from pygame.event.get
        for event in pygame.event.get():
            #If the event is a QUIT command
            if event.type == pygame.QUIT:
                #Quit the game
                self.quit()
            #If the event is the player pressing a button
            elif event.type == pygame.KEYDOWN:
                #And if that button is Escape
                if event.key == pygame.K_ESCAPE:
                    self.quit() #Quit the game 
                elif event.key == pygame.K_SPACE:
                    print(self.player.nearbyEntities)
                    
                #Old movement logic------------------------------------------    
                #Key is left arrow or a
                #elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    #Move vx left by playerSpeed
                #    self.player.rotateLeft()
                #Key is right arrow or d    
                #elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    #Move vx right by playerSpeed
                #    self.player.rotateRight()
                #Key is up arrow or w
                #elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    #Move vy up by playerSpeed
                #    self.player.moveForward()
                #Key is down arrow or s
                #elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    #Move vy down by playerSpeed
                #    self.player.moveBackward()
                    
            #elif event.type == pygame.KEYUP:
            #    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    #Move vx left by playerSpeed
            #        self.player.stopRotateLeft()
                #Key is right arrow or d    
            #    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    #Move vx right by playerSpeed
            #        self.player.stopRotateRight()
                #Key is up arrow or w
            #    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    #Move vy up by playerSpeed
            #        self.player.stopMoveForward()
                #Key is down arrow or s
            #    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    #Move vy down by playerSpeed
            #        self.player.stopMoveBackward()
            #End old movement logic -----------------------------------------
            
            elif event.type == pygame.MOUSEBUTTONUP:
                #when mouse is released, set movePoint to it's most recent location
                x, y = pygame.mouse.get_pos()
                self.player.newMovePoint(x - self.camera.x, y - self.camera.y)
                
            if pygame.mouse.get_pressed()[0]:
                #Move to mouse as long as it's pressed.
                x, y = pygame.mouse.get_pos()
                self.player.newMovePoint(x - self.camera.x, y - self.camera.y)
                
            
#Create the main game object            
g = Game()

while True:
    g.new() #Create the new instance
    g.run() #Run the main game loop

            
