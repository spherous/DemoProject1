import pygame

#Display quadtree in background if True
displayTree = True

GREEN = (0, 255, 0)

def rect_quad_split(rect):
    #Returns a list of rects from a larger rect divided into 4 equal quadrents
    width = rect.width / 2.0
    height = rect.height / 2.0
    rl=[]
    rl.append(pygame.Rect(rect.left, rect.top, width, height))
    rl.append(pygame.Rect(rect.left + width, rect.top, width, height))
    rl.append(pygame.Rect(rect.left, rect.top + height, width, height))
    rl.append(pygame.Rect(rect.left + width, rect.top + height, width, height))
    return rl

class Quadtree(object):
    def __init__(self, level, rect, entities=[], color = (0,0,0)):
        #A quad tree class that recursively subdivides to create subbranches for collision detection
        
        self.maxlevel = 8
        #Max level of subdivision
        self.level = level
        #The level of subdivision that the branch is created on (0 for original branch)
        self.maxEntities = 3
        #Minimum number of particles without subdivision
        self.rect = rect
        #A pygame Rect object that represents the portion of the screen the branch covers
        self.entities = entities        
        #List of entity object instances that determine subdivision
        self.color = color
        #The color of the quadtree (if displayTree == True)
        self.branches = []
        #List of the branches
        self.divided = False
        
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)
        

    def get_rect(self):
        #Returns the rect
        return self.rect

    def subdivide(self):
        #Loop through the 4 new rects returned from rect_quad_split and create a new quadtree level for each branch
        #Then ad them to the list of branches
        for rect in rect_quad_split(self.rect):
            branch = Quadtree(self.level+1, rect, [], (self.color[0]+30,self.color[1],self.color[2]+20))
            self.branches.append(branch)
    
    def add_entity(self, entity):
        if pygame.sprite.collide_rect(self, entity):
            if len(self.entities) < self.maxEntities:
                #Adds a passed in entity to the list of entities
                self.entities.append(entity)
                return True
            if not self.divided:
                self.subdivide()
                self.divided = True
            for branch in self.branches:
                if branch.add_entity(entity):
                    return True
        else:
            return False
        
    def remove_entity(self, entity):
        if pygame.sprite.collide_rect(self, entity):
            for item in self.entities:
                if item == entity:
                    self.entities.remove(item)
                    return True
            if self.divided:
                for branch in self.branches:
                    if branch.remove_entity(entity):
                        return True
        else:
            return False
        

    
    def draw(self, camera, screen):
        screen.blit(self.image, camera.apply(self))
        for branch in self.branches:
            branch.draw(camera, screen)
                
    def query(self, rect, found = []):
        #Pass in a rect and a list
        #Will first remove items from that list that are no longer within the rect
        for item in found:
            if not pygame.sprite.collide_rect(item, rect):
                found.remove(item)
        
        #Will search the quadtree and it's branches to add the proper entity that does intersect the rect to the list found
        if pygame.sprite.collide_rect(self, rect):
            for entity in self.entities:
                #if entity not in found:
                found.append(entity)
                
            for branch in self.branches:
                branch.query(rect, found)
        
        #Returns that updated list of all entity objects within the given rect
        return found
        

    def update(self):
        pass
        #tests for subdivisions of branches
        #if len(self.entities) > self.maxEntities and self.level <= self.maxlevel:
        #    self.subdivide()
        #    self.subdivide_entities()
        #    for branch in self.branches:
        #        branch.update()
        
            
class mouseRect(object):
    #An object to hold the rectangle around the pointer
    def __init__(self, game):
        self.game = game
        
        self.x, self.y = pygame.mouse.get_pos()
        self.width = 175
        self.height = 100
        self.x -= self.width / 2
        self.y -= self.height / 2
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            
        
    def update(self):
        self.x, self.y = pygame.mouse.get_pos()
        self.rect.x = self.x - self.width / 2
        self.rect.y = self.y - self.height / 2
    
    
        
        
        
                
                
        
