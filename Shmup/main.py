# Shmup! - shoot game
import pygame as pg
import random
from settings import *
from sprite import *
from os import path
from pathlib import Path

class Game:
    def __init__(self):
        super().__init__()
        # initialize a game window
        pg.init( )
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        
        self.load_data()

    def load_data(self):
        # load resources

        self.dir = path.dirname(__file__)
        # set image dir
        self.img_dir = path.join(path.dirname(__file__), 'img')
        self.life_image = pg.image.load(Path(path.join(self.img_dir, 'PNG/UI/playerLife3_red.png')).as_posix())
        self.bg_image = pg.image.load(Path(path.join(self.img_dir, 'Backgrounds/darkpurple.png')).as_posix())

        # set sound dir
        self.snd_dir = path.join(path.dirname(__file__), 'snd')
        self.shoot_sound = pg.mixer.Sound(Path(path.join(self.snd_dir, 'Laser_Shoot.wav')).as_posix())
        self.explode_sound = pg.mixer.Sound(Path(path.join(self.snd_dir, 'Explosion.wav')).as_posix())
        self.die_sound = pg.mixer.Sound(Path(path.join(self.snd_dir, 'rumble.wav')).as_posix())
        
        # load highscore
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0


    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.player = Player(self)  
        for i in range(8):
            Mob(self)
        self.pow_timer = pg.time.get_ticks()
        self.run()

    def run(self):
        # Game Loop
        pg.mixer.music.load(Path(path.join(self.snd_dir, '10 - The Empire.mid')).as_posix())
        pg.mixer.music.play(loops = -1)
        pg.mixer.music.set_volume(0.4)
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

        # spawn a powerup
        now = pg.time.get_ticks()
        if now - self.pow_timer > 5000:
            self.pow_timer = now
            Pow(self, choice(['shield', 'double_shoot']))

        # check to see if a powerup hit the player
        hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for hit in hits:
            if hit.pow_type == 'shield':
                self.player.shield += 25
                if self.player.shield > 100:
                    self.player.shield = 100
            if hit.pow_type == 'double_shoot':
                self.player.shoot_type = 'double_shoot'

        # check to see if bullets hit mobs 
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, True, True)
        for hit in hits:
            self.score += 50 - hit.radius
            Mob(self)
            Explosion(self, hit.rect.centerx, hit.rect.centery, 'lg' if hit.radius > 20 else 'sm')
            self.explode_sound.play()

        # check to see if a mob hit the player
        hits = pg.sprite.spritecollide(self.player, self.mobs, True, pg.sprite.collide_circle)
        for hit in hits:
            self.player.shield -= hit.radius*2
            Mob(self)
            Explosion(self, hit.rect.centerx, hit.rect.centery, 'sm')
            self.explode_sound.play()
            if self.player.shield <= 0:
                self.player_expl = Explosion(self, self.player.rect.centerx, self.player.rect.centery, 'gt')
                self.die_sound.play()
                self.player.lives -= 1
                self.player.shield = 100
                self.player.hide()
        
        if self.player.lives <= 0 and not self.player_expl.alive():
            self.playing = False
        
    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game Loop -draw

        # draw background
        self.screen.fill(BLACK)
        self.bg_rect = self.bg_image.get_rect() 
        i = 0
        while i*self.bg_rect.width < WIDTH:
            j = 0    
            while j*self.bg_rect.height < HEIGHT:
                self.bg_rect.x = i*self.bg_rect.width
                self.bg_rect.y = j*self.bg_rect.height
                self.screen.blit(self.bg_image, self.bg_rect)
                j += 1   
            i += 1
            
     
        # draw sprite
        self.all_sprites.draw(self.screen)

        # draw text
        self.draw_text(str(self.score), 22, WHITE, WIDTH/2, 20)

        # draw shield
        self.draw_shield_bar(5, 5, self.player.shield)

        # draw lives
        self.draw_lives(WIDTH-150, 15)

        # *after* drawing everything , flip the display
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def draw_lives(self, x, y):
        for i in range(self.player.lives):
            rect = self.life_image.get_rect()
            rect.x = x + 40*i
            rect.y = y
            self.screen.blit(self.life_image, rect)

    def draw_shield_bar(self, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (pct / 100) * BAR_LENGTH
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        pg.draw.rect(self.screen, GREEN, fill_rect)
        pg.draw.rect(self.screen, WHITE, outline_rect, 2)

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

    def show_start_screen(self):
        # game splash/start screen
                # game splash/start screen
        pg.mixer.music.load(Path(path.join(self.snd_dir, '01 - Opening.mid')).as_posix())
        pg.mixer.music.play(loops = -1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Arrows to move, Space to shoot", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH/2, HEIGHT*3/4)
        self.draw_text("High Score:"+str(self.highscore), 22, WHITE, WIDTH/2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        # game over/continue
            # game over/continue
        if not self.running:
            return 

        pg.mixer.music.load(Path(path.join(self.snd_dir, '01 - Opening.mid')).as_posix())
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

g=  Game()
g.show_start_screen()
while g.running:
     g.new()
     g.show_go_screen()