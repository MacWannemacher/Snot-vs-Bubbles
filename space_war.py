# Imports
import pygame
import random

# Initialize game engine
pygame.init()

# Window
WIDTH = 1500
HEIGHT = 900
SIZE = (WIDTH, HEIGHT)
TITLE = "Space War"

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)

# Fonts
FONT_XS = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 25)
FONT_SM = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 50)
FONT_MD = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 75)
FONT_LG = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 100)
FONT_XL = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 125)

# Images
ship_img = pygame.image.load('assets/images/shipPink_manned.png').convert_alpha()
enemyG_img = pygame.image.load('assets/images/shipGreen_manned.png').convert_alpha()
enemyY_img = pygame.image.load('assets/images/shipYellow_manned.png').convert_alpha()
ufo_img = pygame.image.load('assets/images/shipBlue.png').convert_alpha()
shipPink_img = pygame.image.load('assets/images/small_shipPink.png').convert_alpha()
shipGreen_img = pygame.image.load('assets/images/small_shipGreen.png').convert_alpha()

laser_img = pygame.image.load('assets/images/laserPink1.png').convert_alpha()
bomb_img = pygame.image.load('assets/images/laserGreen1.png').convert_alpha()
powerup_img = pygame.image.load('assets/images/powerup.png').convert_alpha()

explosionG_img = pygame.image.load('assets/images/laserGreen_burst.png').convert_alpha()
explosionY_img = pygame.image.load('assets/images/laserYellow_burst.png').convert_alpha()
explosionP_img = pygame.image.load('assets/images/laserPink_burst.png').convert_alpha()

planet_img = pygame.image.load('assets/images/background/planet_background.png').convert_alpha()

# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')
SHOOT = pygame.mixer.Sound('assets/sounds/shoot.wav')

PLAYING_MUSIC = "assets/sounds/playing_music.wav"
SETUP_MUSIC = "assets/sounds/setup_music.wav"

# Stages
START = 0
PLAYING = 1
WIN = 2
LOSE = 3

# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 4
        self.shield = 3
        self.shots = 0
        ''' self.shoots double = False '''

    def move_left(self):
        self.rect.x -= self.speed
    
    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):

        SHOOT.play()
        self.shots += 1
        
        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx  
        laser.rect.centery = self.rect.top
        lasers.add(laser)
        
        
    def update(self):
        ''' check screen edges '''
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        ''' check powerups '''
        hit_list = pygame.sprite.spritecollide(self, powerups, True, pygame.sprite.collide_mask)

        for hit in hit_list:
            hit.apply(self)
        
        ''' check bombs '''
        hit_list = pygame.sprite.spritecollide(self, bombs, True, pygame.sprite.collide_mask)
 
        for hit in hit_list:
            self.shield -= 1
            EXPLOSION.play()

        if self.shield == 0:
            self.kill()

            explosion = Explosion(explosionP_img)
            explosion.rect.centerx = self.rect.centerx
            explosion.rect.centery = self.rect.centery
            explosions.add(explosion)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, image):
        self.ticks = 5
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()

    def update(self):
        self.ticks -=1

        if self.ticks == 0:
            self.kill()

            EXPLOSION.play()

class Laser(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 4

        SHOOT.play()
        player.shots += 1

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0 :
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)

    def update(self):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            SHOOT.play()
            self.kill()
            player.score += 1
                
            explosion = Explosion(explosionG_img)
            explosion.rect.centerx = self.rect.centerx
            explosion.rect.centery = self.rect.centery
            explosions.add(explosion)
            
