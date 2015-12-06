import pygame as pg

import prepare
from obstacles import Tree, RightGate, LeftGate, Jump, Rock
from obstacles import GreenSign, BlueSign, BlackSign, Pylon
from chairlift import ChairLift


class Course(object):
    def __init__(self, course_info):
        self.map_name = course_info["map_name"]
        self.map_size = course_info["map_size"]
        self.map_rect = pg.Rect((0, 0), self.map_size)
        self.view_rect = prepare.SCREEN_RECT.copy()
        self.class_map = {"tree": Tree,
                             "rightgate": RightGate,
                             "leftgate": LeftGate,
                             "jump": Jump,
                             "rock": Rock,
                             "greensign": GreenSign,
                             "bluesign": BlueSign,
                             "blacksign": BlackSign,
                             "pylon": Pylon
                             }
        self.chairlift = ChairLift(self.map_size)
        self.obstacles = pg.sprite.Group()
        self.gates = pg.sprite.Group()
        self.load_from_info(course_info)
        self.make_sections()
    
    def make_sections(self, split_num=1000):
        """Divide the obstacles into different sections to avoid unnecessary collision checks."""
        self.obstacles.add(self.chairlift.pylons.sprites())
        num = max(1, int(len(self.obstacles) / split_num))
        section_length = int(self.map_size[1] / num)
        self.sections = {}
        for y in range(0, self.map_size[1], section_length):
            rect_info = (0, y, self.map_size[0], section_length)
            rect = pg.Rect(rect_info)
            self.sections[rect_info] = pg.sprite.Group([x for x in self.obstacles if rect.collidepoint(x.rect.midbottom)])

    def get_section_sprites(self):
        """Return sprites from sections that collide with self.view_rect."""
        visible = set()
        for rect_info in self.sections:
            if pg.Rect(rect_info).colliderect(self.view_rect):
                visible.update(self.sections[rect_info])
        return visible
        
    def load_from_info(self, course_info):
        """Instantiate course objects from course_info, a dict loaded from JSON."""
        for item in course_info["obstacles"]:
            klass = self.class_map[item[0].lower()]
            midbottom = item[1]
            obstacle = klass(midbottom, self.obstacles)
            if "gate" in item[0].lower():
                self.gates.add(obstacle)            
    
    def reset(self):
        """Get course ready for player to take another run down the slope."""
        for gate in self.gates:
            gate.reset()
            
    def update(self, dt, boarder):
        self.chairlift.update(dt)
        self.view_rect.center = boarder.rect.center
        self.view_rect.clamp_ip(self.map_rect)
        self.gates.update(boarder)
        self.collidables = {x for x in self.get_section_sprites() if x.rect.colliderect(self.view_rect)}
        for collidable in (c for c in self.collidables if c.collider.colliderect(boarder.collider)):
            collidable.collide_with_boarder(boarder)
        if boarder.collider.colliderect(self.chairlift.bottom_lifthut.rect):
            boarder.reset((self.map_rect.centerx, 50))
            self.reset()

    def draw(self, surface, boarder=None):
        offset = -self.view_rect.left, -self.view_rect.top
        if boarder:
            self.collidables.add(boarder)
            onscreen = self.collidables
        else:
            onscreen = {x for x in self.get_section_sprites() if x.rect.colliderect(self.view_rect)}
        for obstacle in sorted(onscreen, key=lambda x: x.collider.bottom):
            obstacle.draw(surface, offset)            
        self.chairlift.draw(surface, offset)    
