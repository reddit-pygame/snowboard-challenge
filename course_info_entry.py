from collections import OrderedDict
from random import randint
import string
import os
import json


import pygame as pg

import prepare
from state_engine import GameState
from labels import Label, TextBox



class CourseInfoEntry(GameState):
    """Edit a course."""
    def __init__(self):
        super(CourseInfoEntry, self).__init__()
        
    def startup(self, persistent):
        self.persist = persistent
        self.textbox_rect = pg.Rect(0, 0, 600, 200)
        self.textbox_rect.center = prepare.SCREEN_RECT.center
        self.course_info = OrderedDict(
                    (("Course Name", None),
                    ("Course Width", None),
                    ("Course Length", None)))                                     
        self.textbox_style = {
                    "color": pg.Color(242, 255, 255),
                    "font_color": pg.Color(48, 75, 50),
                    "active_color": pg.Color(48, 75, 50),
                    "outline_color": pg.Color(72, 96, 74)} 
        self.textbox = TextBox(self.textbox_rect, **self.textbox_style)
        self.current_info = "Course Name"
        self.label_style = {"text_color": (48, 75, 50), "font_size": 48}
        
        w, h = prepare.SCREEN_SIZE
        self.prompt = Label("Enter {}".format(self.current_info), 
                                     {"midtop": (w//2, 20)}, **self.label_style)
        self.textbox.update()
                                          
    def leave_state(self, next_state):
        self.done = True
        self.next_state = next_state
        
    def get_event(self, event):
        self.textbox.get_event(event, pg.mouse.get_pos())
        if event.type == pg.QUIT:
            self.leave_state("MAIN_MENU")
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.leave_state("MAIN_MENU")
                
    def update(self, dt):
        self.textbox.update()
        if not self.textbox.active:
            self.course_info[self.current_info] = self.textbox.final
            for info in self.course_info:
                if self.course_info[info] is None:
                    self.textbox = TextBox(self.textbox_rect, **self.textbox_style)
                    self.current_info = info
                    if "Width" in info or "Length" in info:
                        self.textbox.accepted = string.digits
                    self.textbox.update()
                    self.prompt.set_text("Enter {}".format(self.current_info))
                    break
            else:
                self.make_course()
            
    def add_random_trees(self, map_size):
        trees = []
        w, h = map_size
        lift_rect = pg.Rect(0, 0, 150, h)
        lift_rect.centerx = w // 2
        num_trees = int(w * h * .0005)
        for _ in range(num_trees):
            while True:
                pos = randint(0, w), randint(0, h)
                if not lift_rect.collidepoint(pos):
                    trees.append(["tree", pos])
                    break
        return trees
            
    def make_course(self):        
        course_info = {}
        name = self.course_info["Course Name"]
        course_info["map_name"] = name
        course_info["map_size"] = (int(self.course_info["Course Width"]),
                                                   int(self.course_info["Course Length"]))
        obstacles = []
        trees = self.add_random_trees(course_info["map_size"])
        obstacles.extend(trees)
        course_info["obstacles"] = obstacles
       
        
        filepath = os.path.join("resources", "courses", "{}.json".format(name))
        with open(filepath, "w") as f:
            json.dump(course_info, f)
        self.done = True
        self.persist["course_name"] = name
        self.next_state = "EDITOR"
        
    def draw(self, surface):
        surface.fill(pg.Color(242, 255, 255))
        self.textbox.draw(surface)
        self.prompt.draw(surface)
