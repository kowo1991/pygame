# Jumpy! - platform game
import  pygame as pg
import random
from os import path
from pathlib import Path
from settings import *
from sprite import *
from tilemap import *

# HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct*BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        super().__init__()
        # initialize a game window
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.running = True
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir, 'img')
        self.map_dir = path.join(self.dir, 'map')
        #self.map = Map(path.join(self.dir, 'map2.txt'))
        self.map = TiledMap(Path(path.join(self.map_dir, 'level1.tmx')).as_posix())
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(Path(path.join(self.img_dir, PLAYER_IMAGE)).as_posix())
        self.mob_img = pg.image.load(Path(path.join(self.img_dir, MOB_IMAGE)).as_posix())

        self.wall_img = pg.image.load(Path(path.join(self.img_dir, WALL_IMAGE)).as_posix())
        self.wall_img = pg.transform.smoothscale(self.wall_img, (TITLE_SIZE, TITLE_SIZE))
    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group() 
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group( )
        '''
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
        '''
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x,tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'zombie':
                Mob(self, tile_object.x, tile_object.y)

        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    def update(self):
        # Game loop - Update
        self.all_sprites.update() 
        self.camera.update(self.player)

        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0,0)

        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0,0)
            if self.player.health <= 0:
                self.playing = False
        
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
              self.quit()
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug

    def quit(self):
        if self.playing:
            self.playing = False
            self.running = False

    def draw(self):
        # Game Loop -draw
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        #self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug: 
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)


        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)

        # *after* drawing everything , flip the display
        pg.display.flip()


    def draw_grid(self):
        # draw vertical line
        for x in range(0, WIDTH, TITLE_SIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        # draw horizontal line
        for y in range(0, HEIGHT, TITLE_SIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
        
    def show_start_screen(self):
        # game splash/start screen
        pass
    def show_go_screen(self):
        # game over/continue
        pass

g=  Game()
g.show_start_screen()
while g.running:
     g.new()
     g.show_go_screen()