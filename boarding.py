import os
from random import choice
import json
import pygame as pg

import prepare, tools
from state_engine import GameState
from course import Course
from snowboarder import Snowboarder


class Boarding(GameState):
    def __init__(self):
        super(Boarding, self).__init__()
    
    def startup(self, persistent):
        self.persist = persistent
        name = self.persist["course_name"]
        filepath = os.path.join("resources", "courses", "{}.json".format(name))
        with open(filepath, "r") as f:
            course_info = json.load(f)
        self.course = Course(course_info)
        x, y = self.course.map_rect.centerx, 50
        self.player = Snowboarder((x, y))
        pg.mouse.set_visible(False)
        pg.mixer.music.load(prepare.MUSIC["wind"])
        pg.mixer.music.set_volume(.7)
        pg.mixer.music.play(-1)
        
    def get_event(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.done = True
                self.next_state = "MAIN_MENU"
                pg.mouse.set_visible(True)
                pg.mixer.music.fadeout(3000)
                
    def update(self, dt):
        keys = pg.key.get_pressed()
        self.player.update(dt, keys, self.course.map_rect)
        self.course.update(dt, self.player)
        
    def draw(self, surface):
        surface.fill(pg.Color(242, 255, 255))
        self.course.draw(surface, self.player)    
  