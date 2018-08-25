import pygame
import math
from settings import *
from UI import *
from SpriteSheet import *
vec = pygame.math.Vector2

#Define the whole Enemy class here
#The goal of the Enemy class is to handle everything the basic enemy can do
#Inherit this for future enemies
class Enemy(pygame.sprite.Sprite):
    #Constructor requires the game, an x and a y location
    def __init__(self, game, x, y):
        #Create the groups for the enemy, the active sprite list and enemies list
        self.groups = game.active_sprite_list, game.enemies                                  
        #Build the sprites for the groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        #This is the game
        self.game = game
        
        #Give type of "Enemy"
        self.type = "Enemy"
        
        #set the image to a surface the size of a tile
        sprite_sheet = SpriteSheet("enemy.png") #load sprite sheet       
        image = sprite_sheet.get_image(0,0, 32, 32)
        self.icon = image
        self.image = self.icon
        #Get the rect
        self.rect = self.image.get_rect()
        
        #Create the hitbox
        self.hitbox = pygame.Rect(0, 0, 32, 32)
        self.hitbox.center = self.rect.center
        
        #Avoid radius to avoid other enemies
        self.avoidRadius = 50
        
        self.vel = vec(0, 0)        
        #Set the x and y grid coordinate
        self.pos = vec(x, y)
        #Set player rotation
        self.rotation = 0
        
        #Set enemy acceleration
        self.acceleration = vec(0,0)
        self.enemySpeed = ENEMY_SPEED
        
        #Health-----------------------------
        #enemy's max hp
        self.maxHealth = 30
        #enemy's current hp, initilized at max hp value
        self.currentHealth = self.maxHealth
        #create the hitbar
        self.hitbar = Hitbar(self)
        #add new hitbar to sprite list
        game.active_sprite_list.add(self.hitbar)
        
        #Regen rate is currently 2%/sec
        self.regenRate = .02 / FPS
        
        #Target----------------------------
        #Range at which target aggro's to target
        self.aggroRange = 300
        #Initilize target to None
        self.target = None
        
        #Attack----------------------------
        #Range of which enemy can attack target
        self.attackRange = 70
        #Base auto attak damage
        self.damage = 10
        #Attack speed
        self.attackSpeed = 1000
        #The timer between auto attacks
        self.attackTimer = 0
        
        
        #self.game.qt.insert(self)
        

    def get_rect(self):
        return self.rect
    
    #Define what hapens when searching for new target
    def newTarget(self):
        #Loop throught list of players in game
        for player in self.game.players:
            #calculate distance to Player in list
            self.distanceToPlayer = math.hypot(player.pos.x - self.pos.x, player.pos.y - self.pos.y)
            
            #If Player in list distance <= enemy aggroRang
            if self.distanceToPlayer <= self.aggroRange:
                #Set target to that player
                self.target = player
            
            #Reset the distance for the next time searching
            self.distanceToPlayer = None
            
    #Walking---------------------------------------------          
    def newWaypoint(self):
        #Define enemy waypoint walking system
        self.vel = self.target.pos - self.pos
        self.distanceToTarget = math.hypot(self.vel.x, self.vel.y)
    
    #Adjust acceleration based on if another enemy is near to path around that enemy
    def avoidEnemies(self):
        for enemy in self.game.enemies:
            if enemy != self:
                distToEnemy = self.pos - enemy.pos
                if 0 < distToEnemy.length() < self.avoidRadius:
                    self.acceleration += distToEnemy.normalize()
    
    #Collision--------------------------------------------
    #Check collision with walls and handle for x then y movement    
    def checkCollision(self, dir):
        if dir == "x":
            hits = pygame.sprite.spritecollide(self, self.game.walls, False, collideHitbox)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.hitbox.width / 2
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.hitbox.width / 2
                #Reset vx
                self.vel.x = 0
                #Update rect for new x coordinate
                self.hitbox.centerx = self.pos.x
                
        if dir == "y":
            hits = pygame.sprite.spritecollide(self, self.game.walls, False, collideHitbox)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.hitbox.height / 2
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.hitbox.height / 2
                self.vel.y = 0
                self.hitbox.centery = self.pos.y
        
                
    #Damage taken----------------------------------------            
    def takeDamage(self, damage):    
        #Define what happens when the enemy takes damage
        #Reduce health by damage passed in
        self.currentHealth -= damage
        #If that brings the health at or below 0, die
        if self.currentHealth <= 0:
            #kill the hitbar
            self.hitbar.kill()
            #kill the creature
            self.kill()
            
    #Define what happens to regen enemy hp
    def regenerateHealth(self):
        if self.currentHealth + (self.maxHealth * self.regenRate) <= self.maxHealth:
            self.currentHealth += self.maxHealth * self.regenRate
    
    #Attacks---------------------------------------------
    #Define what happens when enemy atacks
    def attack(self):
        #Call target's take damage function
        self.target.takeDamage(self.damage)
    
    #Here is what happens frame by frame for this enemy
    def update(self):          
        #if self.game.camera.camera.contains(self.rect):
        #If enemy has no current target
        if self.target == None:
            #Try to find a new target
            self.newTarget() 
        
        #Enemy must already have a target 
        else:
            #Get the next waypoint towards target
            self.newWaypoint() 
            
            #Make sure target is still in range
            if self.distanceToTarget > self.aggroRange:
                #If target not in range, untarget
                self.target = None 
                
            elif self.distanceToTarget <= self.attackRange:
                #attack when in range and create a cooldown on the attack
                now = pygame.time.get_ticks()
                if now - self.attackTimer > self.attackSpeed:    
                    self.attack()
                    self.attackTimer = now
            
            else: #Get in range
                #Calculate the angle to current target
                self.rotation = (self.vel).angle_to(vec(1, 0))
                #rotate the sprite based on that angle
                self.image = pygame.transform.rotate(self.icon, self.rotation)
                #Update the rect center to be the position of the enemy
                self.rect.center = self.pos
                
                #calculate acceleration
                self.acceleration = vec(1, 0).rotate(-self.rotation)
                
                #Adjust acceleration if another enemy is near
                #self.avoidEnemies()
                
                #Adjust acceleration based on enemy speed
                self.acceleration.scale_to_length(self.enemySpeed)
                #Update acceleration with velocity vector
                self.acceleration += self.vel * -1
                
                #Move along the vel vector by acceleration and delta time
                self.vel += self.acceleration * self.game.dt
                #Move pos along that vector
                self.pos += self.vel * self.game.dt + 0.5 * self.acceleration * self.game.dt ** 2
                
                #self.game.qt.remove(self)
                #self.game.qt.insert(self)
        
        #Update hitbox first, check collisions between hitbox and wall and handle them
        self.hitbox.centerx = self.pos.x
        #self.checkCollision("x")
        self.hitbox.centery = self.pos.y
        #self.checkCollision("y")
        
        #Update rect center to be hitbox center after all collisions have been handled
        self.rect.center = self.hitbox.center
        
        #Apply regeneration
        self.regenerateHealth()
        
        
        
