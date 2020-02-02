import pygame as pg
vec = pg.Vector2
#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTGREY = (100, 100, 100)
DARKGREY = (40, 40,40)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# game settings
WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "Zoombie"
BGCOLOR = LIGHTGREY
TITLE_SIZE = 64
GRIDWIDTH = WIDTH / TITLE_SIZE
GRIDHEIGHT = HEIGHT / TITLE_SIZE
WALL_IMAGE = 'PNG/Tiles/tile_171.png'

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_IMAGE = 'PNG/Man Blue/manBlue_gun.png'
PLAYER_HIT_RECT = pg.Rect(0,0,35,35)
BARREL_OFFSET = vec(30,10)
BULLET_DAMAGE = 10


# Mob settings
MOB_HEALTH = 100
MOB_IMAGE = 'PNG/Zombie 1/zoimbie1_hold.png'
MOB_SPEED = [150, 100, 75, 125]
MOB_HIT_RECT = pg.Rect(0,0,30,30)
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 400

# Gun settings
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150
KICKBACK = 200
GUN_SPREAD = 5

# Effects
MUZZLE_FLASHES = [  'PNG/Puff/WhitePuff00.png',
                    'PNG/Puff/WhitePuff01.png',
                    'PNG/Puff/WhitePuff02.png',
                    'PNG/Puff/WhitePuff03.png',
                    'PNG/Puff/WhitePuff04.png',
                    'PNG/Puff/WhitePuff05.png',
                    'PNG/Puff/WhitePuff06.png',
                    'PNG/Puff/WhitePuff07.png',
                    'PNG/Puff/WhitePuff08.png']
FLASH_DURATION = 40

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
ITEM_LAYER = 1
EFFECTS_LAYER = 4

# Items
ITEM_IMAGES = {'health_pack' : 'PNG/Item/health_pack.png'}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 20
BOB_SPEED = 0.6

# Sounds
BG_MUSIC = 'espionage.ogg'
PLAYER_HIT_SOUNDS = ['player/pain1.wav', 'player/pain2.wav' ,'player/pain3.wav', 'player/pain4.wav']
ZOMBIE_MOAN_SOUNDS = ['zombie/moan1.wav', 'zombie/moan2.wav' ,'zombie/moan3.wav']
EFFECT_SOUNDS = {   'level_start' : 'level_start.wav',
                    'health_pack': 'health_pack.wav'}
GUN_SOUNDS = {  'cg1' : 'gun/cg1.wav',
                'shotgun': 'gun/shotgun.wav'}