

from pygame import *
from time import sleep
import pygame
import random
from os import path
from random import randint
import pygame_menu
img_dir = path.join(path.dirname(__file__), 'img')


pygame.init()

win_width = 800
win_height = 500
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
pygame.font.init()
font = pygame.font.Font(None, 70)
font1= pygame.font.Font(None, 36)



pygame.mixer.init()
pygame.mixer.music.load('space.ogg')
pygame.mixer.music.play()
fire = pygame.mixer.Sound('fire.ogg')
screen = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Игра")
clock = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 20)
game_over_font = pygame.font.Font('freesansbold.ttf', 64)       
alion = False
score_val = 0
lost = 0


win = font.render('U WIN', True, (255,215,0))
lose = font.render('U LOSE', True, (180, 0 , 0))
def start_the_game():
        
        
        
        
        
       
        class GameSprite(pygame.sprite.Sprite):
            def __init__(self, player_Image, player_x, player_y, player_speed):
                super().__init__()
                self.image = pygame.transform.scale(pygame.image.load(player_Image), (50, 50))
                self.speed = player_speed


                self.rect = self.image.get_rect()
                self.rect.x = player_x
                self.rect.y = player_y

            def reset(self):
                screen.blit(self.image, (self.rect.x, self.rect.y))
        
        class Player(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.transform.scale(player_img, (100, 70))
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.centerx = win_width / 2
                self.rect.bottom = win_height - 10
                self.speedx = 0

            def update(self):
                self.speedx = 0
                keystate = pygame.key.get_pressed()
                if keystate[K_LEFT]:
                    self.speedx = -8
                if keystate[K_RIGHT]:
                    self.speedx = 8
                self.rect.x += self.speedx
                if self.rect.right > win_width:
                    self.rect.right = win_width
                if self.rect.left < 0:
                    self.rect.left = 0

            def shoot(self):
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                fire.play()
        class Mob(GameSprite):
            
            def update(self):
                
                global lost
                
                self.rect.y += self.speed
                if self.rect.y >= win_height:
                    self.rect.x = randint(80, win_width - 80)
                    self.rect.y = 0
                    lost += 1
                    
                if self.rect.right > win_width:
                    self.rect.right = win_width
                if self.rect.left < 0:
                    self.rect.left = 0

        class Bullet(pygame.sprite.Sprite):
            def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = bullet_img
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.bottom = y
                self.rect.centerx = x
                self.speedy = -10

            def update(self):
                self.rect.y += self.speedy
                if self.rect.bottom < 0:
                    self.kill()

        img_back = "galaxy.jpg"
        background = pygame.transform.scale(pygame.image.load(img_back), (800,500))
        background_rect = background.get_rect()
        player_img = pygame.transform.scale(pygame.image.load('rocket.png'),(100,50))
       
        
        bullet_img = pygame.transform.scale(pygame.image.load('bullet.png'),(20,30))

        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(1,6):
            m = Mob('ufo.png',randint(80, win_width - 80),1, randint(1,4))
            all_sprites.add(m)
            mobs.add(m)
            

        running = True
        while running:
            
            clock.tick(FPS)
            
            for event in pygame.event.get():
            
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.shoot()

                
            hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
            for hit in hits:
                
                global score_val
                score_val += 1
             
                
            hit = pygame.sprite.spritecollide(player, mobs, False)
            if hit:
                running = False

            all_sprites.update()
            
                
            
                

            screen.fill(BLACK)
            screen.blit(background, background_rect)
            all_sprites.draw(screen)
            text = font.render('Cчет:'+ str(score_val),1,(255,255,255))
            screen.blit(text,(10,20))
            text2 = font.render('Пропущено:'+ str(lost),1,(255,255,255))
            screen.blit(text2,(10,50))
            win = font1.render('U WIN', True, (255,215,0))
            lose = font1.render('U LOSE', True, (255,255,255))
            
            pygame.display.update()
            
            if lost == 5 or lost >=5:
                
                screen.blit(lose,(10,100))
                sleep(5)
                quit()
                
            if score_val == 5:
                
                screen.blit(win,(400,250))
                display.update()
                time.delay(3000)
                quit()
menu = pygame_menu.Menu('Солдат vs Чужих', 800, 500,
                       theme=pygame_menu.themes.THEME_GREEN)

menu.add.text_input('Имя солдата :', default='Гоуст')

menu.add.button('Играть', start_the_game)
menu.add.button('Выход', pygame_menu.events.EXIT)

menu.mainloop(screen)