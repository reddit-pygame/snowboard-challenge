from itertools import cycle

import pygame as pg

from prepare import GFX, SFX
from animation import Task


class Snowboarder(pg.sprite.Sprite):
    """A snowboarding elf controlled by the player."""
    image_dict = {
            "brake": {
                    "left": cycle([GFX["leftboardbrake{}".format(x)] for x in (1,2,3)]),                        
                    "right": cycle([GFX["rightboardbrake{}".format(x)] for x in (1,2,3)]),
                    "down": cycle([GFX["downboardbrake1"]])},
            "no brake": {
                    "left": cycle([GFX["leftboard{}".format(x)] for x in (1,2,3)]),                                
                    "right": cycle([GFX["rightboard{}".format(x)] for x in (1,2,3)]),
                    "down": cycle([GFX["downboard{}".format(x)] for x in (1,2,3)])},
            "crash": {"down": cycle([GFX["crash{}".format(x)] for x in range(1, 6)])}}
    
    def __init__(self, midbottom, *groups):
        super(Snowboarder, self).__init__(*groups)
        self.xpos, self.ypos = midbottom
        self.state = "no brake"
        self.direction = "left"
        self.max_speed = .3
        self.x_velocity = 0
        self.y_velocity = 0
        self.crashed = False
        self.crash_count = 0
        self.controls = {"left": pg.K_LEFT,
                                "right": pg.K_RIGHT,
                                "down": pg.K_DOWN,
                                "braking": pg.K_SPACE}
        self.acceleration = {"left": False,
                                     "right": False,
                                     "down": False,
                                     "braking": False}
        self.collider_sizes = {"left": (12, 2),
                                        "right": (12, 2),
                                        "braking": (12, 2),
                                        "down": (4, 12)}
        self.images = self.image_dict[self.state][self.direction]
        self.image = next(self.images)
        self.rect = self.image.get_rect(midbottom=(self.xpos, self.ypos))
        self.collider = pg.Rect((0, 0), self.collider_sizes[self.direction])
        self.collider.midbottom = self.rect.midbottom
        self.spray_images = cycle([GFX["spray{}".format(x)] for x in (1,2,3)])
        self.spray_image = next(self.spray_images)
        self.spray_rect = self.spray_image.get_rect()
        self.grunt = SFX["elfgrunt"]
        self.glide = SFX["edgegrind"]
        self.glide.set_volume(.3)
        self.animations = pg.sprite.Group()
        task = Task(self.flip_image, 150, -1)
        self.animations.add(task)
        
    def reset(self, midbottom):
        """Get ready for another run down the mountain."""
        self.xpos, self.ypos = midbottom
        self.x_velocity = 0
        self.y_velocity = 0
        self.rect.midbottom = midbottom
        self.collider.midbottom = midbottom
        self.state = "no brake"
        self.direction = "left"
        self.change_image()
        
    def update(self, dt, keys, map_rect):
        self.animations.update(dt)
        last_state = self.state
        last_direction = self.direction
        if self.state == "crash":
            if self.crash_count > 0:
                self.crash_count -= dt
                if self.x_velocity < 0:
                    self.x_velocity += .000625 * dt
                elif self.x_velocity > 0:
                    self.x_velocity -= .000625 * dt
            else:
                self.recover()
        else:
            self.process_keys(keys)
            self.accelerate(dt)
        
        self.move(dt)
        clamped = self.rect.clamp(map_rect)
        if clamped != self.rect:
            self.rect = clamped
            self.xpos, self.ypos = self.rect.midbottom
        if (self.direction != last_direction) or (self.state != last_state):
            self.change_image()   
            
    def move(self, dt):
        """Constrain player velocities and move accordingly."""
        self.x_velocity = min(self.max_speed, max(-self.max_speed, self.x_velocity))
        self.y_velocity = min(self.max_speed, max(0, self.y_velocity))
        self.xpos += self.x_velocity * dt
        self.ypos += self.y_velocity * dt
        self.rect.midbottom = self.xpos, self.ypos
        self.collider.midbottom = self.rect.midbottom
            
    def process_keys(self, keys):
        """Handle key events and play braking sound if braking."""
        moving = any((abs(vel) > self.max_speed * .1
                               for vel in (self.y_velocity, self.x_velocity)))
        if moving and keys[self.controls["braking"]]:
            glide_channel = pg.mixer.Channel(1)
            if not glide_channel.get_busy():
                glide_channel.play(self.glide)
            self.state = "brake"
        else:
            self.glide.stop()
            self.state = "no brake"
        for control in self.controls:
            self.acceleration[control] = keys[self.controls[control]]
        for direct in ("down", "left", "right"):
            if self.acceleration[direct]:
                self.direction = direct
                break
      
    def accelerate(self, dt):
        """Calculate elf's acceleration in diffferent directions."""
        try:   
            mod = -self.x_velocity / abs(self.x_velocity)
        except ZeroDivisionError:
            mod = 0
        brake_mod = not self.acceleration["braking"] #capitalizing on the fact that bools are ints
        accel_mods = {
                "left": (-.00035 * dt, -.00003 * dt),
                "right": (.00035 * dt, -.00003 * dt),
                "down": (.00003 * mod * dt, .0005 * dt * brake_mod),
                "braking": (.0001 * mod * dt, -.0002 * dt)}
        for accel_direction in accel_mods:
            if self.acceleration[accel_direction]:
                x, y = accel_mods[accel_direction]
                self.x_velocity += x
                self.y_velocity += y
        
    def crash(self, crash_count=1500):
        """Crash the player if they aren't already crashed."""
        if self.state != "crash":
            self.grunt.play()
            self.state = "crash"
            self.direction = "down"
            self.crash_count = crash_count
            self.x_velocity = -self.x_velocity / 2.0
            self.y_velocity = .0625
            for key in self.acceleration:
                self.acceleration[key] = False
            self.change_image()
                
    def recover(self):
        """Recover from a crash."""
        self.state = "no brake"
        self.x_velocity = 0
        self.y_velocity = 0
        self.direction = "left"

    def flip_image(self):
        """Switch to the next image in the animation cycle."""
        self.image = next(self.images)
        
    def change_image(self):
        """Switch to appropriate animation cycle."""
        self.images = self.image_dict[self.state][self.direction]
        if self.state == "brake":
            size = self.collider_sizes["braking"]
        else:
            size = self.collider_sizes[self.direction]
        self.rect = self.image.get_rect(midbottom=(self.xpos, self.ypos))
        self.collider = pg.Rect((0, 0), size)
        self.collider.midbottom = self.rect.midbottom
        self.flip_image()
          
    def draw(self, surface, offset):     
        surface.blit(self.image, self.rect.move(offset))
        if self.acceleration["braking"]:
            if any((abs(vel) > self.max_speed * .1 for vel in (self.y_velocity, self.x_velocity))):
                self.spray_rect.midbottom = (self.rect.centerx,
                                                             self.rect.bottom + 3)
                surface.blit(self.spray_image, self.spray_rect.move(offset))
        #pg.draw.rect(surface, pg.Color("blue"), self.rect.move(offset), 1)
        #pg.draw.rect(surface, pg.Color("red"), self.collider.move(offset))