import os
from random import choice, sample
import pygame as pg
import tools


SCREEN_SIZE = (1280, 720)
ORIGINAL_CAPTION = "Snowboarding"

pg.mixer.pre_init(44100, -16, 1, 512)

pg.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
pg.display.set_caption(ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

GFX = tools.load_all_gfx(os.path.join("resources", "graphics"))
SFX = tools.load_all_sfx(os.path.join("resources", "sounds"))
MUSIC = tools.load_all_music(os.path.join("resources", "music"))

SFX["elfgrunt"].set_volume(.5)
SFX["edgegrind"].set_volume(.4)


def make_chair_images():
    """Create different colored variations of chairlift rider images."""
    #colors for each potential rider in the original image 
    original_colors = {
        "hat": [(0, 38, 255), (72, 0, 255), (255, 0, 220)],
        "hair": [(255, 189, 0), (76, 255, 0), (0, 255, 33)],
        "skin": [(191, 84, 33), (255, 178, 127), (104, 41, 0)],
        "shirt": [(1, 127, 15), (255, 0, 0), (255, 106, 0)],
        "pants": [(0, 148, 255), (0, 74, 127), (0, 127, 127)],
        "board": [(127, 0, 0), (127, 51, 0), (127, 106, 0)]}
    chairs = []
    skin_tones = tools.strip_from_sheet(GFX["skin-palette"], (0, 0), (16, 16), 3)    
    skin_colors = [img.get_at((0, 0)) for img in skin_tones]         
    hair_tones = tools.strip_from_sheet(GFX["hair-palette"], (0, 0), (16, 16), 4)
    hair_colors = [hair.get_at((0, 0)) for hair in hair_tones]
    elf_tones = tools.strip_from_sheet(GFX["elf-palette"], (0, 0), (16, 16), 15)
    elf_colors = [elf.get_at((0, 0)) for elf in elf_tones]
    originals = [GFX["upchair{}".format(x)] for x in range(1, 4)]
    names = ("skin", "hair", "hat", "shirt", "pants", "board")
    for original in originals:
        for _ in range(10):
            swap_dict = {}
            for i in range(3):
                old_colors = [original_colors[name][i] for name in names]             
                new_colors = [choice(skin_colors), choice(hair_colors)]
                new_colors.extend(sample(elf_colors, 4))
                swap_dict.update(zip(old_colors, new_colors))
            chairs.append(tools.color_swap(original, swap_dict))   
    return chairs
    
CHAIRS = make_chair_images()    