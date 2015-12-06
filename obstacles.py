from random import randint, choice
import pygame as pg
import prepare, tools

      
class Obstacle(pg.sprite.Sprite):
    """Base class for course objects."""
    def __init__(self, name, midbottom, collider_tl, collider_size, *groups):
        super(Obstacle, self).__init__(*groups)
        self.name = name
        self.image = prepare.GFX[self.name]
        self.pos = midbottom
        self.rect = self.image.get_rect(midbottom=midbottom)
        x, y = collider_tl
        self.collider = pg.Rect((self.rect.left + x, self.rect.top + y),
                                          collider_size)
        
    def collide_with_boarder(self, boarder):
        """
        Called when player collides with an obstacle. Obstacles that
        should cause a crash when collided with should call boarder.crash
        from this method.
        """
        pass
    
    def update(self, boarder):
        pass
       
    def draw(self, surface, offset):
        surface.blit(self.image, self.rect.move(offset))
        #pg.draw.rect(surface, pg.Color("red"), self.collider.move(offset))
        #pg.draw.rect(surface, pg.Color("blue"), self.rect.move(offset), 2)
        #try:
        #    pg.draw.rect(surface, pg.Color("green"), self.goal_rect.move(offset), 2)
        #except:
        #    pass
            

class Tree(Obstacle):
    """A pine tree for crashing into."""
    def __init__(self, midbottom, *groups):
        super(Tree, self).__init__("tree", midbottom, (11, 27), (3, 4), *groups)
    
    def collide_with_boarder(self, boarder):
        boarder.crash()


class Rock(Obstacle):
    """A rock for crashing into."""
    def __init__(self, midbottom, *groups):
        super(Rock, self).__init__("rock", midbottom, (0, 24), (23, 8), *groups)

    
    def collide_with_boarder(self, boarder):
        boarder.crash()
        
    
class Gate(Obstacle):
    """
    Base class for slalom gates. Passing a gate on the correct side changes the gate's
    image and plays a boing sound.
    """    
    def __init__(self, image_name, midbottom, *groups):
        super(Gate, self).__init__(image_name, midbottom, (16, 32), (6, 6), *groups)
        self.unpassed_image = self.image
        self.goal_rect = pg.Rect(0, 0, 250, self.collider.height)
        self.passed = False
        
    def reset(self):
        self.passed = False
        self.image = self.unpassed_image 
        
    def update(self, boarder):
        if not self.passed: 
            if self.goal_rect.collidepoint(boarder.collider.midbottom):
                self.image = self.passed_image
                self.sound.play()
                self.passed = True
    
    def collide_with_boarder(self, boarder):
        boarder.crash()

        
class LeftGate(Gate):
    def __init__(self, midbottom, *groups):
        super(LeftGate, self).__init__("leftgate", midbottom, *groups)
        self.passed_image = prepare.GFX["passedgate"]
        self.sound = prepare.SFX["boing1"]
        self.goal_rect.topright = self.collider.topleft
        

class RightGate(Gate):
    def __init__(self, midbottom, *groups):
        super(RightGate, self).__init__("rightgate", midbottom, *groups)
        self.passed_image = prepare.GFX["passedgate"]
        self.sound = prepare.SFX["boing2"]
        self.goal_rect.topleft = self.collider.topright

                
class Jump(Obstacle):
    """Currently unimplemented, a jump for catching some air."""
    def __init__(self, midbottom, *groups):
        self.entrance = "down"
        super(Jump, self).__init__("jump", midbottom, (0, 6), (29, 15), *groups)
        self.hit = False
        
   
class GreenSign(Obstacle):
    """A trail marker for relatively easy trails."""
    def __init__(self, midbottom, *groups):
        super(GreenSign, self).__init__("greensign", midbottom, (16, 32), (6, 6), *groups)
        
        
class BlueSign(Obstacle):
    """A trail marker for moderately difficult trails."""
    def __init__(self, midbottom, *groups):
        super(BlueSign, self).__init__("bluesign", midbottom, (16, 32), (6, 6), *groups)
        

class BlackSign(Obstacle):
    """A trail marker for difficult trails."""
    def __init__(self, midbottom, *groups):
        super(BlackSign, self).__init__("blacksign", midbottom, (16, 32), (6, 6), *groups)        
        

class Chair(pg.sprite.Sprite):
    """Base class for chairlift chairs."""
    def __init__(self, name, midbottom, *groups):
        super(Chair, self).__init__(*groups)
        self.name = name
        self.xpos, self.ypos = midbottom
        if name == "upchair":
            if not randint(0, 4):
                self.image = prepare.GFX["upchair0"]
            else:
                self.image = choice(prepare.CHAIRS)
        else:
            self.image = prepare.GFX[self.name]        
        self.rect = self.image.get_rect(midbottom=midbottom)
        self.collider = pg.Rect(self.rect.center, (2, 2))
        
    def draw(self, surface, offset):
        surface.blit(self.image, self.rect.move(offset))
       
       
class DownChair(Chair):
    """An empty chairlift chair travelling down the mountain."""
    def __init__(self, midbottom, *groups):
        super(DownChair, self).__init__("downchair", midbottom, *groups)
        
        
class UpChair(Chair):
    """
    A chairlift chair travelling up the mountain with a random
    number of randomly colored elves riding it.
    """
    def __init__(self, midbottom, *groups):
        super(UpChair, self).__init__("upchair", midbottom, *groups)
        
        
class TopLiftHut(Obstacle):
    """Where elves get off the chairlift."""
    def __init__(self, midbottom, *groups):
        super(TopLiftHut, self).__init__("toplifthut", midbottom, (0, 0), (2, 2), *groups)

        
class BottomLiftHut(Obstacle):
    """
    Where elves get on the chairlift. Snowboarding inbto this building will return the
    player to the top of the mountain for another run.
    """
    def __init__(self, midbottom, *groups):
        super(BottomLiftHut, self).__init__("bottomlifthut", midbottom, (0, 0), (2, 2), *groups)


class Pylon(Obstacle):
    """A pole that supoorts the chairlift cables."""
    def __init__(self, midbottom, *groups):
        super(Pylon, self).__init__("pylon", midbottom, (0, 35), (4, 5), *groups)

    def collide_with_boarder(self, boarder):
        boarder.crash()
        
        
class Cable(Obstacle):
    """The cables that chairlift chairs are suspended from."""
    def __init__(self, midbottom, *groups):
        super(Cable, self).__init__("cables", midbottom, (0, 0), (2, 2), *groups)
            
