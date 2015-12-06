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
        
        #remove for challenge
        self.icons = ButtonGroup()
        icons = tools.strip_from_sheet(prepare.GFX["icon-strip"],
                                                       (0, 0), (48, 48), 8)   
        icon_classes = (Tree, Rock, RightGate, LeftGate, Jump,
                                GreenSign, BlueSign, BlackSign)
        left = 20
        top = 20
        for icon, klass in zip(icons, icon_classes):
            Button((left, top), self.icons, idle_image=icon, hover_image=icon,
                       call=self.set_current_object, args=klass)
            top += 54
        self.set_current_object(Tree)
        
    def set_current_object(self, klass):
        self.current_object = klass
        
    def add_object(self, screen_pos):        
        screenx, screeny  = screen_pos
        viewx, viewy = self.course.view_rect.topleft
        x, y = screenx + viewx, screeny + viewy
        sprite = self.current_object((x, y), self.course.obstacles)
        for rect_info in self.course.sections:
            if pg.Rect(rect_info).collidepoint(sprite.rect.midbottom):
                self.course.sections[rect_info].add(sprite)
        
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
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                if not any((x.rect.collidepoint(event.pos) for x in self.icons)):
                    self.add_object(event.pos)
            
        self.icons.get_event(event)
        
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
        if pg.mouse.get_pressed()[2]:
            mousex, mousey = mouse_pos
            viewx, viewy = self.course.view_rect.topleft
            x, y = mousex + viewx, mousey + viewy
            for sprite in self.course.obstacles:
                if sprite.rect.collidepoint((x, y)):
                    sprite.kill()
        self.scroll(dt, mouse_pos)
        self.icons.update(mouse_pos)
        
        
    def draw(self, surface):
        surface.fill(pg.Color(242, 255, 255))
        self.course.draw(surface)
        self.icons.draw(surface)