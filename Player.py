import pygame
import math
from settings import *
from UI import *
from SpriteSheet import *
vec = pygame.math.Vector2

#Define the whole Player class here
#The goal of the Player class is to handle everything the player can do
class Player(pygame.sprite.Sprite):
    #Constructor take the game and the x and y coordinates
    def __init__(self, game, x, y):
        #Create the groups for the player, the active sprite list and players list
        self.groups = game.active_sprite_list, game.players
        #Build the sprites for the groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        #The game
        self.game = game
        
        self.active = True
        
        #Gives the player the Player type
        self.type = "Player"
        
        #Sprite-----------------------------
        sprite_sheet = SpriteSheet("player.png") #load sprite sheet       
        image = sprite_sheet.get_image(0,0, 64, 64)
        self.icon = image
        self.image = self.icon
        
        #Get the rect
        self.rect = self.image.get_rect()
        
        #Create the hitbox
        self.hitbox = pygame.Rect(0, 0, 54, 54)
        self.hitbox.center = self.rect.center
        
        
        #Movement----------------------------
        #Set the velocity vector
        self.vel = vec(0, 0)        
        #Set the proper grid position
        self.pos = vec(x, y) * TILESIZE        
        #Set player playerSpeed
        self.playerSpeed = PLAYER_SPEED        
        #Set player rotation
        self.rotation = 0
        self.rotationSpeed = 0
        self.movePoint = self.pos
        self.acceleration = vec(0,0)
        self.distanceToMovePoint = 0
        
        #Health------------------------------
        #TODO: Make this complex based on level and stats
        self.maxHealth = 100
        #Players current hp, initilized at players max hp on player creation
        self.currentHealth = self.maxHealth
        self.regenRate = .02 / FPS
        
        #create the hitbar
        self.hitbar = Hitbar(self)
        self.hitbar.lengthMod = 2
        #add new hitbar to sprite list
        game.active_sprite_list.add(self.hitbar) 
        
        #Target----------------------------
        #Player's current target stored, initilized as None
        self.target = None
        #Range for auto target system
        self.targetRange = 200
        #Distance to target, initilized as None
        self.targetDist = None
        
        #self.nearbyBox = Rectangle(self.pos.x, self.pos.y, self.targetRange, self.targetRange)
        self.nearbyEntities = []
        
        #Attack----------------------------
        #TODO: Expand to scale based on stats
        #Range for auto attacking target
        self.attackRange = 70
        #Speed to auto attack
        self.attackSpeed = 750
        #The cooldown timer for auto attack
        self.attackTimer = 0
        #Basic auto atack damage
        self.damage = 10
        
        
        self.game.tree.add_entity(self)
        
    def get_rect(self):
        return self.rect
        
    #Do mouse movement    
    def newMovePoint(self, x, y):
        self.movePoint = vec(x, y)
        self.vel = self.movePoint - self.pos
        self.distanceToMovePoint = math.hypot(self.vel.x, self.vel.y)
        
    #def rotateLeft(self):
    #    self.rotationSpeed = PLAYER_ROTATION_SPEED
    #def rotateRight(self):
    #    self.rotationSpeed = -PLAYER_ROTATION_SPEED
    #def moveForward(self):
    #    self.vel = vec(self.playerSpeed, 0).rotate(-self.rotation)
    #def moveBackward(self):
    #    self.vel = vec(-self.playerSpeed / 2, 0).rotate(-self.rotation)
    #def stopRotateLeft(self):
    #    self.rotationSpeed = 0
    #def stopRotateRight(self):
    #    self.rotationSpeed = 0
    #def stopMoveForward(self):
    #    self.vel = vec(0, 0).rotate(-self.rotation)
    #def stopMoveBackward(self):
    #    self.vel = vec(0, 0).rotate(-self.rotation)         
    
    #Check if collision with wall occured, pass in x or y based on direction traveling
    def checkCollision(self, dir):
        #If traveling on x axis
        if dir == "x":
            #hits is set if self sprite hits a wall in game.walls. False to not remove the wall when hit
            hits = pygame.sprite.spritecollide(self, self.game.walls, False, collideHitbox)
            #If something was hit
            if hits:
                #Check if we were heading left or right, adjust x properly
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.hitbox.width / 2
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.hitbox.width / 2
                #Reset vx
                self.vel.x = 0
                #Update rect for new x coordinate
                self.hitbox.centerx = self.pos.x
                self.movePoint.x = self.pos.x
                
        #Reapeat for y axis        
        if dir == "y":
            hits = pygame.sprite.spritecollide(self, self.game.walls, False, collideHitbox)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.hitbox.height / 2
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.hitbox.height / 2
                self.vel.y = 0
                self.hitbox.centery = self.pos.y
                self.movePoint.y = self.pos.y
    
    #Define what happens when the player takes damage, pass it damage given
    def takeDamage(self, damage):
        #Update currentHealth by damage
        self.currentHealth -= damage
        #Define what happens when health hits 0 or less
        #TODO:Respawn player
        if self.currentHealth <= 0:
            #To do self.kill()
            self.currentHealth = 0
            
    #Define what happens to regen player hp
    def regenerateHealth(self):
        #Check if regeneration should end because player's hp is full
        if self.currentHealth + (self.maxHealth * self.regenRate) <= self.maxHealth:
            self.currentHealth += self.maxHealth * self.regenRate
     
    #When attempting to find a new target 
    def newTarget(self):
        #Loop throught list of enemies in game
        for enemy in self.game.enemies:
            #Calculate distance to enemy in list
            self.distanceToEnemy = math.hypot(self.pos.x - enemy.pos.x, self.pos.y - enemy.pos.y) 
            
            #If enemy distance is less than or equal to player target range
            if self.distanceToEnemy <= self.targetRange:
                #Set target to that enemy
                self.target = enemy
                
            #Reset distance to enemy to None for next search    
            self.distanceToEnemy = None
    
    #Define what happens when attack is called
    def attack(self):
        #Cals the take damage function of the current target, passes its damage.
        self.target.takeDamage(self.damage)
        if self.target.currentHealth <= 0:
            self.target = None
    
    #Frame by frame updates
    def update(self):
        
        #If player has no current target
        if self.target == None:
            #Try to find a new target
            self.newTarget()
        
        #Player must already have a target
        else:
            #Calculate distance to the target
            self.targetDistance = math.hypot(self.pos.x - self.target.pos.x, self.pos.y - self.target.pos.y)
            
            #Make sure target is still in range
            if self.targetDistance > self.targetRange:
                #If target not in range, untarget
                self.target = None
            
            #Check if distnce to target is less than or equal to auto attack rang
            elif self.targetDistance <= self.attackRange:
                #Get time in ticks for now
                now = pygame.time.get_ticks()
                #If now = the attack timer is more than the player's atack speed
                if now - self.attackTimer > self.attackSpeed:
                    #Attack the target
                    self.attack()
                    #Set the attack timer to time for new attack so as to not attack repeadidly
                    self.attackTimer = now
                    
        #If near movePoint, stop moving         
        if self.distanceToMovePoint < 12:
            self.vel = vec(0,0)
        
        #If further from movePoint, move towards it
        else:
            #Calculate the angle to current movePoint
            self.rotation = (self.vel).angle_to(vec(1, 0))
            self.image = pygame.transform.rotate(self.icon, self.rotation)
            self.rect.center = self.pos
            
            self.acceleration = vec(1, 0).rotate(-self.rotation)
            
            #Adjust acceleration based on enemy speed
            self.acceleration.scale_to_length(self.playerSpeed)
            #Update acceleration with velocity vector
            self.acceleration += self.vel * -1
            
            #Move along the vel vector by acceleration and delta time
            self.vel += self.acceleration * self.game.dt
            #Move pos along that vector
            self.pos += self.vel * self.game.dt + 0.5 * self.acceleration * self.game.dt ** 2       
            
            #Calculate the new distance to the movepoint
            self.distanceToMovePoint = math.hypot(self.pos.x - self.movePoint.x, self.pos.y - self.movePoint.y)
            #self.game.qt.remove(self)
            #self.game.qt.insert(self)
            
            
        #update x and y rects for the frame and check and handle collision between each
        self.hitbox.centerx = self.pos.x
        #self.checkCollision("x")        
        self.hitbox.centery = self.pos.y
        #self.checkCollision("y")    
        #Update rect center to be hitbox center    
        self.rect.center = self.hitbox.center
        #self.nearbyBox.x = self.pos.x
        #self.nearbyBox.y = self.pos.y
        #self.nearbyEntities = self.game.qt.query(self.nearbyBox)
        
        #Regen the players HP
        self.regenerateHealth()
        
        self.game.tree.remove_entity(self)
        self.game.tree.add_entity(self)