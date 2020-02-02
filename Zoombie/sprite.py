import pygame as pg
from random import uniform, choice, randint, random
import pytweening as tween
from settings import *
from tilemap import collide_hit_rect
vec = pg.math.Vector2


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx - sprite.hit_rect.centerx > 0:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            else:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2   
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery - sprite.hit_rect.centery > 0:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            else:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups  = game.all_sprites
        super().__init__(self.groups)
        self._layer = PLAYER_LAYER
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.rect.center = (x ,y)
        self.hit_rect.center = self.rect.center
        self.vel = vec(0,0)
        self.pos = vec(x,y) 
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH

    def set_pos(self, x ,y):
        self.pos.x = x
        self.pos.y = y

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
            #self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
            #self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
            #self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(- PLAYER_SPEED / 2, 0).rotate(-self.rot)

        if keys[pg.K_SPACE]:

            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:            
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                Bullet(self.game, self.pos + BARREL_OFFSET.rotate(-self.rot), dir)
                self.vel = vec(-KICKBACK,0).rotate(-self.rot)
                MuzzleFlash(self.game, self.pos+BARREL_OFFSET.rotate(-self.rot))
                self.game.gun_sounds['cg1'].play()
        if self.vel != (0, 0):
            self.vel *= 0.7071

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        center = self.rect.center
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.pos += self.vel*self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x ,y):
        self._layer = WALL_LAYER
        self.groups = game.walls
        super().__init__(self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x*TITLE_SIZE
        self.rect.y = self.y*TITLE_SIZE
        
class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x ,y, w, h):
        self.groups = game.walls
        super().__init__(self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        super().__init__(self.groups)
        self.game = game
        self.image = game.mob_img.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.speed = choice(MOB_SPEED)
        self.target = game.player

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width*self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0,0,width,7)
        if self.health < 100:
            pg.draw.rect(self.image, col, self.health_bar)

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < DETECT_RADIUS**2:
            if random() < 0.002:
                choice(self.game.zombie_moan_sounds).play()
            self.rot = target_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += -1 * self.vel
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5*self.acc*self.game.dt**2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
            if self.health < 0:
                self.kill()


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        super().__init__(self.groups)
        self.game = game
        self.image = pg.Surface((10,10))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        pg.draw.circle(self.image, DARKGREY, (5,5),3)
        pg.draw.circle(self.image, WHITE, (5,5),5,1)
        self.hit_rect = self.rect
        self.pos = vec(pos)
        spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.rect.center = pos
        self.vel = dir.rotate(spread )*BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()
    
    def update(self):
        self.pos += self.vel*self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()
        pg.draw.circle(self.image, WHITE, (0,0),100,20)


class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        size = randint(30, 45)
        self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
      
        self._layer = ITEM_LAYER
        self.groups = game.all_sprites, game.items
        super().__init__(self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.pos = pos
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir  = 1

    def update(self):
        # bobbing motion
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset*self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1
