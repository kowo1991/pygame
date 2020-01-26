# Jumpy! (a platform game)
# Art from kenney.nl
# attempt by https://opengameart.org/content/summer-park-8bit-tune-loop
# Salt Marsh Birds by https://opengameart.org/content/salt-marsh-birds-cuteplayful
import pygame as pg
import random
from settings import *
from sprites import *
from os import path
from pathlib import Path

class Game:
    def __init__(self):
        super().__init__()
        # initialize a game window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
    
    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        
        with open(path.join(self.dir, HS_FILE),'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        # load spritesheet image
        self.img_dir= path.join(self.dir, 'img')
        self.spritesheet = Spritesheet(Path(path.join(self.img_dir, SPSRITESHEET)).as_posix())

        # cload images
        self.cloud_images = []
        for i in range(1,4):
            self.cloud_images.append(pg.image.load(Path(path.join(self.img_dir, 'PNG/extra/cloud{}.png'.format(i))).as_posix()).convert())

        # load sounds
        self.snd_dir = path.join(self.dir, 'snd') 
        print (Path(path.join(self.snd_dir, 'Jump12.wav')).as_posix())
        self.jump_sound = pg.mixer.Sound(Path(path.join(self.snd_dir, 'Jump12.wav')).as_posix())
        self.boost_sound = pg.mixer.Sound(Path(path.join(self.snd_dir, 'Powerup2.wav')).as_posix())

    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.player = Player(self)

        for plat in PLAtFORM_LIST:
            Platform(self, *plat)

        for i in range(6):
            c = Cloud(self)
            c.rect.y += 500
        self.mob_timer = 0   
        self.topest_platform = Platform(self, *PLAtFORM_LIST[-1])

        self.run()

    def run(self):
        # Game Loop
        pg.mixer.music.load(Path(path.join(self.snd_dir, 'Salt Marsh Birds.mp3')).as_posix())
        pg.mixer.music.play(loops = -1)
        self.playing = True
        while self.playing:
                self.clock.tick(FPS)
                self.events()
                self.update()
                self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):
        # Game loop - Update   
        self.all_sprites.update()

        # spawn a mob
        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000+random.choice([-1000,1000]):
            self.mob_timer = now
            Mob(self)

        # hit mobs?
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        if mob_hits:
            self.playing = False

        # check if a player hit a platform when falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False, pg.sprite.collide_mask)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.y < lowest.rect.centery and \
                   self.player.pos.x > lowest.rect.left and \
                   self.player.pos.x < lowest.rect.right:
                    self.player.pos.y = lowest.rect.top
                    self.player.vel.y = 0
                    self.player.jumping = False

        # if player reaches top 1/4 of screen
        if self.player.rect.top <= HEIGHT/4:
            if random.randrange(100) < 5:
                Cloud(self)

            self.player.pos.y += max(abs(self.player.vel.y),2)
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y),2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y),2)
                if plat.rect.top > HEIGHT:
                    plat.kill()
                    self.score += 20
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y),2)
                if mob.rect.y > HEIGHT:
                    mob.kill()
        # if player hits powerup
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.player.vel.y = -BOOST_POWERUP
                self.player.jumping = False
                self.boost_sound.play()

        # Die!
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False


        # update topest platform
        for plat in self.platforms:
            if plat.rect.y < self.topest_platform.rect.y:
                self.topest_platform = plat

        # spawn new platforms to keep same average number
        while len(self.platforms) < 6:
            width = random.randrange(50,100)
            Platform(self, random.randrange(0, WIDTH-width),
                     random.randrange(-250+self.topest_platform.rect.y, -100+self.topest_platform.rect.y))

        
        
    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        # Game Loop -draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        #self.screen.blit(self.player.image, self.player.rect)
        self.draw_text(str(self.score), 22, WHITE, WIDTH/2, 15)
        # *after* drawing everything , flip the display
        pg.display.flip()
    def show_start_screen(self):
        # game splash/start screen
        pg.mixer.music.load(Path(path.join(self.snd_dir, '8bit attempt.ogg')).as_posix())
        pg.mixer.music.play(loops = -1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH/2, HEIGHT*3/4)
        self.draw_text("High Score:"+str(self.highscore), 22, WHITE, WIDTH/2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)
    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return 

        pg.mixer.music.load(Path(path.join(self.snd_dir, '8bit attempt.ogg')).as_posix())
        pg.mixer.music.play(loops = -1)
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Score:"+str(self.score), 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH/2, HEIGHT*3/4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH/2, HEIGHT/2+40)
            with open(path.join(self.dir,HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("Highest score:"+str(self.highscore), 22, WHITE, WIDTH/2, HEIGHT/2+40)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def draw_text(self, text ,size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False 

g=  Game()
g.show_start_screen()
while g.running:
     g.new()
     g.show_go_screen()
pg.quit()