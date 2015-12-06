import os
import json

import pygame as pg

import tools
import prepare
from state_engine import GameState
from labels import Button, ButtonGroup
from course import Course
from obstacles import Tree, Rock, RightGate, LeftGate, Jump
from obstacles import GreenSign, BlueSign, BlackSign


class Editor(GameState):
    """Allows the user to edit a course."""
    def __init__(self):
        super(Editor, self).__init__()
        self.next_state = "MAIN_MENU"

    def startup(self, persistent):
        """Creates a Course object from the previously selected JSON file."""
        self.persist = persistent
        name = self.persist["course_name"]
        filepath = os.path.join("resources", "courses", "{}.json".format(name))
        with open(filepath, "r") as f:
            course_info = json.load(f)
        self.course = Course(course_info)
        self.scroll_speed = .25
        self.view_center = list(self.course.view_rect.center)
        
    def save_to_json(self):
        """Saves location of all course objects to be loaded for future use."""
        course_info = {
                "map_name": self.course.map_name,
                "map_size": self.course.map_size,
                "obstacles": [[x.name, x.rect.midbottom] for x in self.course.obstacles]
                }
        
        filepath = os.path.join("resources", "courses", "{}.json".format(self.course.map_name))
        with open(filepath, "w") as f:
            json.dump(course_info, f)
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.save_to_json()
            self.done = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.save_to_json()
                self.done = True
        
    def scroll(self, dt, mouse_pos):
        """Move the view rect when the mouse is at the edge of the screen."""
        speed = self.scroll_speed * dt
        x, y = mouse_pos
        w, h = prepare.SCREEN_SIZE
        if x < 20:
            self.view_center[0] -= speed
        elif x > w - 20:
            self.view_center[0] += speed
        if y < 20:
            self.view_center[1] -= speed
        elif y > h - 20:
            self.view_center[1] += speed  
        self.course.view_rect.center = self.view_center
        
    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        self.scroll(dt, mouse_pos)        
        
    def draw(self, surface):
        surface.fill(pg.Color(242, 255, 255))
        self.course.draw(surface)