class Bomb(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 5

        SHOOT.play()

    def update(self):
        self.rect.y += self.speed

        if self.rect.bottom > HEIGHT:
            self.kill()

class ShieldPowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 4

    def apply(self, ship):
        print("zoom")
        ship.shield = 3
        self.kill()
        
    def update(self):
        self.rect.y += self.speed


        if self.rect.bottom > HEIGHT:
            self.kill()
        
class Fleet():
    def __init__(self, mobs):
        self.mobs = mobs
        self.speed = 5
        
        self.moving_right = True
        self.drop_speed = 20
        self.bomb_rate = 20
    
    def move(self):
        hits_edge = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right >= WIDTH:
                    hits_edge = True

            else:
                m.rect.x -= self.speed

                if m.rect.left <= 0:
                    hits_edge = True

        if hits_edge:
            self.reverse()
            self.move_down()
            
    def reverse(self):
        self.moving_right = not self.moving_right
    
    def move_down(self):
        for m in mobs:
            m.rect.y += self.drop_speed
            
    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        
        mob_list = mobs.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice (mob_list)
            bomber.drop_bomb()
    
    def update(self):
        self.move()
        self.choose_bomber()


class Ufo(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 6

    def update(self):
        self.rect.x += self.speed

        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
                SHOOT.play()
                self.kill()
                player.score += 10

                EXPLOSION.play()

                explosion = Explosion(explosionG_img)
                explosion.rect.centerx = self.rect.centerx
                explosion.rect.centery = self.rect.centery
                explosions.add(explosion)
        

# Game helper functions
def draw_background():
    screen.fill(BLACK)
    
def show_start_screen():
    screen.blit(planet_img, [0, 0])
    screen.blit(shipPink_img, [350, 175])
    screen.blit(shipPink_img, [415, 175])
    screen.blit(shipPink_img, [390, 200])
    screen.blit(shipGreen_img, [1200, 500])
    screen.blit(shipGreen_img, [1100, 550])
    screen.blit(shipGreen_img, [1185, 575])
    
    
    title_text = FONT_XL.render("Space War!", 1, WHITE)
    w = title_text.get_width()
    screen.blit(title_text, [WIDTH/2 - w/2, 300])
    
    start_text = FONT_SM.render("Press 'Space' to start", 1, WHITE)
    w1 = start_text.get_width()
    screen.blit(start_text, [WIDTH/2 - w1/2, 400])


def show_win_screen():
    screen.fill(BLACK)
    
    win_text = FONT_XL.render("YOU WON", 1, WHITE)
    w = win_text.get_width()
    screen.blit(win_text, [WIDTH/2 - w/2, 300])
    
    stats_text = FONT_SM.render("You scored " + str(player.score) + "  points using " + str(player.shots) + " lasers!!", 1, WHITE)
    w1 = stats_text.get_width()
    screen.blit(stats_text, [WIDTH/2 - w1/2, 400])

def show_lose_screen():
    screen.fill(BLACK)
    
    lose_text = FONT_XL.render("You lost!", 1, WHITE)
    w = lose_text.get_width()
    screen.blit(lose_text, [WIDTH/2 - w/2, 300])    
                                                                  
def show_stats():
    score1 = FONT_XS.render("Score: " + str(player.score), 1, WHITE)
    screen.blit(score1, [10, 10])
    
    shield1 = FONT_XS.render("Shield: " + str(ship.shield), 1, WHITE)
    shield_rect = shield1.get_rect()
    shield_rect.right = WIDTH -10
    shield_rect.top = 10
    screen.blit(shield1, shield_rect)

def check_end():
    global stage

    if len(mobs) == 0:
        stage = WIN
        set_music(SETUP_MUSIC)
    elif len(player) == 0:
        stage = LOSE
        set_music(SETUP_MUSIC)

def set_music(track):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(2500)

    if track != None:
        pygame.mixer.music.load(track)
        pygame.mixer.music.play(-1)
    
def setup():
    global stage, done, ticks
    global player, ship, lasers, mobs, fleet, bombs, explosions, ufo, powerups

    ''' Make game objects '''
    ship = Ship(ship_img)
    ship.rect.centerx = WIDTH / 2
    ship.rect.bottom = HEIGHT - 30
    
    ''' Make sprite groups '''
    
    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0
    player.shots = 0

    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    
    mob1 = Mob(300, 50, enemyG_img)
    mob2 = Mob(700, 50, enemyG_img)
    mob3 = Mob(1100, 50, enemyG_img)
    mob4 = Mob(500, 150, enemyY_img)
    mob5 = Mob(900, 150, enemyY_img)
    
    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3, mob4, mob5)

    ufo1 = Ufo(-2800, 500, ufo_img)
    ufo = pygame.sprite.Group()
    ufo.add(ufo1)
    
    
    fleet = Fleet(mobs)

    powerup1 = ShieldPowerUp(800, -2000, powerup_img)
    powerups = pygame.sprite.Group()
    powerups.add(powerup1)
    
    ''' set stage '''
    stage = START
    done = False

    ''' set timer '''
    ticks = 0

    ''' set music '''
    set_music(SETUP_MUSIC)
    
# Game loop
setup()
while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
                    set_music(PLAYING_MUSIC)
                    
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()

            elif stage == WIN:
                    stage = START
                    setup()

            elif stage == LOSE:
                    stage = START
                    setup()
                    

    pressed = pygame.key.get_pressed()

    if stage == PLAYING:
        if pressed [pygame.K_LEFT]:
            ship.move_left()
        elif pressed [pygame.K_RIGHT]:
            ship.move_right()
        
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        player.update()
        lasers.update()
        bombs.update()
        fleet.update()
        mobs.update()
        explosions.update()
        ufo.update()
        powerups.update()
        ticks += 1

        check_end()

    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    if stage == START:
        show_start_screen()
        
    if stage == PLAYING:
        draw_background()
        show_stats()
        lasers.draw(screen)
        bombs.draw(screen)
        player.draw(screen)
        mobs.draw(screen)
        explosions.draw(screen)
        ufo.draw(screen)
        powerups.draw(screen)
        
    if stage == WIN:
        show_win_screen()
        
    if stage == LOSE:
        show_lose_screen()

    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()

    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)

# Close window and quit
pygame.quit()
