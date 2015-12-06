import pygame as pg

from animation import Animation, Task
from obstacles import Pylon, UpChair, DownChair, TopLiftHut, BottomLiftHut, Cable


class ChairLift(object):
    """Crates a chairlift in the center of the course."""
    def __init__(self, map_size):
        self.animations = pg.sprite.Group()
        width, length = map_size
        centerx = width // 2
        centery = 150
        self.top_lifthut = TopLiftHut((centerx, centery))
        self.pylons = pg.sprite.Group()
        self.cables = pg.sprite.Group()
        self.chairs = pg.sprite.Group()
        self.make_pylons(map_size)
        bottom = max((x.rect.bottom for x in self.pylons))
        self.bottom_lifthut = BottomLiftHut((centerx, bottom + 130))
        self.add_chairs()
        
    def make_pylons(self, map_size):
        """Add pylons (poles) for chairlift based on the length of the course."""
        width, length = map_size
        top = self.top_lifthut.rect.bottom + 158
        centerx = self.top_lifthut.rect.centerx
        num_pylons, remainder = divmod((length - top), 168)
        bottom = length - 130
        for y in range(top, bottom, 168):
            Pylon((centerx, y), self.pylons, self.pylons)
            Cable((centerx, y), self.cables, self.cables)
            
    def update(self, dt):
        self.animations.update(dt)
        
    def add_chair(self, midbottom, direction):
        """Add a single chair to the chairlift."""
        centerx, bottom = midbottom
        if direction == "up":
            x_offset = 18
            destination = self.top_lifthut.rect.bottom + 10 
            distance = bottom - destination
            klass = UpChair
        elif direction == "down":
            x_offset = -19
            destination = self.bottom_lifthut.rect.top + 70
            distance = destination - bottom
            klass = DownChair
        duration = distance * 30
        chair = klass((centerx + x_offset, bottom), self.chairs)
        ani = Animation(bottom=destination, duration=duration, round_values=True)
        opposite = "up" if direction == "down" else "down"
        ani.start(chair.rect)
        ani.callback = chair.kill
        task = Task(self.recycle_chair, interval=duration, args=(opposite,))
        self.animations.add(ani, task)
        
    def add_chairs(self):
        """Add enough chairs to "fill" the chairlift."""
        self.chair_space = space = 200
        centerx = self.top_lifthut.rect.centerx
        bottom = self.top_lifthut.rect.bottom + (space // 2)
        finish = self.bottom_lifthut.rect.top - (space // 2)
        for y in range(bottom, finish, space):
            self.add_chair((centerx, y), "up")
            self.add_chair((centerx, y), "down")
            
    def recycle_chair(self, direction):
        """
        Replaces a chair that has reached its destination with a chair
        heading in the opposite direction.
        """
        if direction == "up":
            start = self.bottom_lifthut.rect.top + 70
        else:
            start = self.top_lifthut.rect.bottom - 10
        centerx = self.top_lifthut.rect.centerx    
        self.add_chair((centerx, start), direction)
            
    def draw(self, surface, offset):
        for chair in self.chairs:
            chair.draw(surface, offset)
        for cable in self.cables:    
            cable.draw(surface, offset)
        self.top_lifthut.draw(surface, offset)
        self.bottom_lifthut.draw(surface, offset)
            


