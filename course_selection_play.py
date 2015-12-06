import os

import pygame as pg

import tools
from state_engine import GameState
from labels import Label, Button, ButtonGroup


class CourseSelectPlay(GameState):
    def __init__(self):
        super(CourseSelectPlay, self).__init__()
        
    def startup(self, persistent):
        self.persist = persistent
        self.make_buttons()
        
    def make_buttons(self):
        self.buttons = ButtonGroup()
        style = {"button_size": (250, 80),
                    "fill_color": pg.Color(48, 75, 50),
                    "hover_fill_color": pg.Color(72, 96, 74),
                    "text_color": pg.Color("gray80"),
                    "hover_text_color": pg.Color("gray90")}
        course_dict = tools.load_all_courses(os.path.join("resources", "courses"))
        w, h = style["button_size"]
        left = self.screen_rect.centerx - (w // 2)
        top = 10
        vert_space = 100 
        for name in course_dict:
            Button((left, top), self.buttons, text=name.replace("-", " "), 
                      hover_text=name.replace("-", " "), call=self.load_course,
                      args=name, **style)
            top += vert_space
        
    def load_course(self, course_name):
        self.persist["course_name"] = course_name
        self.next_state = "BOARDING"
        self.done = True
        
    def leave_state(self, next_state):
        self.next_state = next_state
        self.done = True

    def get_event(self, event):
        self.buttons.get_event(event)
        if event.type == pg.QUIT:
            self.leave_state("MAIN_MENU")
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.leave_state("MAIN_MENU")
                
    def update(self, dt):
        self.buttons.update(pg.mouse.get_pos())
        
    def draw(self, surface):
        surface.fill(pg.Color(242, 255, 255))
        self.buttons.draw(surface)
