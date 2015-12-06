import sys
import pygame as pg

from state_engine import Game, GameState
import prepare
import main_menu, course_selection_play, course_info_entry, editor, course_selection_edit, boarding

states = {"MAIN_MENU": main_menu.MainMenu(),
               "COURSE_SELECT_PLAY": course_selection_play.CourseSelectPlay(),
               "NEW_COURSE": course_info_entry.CourseInfoEntry(),
               "EDITOR": editor.Editor(),
               "COURSE_SELECT_EDIT": course_selection_edit.CourseSelectEdit(),
               "BOARDING": boarding.Boarding()}
game = Game(prepare.SCREEN, states, "MAIN_MENU")
game.run()
pg.quit()
sys.exit()