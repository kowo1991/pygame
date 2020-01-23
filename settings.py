# game options/settings
TITLE="Jumpy!"
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'
HS_FILE = 'highscore.txt'
SPSRITESHEET = 'Spritesheets/spritesheet_jumper.png'

#Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

# Game properties
BOOST_POWERUP = 60
POW_SPAWN_PCT = 7
MOB_FREQ = 5000
PLAYER_LAYER = 2
PLAtFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = 0


# Starting platforms
PLAtFORM_LIST = [(0,HEIGHT-40),
                (WIDTH/2-50, HEIGHT*3/4),
                (125, HEIGHT-350),
                (350, 200),
                (175, 100)]

# define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0,0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
LIGHTBLUE = (0, 155, 155)
BRIGHTBLUE = (0, 128, 255)
BGCOLOR = BRIGHTBLUE