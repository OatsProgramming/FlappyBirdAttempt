import time
import pygame, os
from sys import exit
from random import randint

os.system('clear')
os.chdir('/Users/OatsProgramming/Documents/Python_Files/Python Lessons and notes/Pygame Tutorial/Flappy Bird')


class Bird(pygame.sprite.Sprite):
    score = 0
    def __init__(self):
        super().__init__()

        self.frames = [bird1, bird2, bird3]
        self.frames_index = 0
        self.image = self.frames[self.frames_index]
        # self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(center = (100, 400))

        self.rot_vel = 0
        self.gravity = 0
    
    def player_input(self):
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_SPACE] and self.rect.bottom <= 800 and self.gravity > 0:
            rotation = 0
            rotation += 25
            if rotation == 85:
                rotation = 85
            self.gravity -= 8 
            
    def animation(self):
        if self.gravity != 0:
            self.image = self.rotation()
        else:
            self.frames_index += 0.1
            if self.frames_index > len(self.frames):
                self.frames_index = 0
            self.image = self.frames[int(self.frames_index)]
        
    
    def rotation(self):
        if self.gravity < 0:
            self.rot_vel += 10.5
            if self.rot_vel >= 25:
                self.rot_vel = 25
            surface = bird3
        else:
            surface = bird1
            self.rot_vel -= 2.5
            if self.rot_vel >= -90 and self.rot_vel <= -35:
                surface = bird2
            if self.rot_vel <= -90:
                self.rot_vel = -90
                surface = bird1
            if self.rect.bottom == 700:
                self.rot_vel = 0
                surface = bird2
        return pygame.transform.rotate(surface, self.rot_vel)
         
        

    def apply_gravity(self):
        if game_active:
            self.gravity += 0.4
            self.rect.y += self.gravity
            self.image = bird1
            if self.gravity >= 20:
                self.gravity = 20
            if self.rect.bottom >= 700:
                #self.gravity = 0
                self.rect.bottom = 700
                

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()

class Obstacles(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pipe
        self.rect = self.image.get_rect(midtop = (700, randint(200, 600)))
        

    def destroy(self):
        if self.rect.right < 0:
            self.kill()
            
    
    def update(self):
        global game_active, actual_score
        duplicate = pygame.transform.rotate(pipe, 180)
        self.duplicate_rect = duplicate.get_rect(midbottom = (52 + self.rect.x, (-200) + self.rect.y))
        screen.blit(duplicate, self.duplicate_rect)
        new_score = self.get_score() 
        Bird.score += new_score # For some reason its giving me the number 25
        actual_score = Bird.score // 25 # I will divide it by 25 to get the actual score
        Obstacles.display_score()
        self.destroy()
        game_active = active(self.duplicate_rect)
        if game_active:
            self.rect.x -= 2
        else:
            game_active = False
            return game_active

    def display_score():
        text_font = pygame.font.Font('Pixeltype copy.ttf', 50)
        score_surf = text_font.render(f'Score: {actual_score}', False, 'DarkGrey')
        score_rect = score_surf.get_rect(center = (300, 200))
        screen.blit(score_surf, score_rect)

    def get_score(self):
        line = pygame.draw.line(screen, 'gold', self.rect.midtop, self.duplicate_rect.midbottom)
        if bird.sprite.rect.colliderect(line):
            return 1
        else:
            return 0
        
        
        

def active(duplicate_rect):
    if pygame.sprite.spritecollide(bird.sprite, obstacle, False) or duplicate_rect.colliderect(bird.sprite.rect):
        return False
    return True

# class Ground(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = ground_surf
#         self.rect = self.image.get_rect(topleft = (0, 700))
#     
#     def animation(self):
#         jh = 
    
pygame.init()

screen = pygame.display.set_mode((600, 800))
game_active = False
clock = pygame.time.Clock()

bird1 = pygame.image.load('flappy bird imgs/bird1.png').convert_alpha()
bird1 = pygame.transform.scale(bird1, (51, 36))
bird2 = pygame.image.load('flappy bird imgs/bird2.png').convert_alpha()
bird2 = pygame.transform.scale(bird2, (51, 36))
bird3 = pygame.image.load('flappy bird imgs/bird3.png').convert_alpha()
bird3 = pygame.transform.scale(bird3, (51, 36))

bird = pygame.sprite.GroupSingle()
bird.add(Bird())

pipe = pygame.image.load('flappy bird imgs/pipe.png').convert_alpha()
pipe = pygame.transform.scale2x(pipe)

sky_surf = pygame.image.load('flappy bird imgs/bg.png').convert()
sky_surf = pygame.transform.scale(sky_surf, (600,800))
ground_surf = pygame.image.load('flappy bird imgs/base.png').convert()
ground_surf = pygame.transform.scale2x(ground_surf)
ground_rect = ground_surf.get_rect(topleft = (0, 700))

obstacle = pygame.sprite.Group()

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 5000)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
        if game_active:
            if event.type == obstacle_timer:
                obstacle.add(Obstacles())
                

            #if event.type == pygame.MOUSEMOTION:
             #   print(event.pos)
        
        elif not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.sprite.rect.center = (100, 400)
                bird.sprite.rot_vel = 0
                obstacle.empty()
                game_active = True
    
    if game_active:

        screen.blit(sky_surf, (0,0))
        

        bird.draw(screen)
        bird.update()

        obstacle.draw(screen)
        obstacle.update()
        
        screen.blit(ground_surf, ground_rect)
    
    else:
        screen.blit(sky_surf, (0,0))
        bird.draw(screen)
        bird.update()
        obstacle.draw(screen)
        obstacle.update()
        screen.blit(ground_surf, (0, 700))
    pygame.display.update()
    clock.tick(60)
