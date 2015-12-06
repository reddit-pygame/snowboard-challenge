import pygame as pg

from state_engine import GameState
from labels import Label, Button, ButtonGroup


class MainMenu(GameState):
    def __init__(self):
        super(MainMenu, self).__init__()
        self.make_buttons()
    
    def startup(self, persistent):
        self.persist = persistent
        
    def make_buttons(self):
        button_info = (
                ("Hit the Slopes", self.hit_the_slopes),
                ("Create Course", self.create_course),
                ("Edit Course", self.edit_course))
                               
        self.buttons = ButtonGroup()
        style = {"button_size": (350, 120),
                     "font_size": 64,
                    "fill_color": pg.Color(48, 75, 50),
                    "hover_fill_color": pg.Color(72, 96, 74),
                    "text_color": pg.Color("gray80"),
                    "hover_text_color": pg.Color("gray90")}
        w, h = style["button_size"]
        left = self.screen_rect.centerx - (w // 2)
        top = 100
        vert_space = 180 
        for text, callback in button_info:
            Button((left, top), self.buttons, text=text, 
                      hover_text=text, call=callback, **style)
            top += vert_space
    
    def create_course(self, *args):
        self.next_state = "NEW_COURSE"
        self.done = True
        
    def edit_course(self, *args):
        self.next_state = "COURSE_SELECT_EDIT"    
        self.done = True
        
    def hit_the_slopes(self, *args):
        self.next_state = "COURSE_SELECT_PLAY"
        self.done  = True
        
    def get_event(self, event):
        self.buttons.get_event(event)
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        
    def update(self, dt):
        self.buttons.update(pg.mouse.get_pos())
        
    def draw(self, surface):
        surface.fill(pg.Color(242, 255, 255))
        self.buttons.draw(surface)        
