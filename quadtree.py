from settings import *

class Rectangle():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def contains(self, entity):
        if entity.pos.x >= self.x - self.width and entity.pos.x <= self.x + self.width and entity.pos.y >= self.y - self.height and entity.pos.y <= self.y + self.height:
            return True
        
    def intersects(self, range):
        if range.x - range.width > self.x + self.width or range.x + range.width < self.x - self.width or range.y - range.height < self.y + self.height or range.y + range.height > self.y - self.height:
            return False
        
class QuadTree():
    def __init__(self, boundry):
        self.boundry = boundry
        self.capacity = QUADTREECAPACITY
        self.entities = []
        self.divided = False
        
    def subdivide(self):
        x = self.boundry.x
        y = self.boundry.y
        width = self.boundry.width
        height = self.boundry.height
        
        self.nw = Rectangle(x - width / 2, y - height / 2, width / 2, height / 2)
        self.ne = Rectangle(x + width / 2, y - height / 2, width / 2, height / 2)
        self.sw = Rectangle(x - width / 2, y + height / 2, width / 2, height / 2)
        self.se = Rectangle(x + width / 2, y + height / 2, width / 2, height / 2)
        
        self.northwest = QuadTree(self.nw)        
        self.northeast = QuadTree(self.ne)
        self.southwest = QuadTree(self.sw)
        self.southeast = QuadTree(self.se)
        
        self.divided = True
        
    def prune(self):
        if self.divided == True:
            if len(self.northwest.entities) == 0 and len(self.northeast.entities) == 0 and len(self.southwest.entities) == 0 and len(self.southeast.entities) == 0:
                self.northwest.kill()
                self.northeast.kill()
                self.southwest.kill()
                self.southeast.kill()
                self.divided = False
        
    def insert(self, entity):
        if self.boundry.contains(entity) != True:
            return False
        
        elif len(self.entities) < self.capacity:
            self.entities.append(entity)
            return True
        
        elif self.divided != True:
                self.subdivide()
                
        if self.northwest.insert(entity):
            return True
        elif self.northeast.insert(entity):
            return True
        elif self.southwest.insert(entity):
            return True
        elif self.southeast.insert(entity):
            return True
        
    def remove(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)
            #self.prune()
            return True
        
        elif self.divided == True:
            if self.northwest.remove(entity):
                #self.prune()
                return True
            elif self.northeast.remove(entity):
                #self.prune()
                return True
            elif self.southwest.remove(entity):
                #self.prune()
                return True
            elif self.southeast.remove(entity):
                #self.prune()
                return True
        return False
            
                
    def query(self, range, found = []):
        #for item in found:
        #    if not range.contains(item):
        #        found.remove(item)
                
        if self.boundry.intersects(range) != False:
            return
        
        else:
            for entity in self.entities:
                if range.contains(entity):
                    if entity not in found:
                        found.append(entity)
                        
                    
        if self.divided:
            self.northwest.query(range, found)
            self.northeast.query(range, found)
            self.southwest.query(range, found)
            self.southeast.query(range, found)
            
        return found
                    
                    
                    
