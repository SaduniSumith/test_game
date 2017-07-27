
import pygame
import random

WIDTH = 480 # WIDTH OF GAME WINDOW 
HEIGHT = 600 #HEIGHT OF GAME WINDOW
FPS = 60

#Colors
Black = (0, 0, 0,)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,40))  
        self.image.fill(Green)
        self.rect = self.image.get_rect()
        self.rect.centerx = (WIDTH/2)
        self.rect.bottom = (HEIGHT-10)
        self.speedx = 0
    def update(self):
        self.speedx = 0 #speed in x direction
        keystate = pygame.key.get_pressed() # checks if key is being pressed
        if keystate[pygame.K_LEFT]: # if left key is being pressed 
            self.speedx = -8   
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH: # bounderies so sprite doesnt go off screen 
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet) 

class Mob(pygame.sprite.Sprite): #enemy sprites
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,40))
        self.image.fill((Red))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width) 
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(4,10)
        self.speedx = random.randrange(-3,3) 
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.right < 0 or self.rect.left > WIDTH: 
            self.rect.x = random.randrange(WIDTH - self.rect.width) 
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(4,10)
            self.speedx = random.randrange(-3,3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface((10,10))
        self.image.fill((White))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -20
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill() 
            
    
#initialize and create game window

pygame.init()
pygame.mixer.init() # initialize sound
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # create screen 
pygame.display.set_caption("Game") # give game a name 
clock = pygame.time.Clock() # keep track of speed and time


bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player) 

mobs = pygame.sprite.Group()
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

#Game Loop

running = True
while running:
    clock.tick(FPS) # keep the loop running at the right speed 
    #1.Processes Inputs (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot() 
    #2.Updates
    all_sprites.update()
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m) 
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False
 
    #3.Renders (draws)
        
    screen.fill(Black)
    all_sprites.draw(screen) 
    #after drawing everything, flip display
    pygame.display.flip() 
pygame.quit() 
    
    
