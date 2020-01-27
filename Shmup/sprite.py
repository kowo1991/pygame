from random import randrange, choice
from settings import *
import pygame as pg
from os import path
from pathlib import Path

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        super().__init__(self.groups)

        self.game = game
        '''
        self.shoot_types = {'normal_shoot':0,
                            'double_shoot':1}
        '''

        self.image = pg.image.load(Path(path.join(self.game.img_dir,'PNG/playerShip3_red.png')).as_posix())
        rect = self.image.get_rect()
        scale = 0.5
        self.image = pg.transform.smoothscale(self.image, (round(rect.width*scale), round(rect.height*scale)))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT -10
        self.radius = self.rect.height//2
        self.shield = 100
        self.shoot_delay = 250
        self.shoot_type = 'normal_shoot'
        self.shoot_duration = 5000
        self.shoot_timer = pg.time.get_ticks()

        self.last_shot = pg.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()
        self.vx = 0

    def update(self):
        # unhide if hidden
        if self.hidden and pg.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT -10

        # reset shoot type to normal
        now = pg.time.get_ticks()
        if now-self.shoot_timer > 5000:
            self.shoot_timer = now
            self.shoot_type = 'normal_shoot'

        self.vx = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.vx = -5
        if keystate[pg.K_RIGHT]:
            self.vx = 5
        if keystate[pg.K_SPACE]:
            self.shoot()
        
        self.rect.x += self.vx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def set_shoot_type(self, shoot_type):
        self.shoot_type = shoot_type
        self.shoot_timer = pg.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def shoot(self):
        now = pg.time.get_ticks()
        if now-self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.shoot_type == 'normal_shoot':
                Bullet(self.game, self.rect.centerx, self.rect.top)
            if self.shoot_type == 'double_shoot':
                Bullet(self.game, self.rect.centerx-15, self.rect.top)
                Bullet(self.game, self.rect.centerx+15, self.rect.top)
            self.game.shoot_sound.play()


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, x, y):  
        self.groups = game.all_sprites, game.bullets
        super().__init__(self.groups)
        self.game = game
      
        images = [  'PNG/Lasers/laserRed01.png',
                    'PNG/Lasers/laserBlue01.png',]
        self.image = pg.image.load(Path(path.join(self.game.img_dir, images[0])).as_posix())
        rect = self.image.get_rect()
        scale = 1
        self.image = pg.transform.smoothscale(self.image, (round(rect.width*scale), round(rect.height*scale)))


        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.vy = -10
    
    def update(self):
        self.rect.y += self.vy
        # kill if a bullet moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.mobs
        super().__init__(self.groups)
        self.game = game
   
        images = [  'PNG/Meteors/meteorBrown_big1.png',
                    'PNG/Meteors/meteorBrown_big2.png',
                    'PNG/Meteors/meteorBrown_big3.png',
                    'PNG/Meteors/meteorBrown_big4.png',
                    'PNG/Meteors/meteorBrown_med1.png',
                    'PNG/Meteors/meteorBrown_med3.png',
                    'PNG/Meteors/meteorBrown_small1.png',
                    'PNG/Meteors/meteorBrown_small2.png',
                    'PNG/Meteors/meteorBrown_tiny1.png',
                    'PNG/Meteors/meteorBrown_tiny2.png']
                            

        self.image = pg.image.load(Path(path.join(self.game.img_dir,choice(images))).as_posix())
        rect = self.image.get_rect()
        scale = 1
        self.image = pg.transform.smoothscale(self.image, (round(rect.width*scale), round(rect.height*scale)))
        self.image_orig = self.image

        self.rect = self.image.get_rect()
        self.rect.x = randrange(WIDTH-self.rect.width)
        self.rect.y = randrange(-100, -40)
        self.radius = self.rect.height//2
        #pg.draw.circle(self.image, RED, (self.rect.width//2,self.rect.height//2), self.radius)

        self.vx = randrange(-3, 3)
        self.vy = randrange(1,8)
        self.rot= 0
        rot_rng = round(200/self.rect.width)
        self.rot_speed = randrange(-rot_rng, rot_rng)
        self.last_update = pg.time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.top > HEIGHT + 10 \
            or self.rect.left < -self.rect.width \
            or self.rect.left > WIDTH:   
            self.rect.x = randrange(WIDTH-self.rect.width)
            self.rect.y = randrange(-100, 40)
            self.vy = randrange(1,8)

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot+self.rot_speed) % 360
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


class Pow(pg.sprite.Sprite):
    def __init__(self, game, pow_type):
        self.groups = game.all_sprites, game.powerups
        super().__init__(self.groups)
        self.game = game
        pow_types = {   'shield': 0, 
                        'double_shoot':1}
        self.pow_type = pow_type

        images = [  'PNG/Power-ups/pill_red.png',
                    'PNG/Power-ups/bolt_bronze.png']
                            

        self.image = pg.image.load(Path(path.join(self.game.img_dir, images[pow_types[self.pow_type]])).as_posix())
        rect = self.image.get_rect()
        scale = 1
        self.image = pg.transform.smoothscale(self.image, (round(rect.width*scale), round(rect.height*scale)))
        self.image_orig = self.image

        self.rect = self.image.get_rect()
        self.rect.x = randrange(WIDTH-self.rect.width)
        self.rect.y = randrange(-100, -40)
        self.radius = self.rect.height//2
        #pg.draw.circle(self.image, RED, (self.rect.width//2,self.rect.height//2), self.radius)  
        self.vy = randrange(2,5)


    def update(self):
        self.rect.y += self.vy
        if self.rect.top > HEIGHT + 10 \
            or self.rect.left < -self.rect.width \
            or self.rect.left > WIDTH:   
            self.kill()


class Explosionsheet:
    # utitlity class for loading and parsinig spritesheets
    def __init__(self, filename):
        self.explosionsheet = pg.image.load(filename).convert()

    def get_image(self, idx):
        # grab an image out of a larger spritesheet
        width = 111
        height = 109
        image = pg.Surface((width, height))
        image.blit(self.explosionsheet, (0,0), (idx*width,0,width, height))
        image = pg.transform.scale(image, (width, height))
        return image

class Explosion(pg.sprite.Sprite):
    def __init__(self, game, x, y, size):
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.size = size
        self.explosionsheet = Explosionsheet(Path(path.join(self.game.img_dir, 'PNG/explosionBig.png')).as_posix())
        self.explosion_anim = {}
        self.explosion_anim['lg'] = []
        self.explosion_anim['sm'] = []
        self.explosion_anim['gt'] = []
        for i in range(16):
            image = self.explosionsheet.get_image(i)
            rect = image.get_rect()
            image.set_colorkey(BLACK)
            self.explosion_anim['lg'].append(image)
            image = pg.transform.smoothscale(image, (rect.width//2, rect.height//2))
            self.explosion_anim['sm'].append(image)
            image = pg.transform.smoothscale(image, (rect.width*3//2, rect.height*3//2))
            self.explosion_anim['gt'].append(image)
        self.curr_frame = 0
        self.image = self.explosion_anim[self.size][self.curr_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #self.rect.center = (WIDTH//2, HEIGHT//2)
        self.last_update = pg.time.get_ticks()
    def update(self):
        self.animate()

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 30:
            self.last_update = now
            self.curr_frame += 1
            if self.curr_frame == len(self.explosion_anim[self.size])-1:
                self.kill()
            self.image = self.explosion_anim[self.size][self.curr_frame]

