from glob import glob
import pygame, os
from sys import exit
from random import randint

os.system('clear')
os.chdir('/Users/OatsProgramming/Documents/Python_Files/Python Lessons and notes/Pygame Tutorial/Flappy Bird')


class Bird(pygame.sprite.Sprite):
    score = 0 # Added this here for convenience
    def __init__(self):
        super().__init__()

        self.frames = [bird1, bird2, bird3]
        self.frames_index = 0
        self.image = self.frames[self.frames_index]
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
        self.rect = self.image.get_rect(midtop = (700, randint(300, 600)))
        
        self.actual_score = 0

    def destroy(self):
        if self.rect.right < 0:
            self.kill()
            
    
    def update(self):
        global game_active
        duplicate = pygame.transform.rotate(pipe, 180)
        self.duplicate_rect = duplicate.get_rect(midbottom = (52 + self.rect.x, (-200) + self.rect.y))
        screen.blit(duplicate, self.duplicate_rect)
        self.destroy()
        game_active = active(self.duplicate_rect)
        if game_active:
            self.rect.x -= 2
 
            new_score = self.get_score() 
            Bird.score += new_score # For some reason its giving me the number 25
            self.actual_score = Bird.score // 25 # I will divide it by 25 to get the actual score
            display_score(self.actual_score)
        else:
            game_active = False
    
        

    def get_score(self):
        # The next four lines are to create a transparent dummy surface for the line
        dummy_surface = pygame.Surface((600,800))  # the size of your rect
        dummy_surface.set_alpha(0)                  # alpha level (Set to 0 for clear; set anything > 0 for increasing translucence)
        dummy_surface.fill((255,255,255))           # this fills the entire surface
        screen.blit(dummy_surface, (0,0))
        line = pygame.draw.line(dummy_surface, 'black', self.rect.midtop, self.duplicate_rect.midbottom) # Left the line colored to see if itll appear on screen
        if bird.sprite.rect.colliderect(line):
            return 1
        else:
            return 0
        
def active(duplicate_rect):
    if pygame.sprite.spritecollide(bird.sprite, obstacle, False) or duplicate_rect.colliderect(bird.sprite.rect):
        return False
    return True
    

# Initiation
pygame.init()

# The fundamentals
screen = pygame.display.set_mode((600, 800))
game_active = False
clock = pygame.time.Clock()

# Bird stuff
bird1 = pygame.image.load('flappy bird imgs/bird1.png').convert_alpha()
bird1 = pygame.transform.scale(bird1, (51, 36))
bird2 = pygame.image.load('flappy bird imgs/bird2.png').convert_alpha()
bird2 = pygame.transform.scale(bird2, (51, 36))
bird3 = pygame.image.load('flappy bird imgs/bird3.png').convert_alpha()
bird3 = pygame.transform.scale(bird3, (51, 36))
bird = pygame.sprite.GroupSingle()
bird.add(Bird())

# Obstacle stuff
pipe = pygame.image.load('flappy bird imgs/pipe.png').convert_alpha()
pipe = pygame.transform.scale2x(pipe)
obstacle = pygame.sprite.Group() # DO NOT CHANGE THIS TO GROUPSINGLE. IT WILL CAUSE BUGS EVERYTIME IT LOOPS
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 5000) # This is changeable. controls the spawn rate of the obstacles

# Background (Maybe incorporate parrallax feature?)
sky_surf = pygame.image.load('flappy bird imgs/bg.png').convert()
sky_surf = pygame.transform.scale(sky_surf, (600,800))

# Ground stuff
ground_surf = pygame.image.load('flappy bird imgs/base.png').convert()
ground_surf = pygame.transform.scale2x(ground_surf)
ground_rect = ground_surf.get_rect(topleft = (0, 700))
duplicate_ground = ground_surf
duplicate_groundrect = duplicate_ground.get_rect(topleft = (625,700)) # I found that x_pos = 625 pixels is the best position to avoid the "stitches" look for the ground animation

# Intro stuff
text_font = pygame.font.Font('flappy-font.ttf', 50)
title_surf = text_font.render('Flappy Bird', False, 'white')
title_rect = title_surf.get_rect(topleft = (250, 100))
attempt_surf = text_font.render('Attempted by Jay', False, '#C79626')
attempt_surf = pygame.transform.scale(attempt_surf, (150, 25))
attempt_rect = attempt_surf.get_rect(topleft = (375, 175))

def display_score(actual_score):
    score_surf = text_font.render(f'Score: {actual_score}', False, 'Black')
    score_rect = score_surf.get_rect(center = (300, 100))
    screen.blit(score_surf, score_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # To close the game and program
            pygame.quit()
            exit()
    
        if game_active:
            if event.type == obstacle_timer:
                obstacle.add(Obstacles())
                
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Reset everything. Trying to figure out to reset score 
                bird.sprite.rect.center = (100, 400)
                bird.sprite.rot_vel = 0
                obstacle.empty()
                game_active = True
    
    if game_active:

        screen.blit(sky_surf, (0,0))
        # Bird 
        bird.draw(screen)
        bird.update()
        # Pipes
        obstacle.draw(screen)
        obstacle.update()
        # Ground animation
        screen.blit(ground_surf, ground_rect)
        ground_rect.x -= 2
        screen.blit(duplicate_ground, duplicate_groundrect)
        duplicate_groundrect.x -= 2
        # Objective: Pretty much make a treadmill of animation for the ground
        if ground_rect.right < 0:
            ground_rect.left = duplicate_groundrect.right
        if duplicate_groundrect.right < 0:
            duplicate_groundrect.left = ground_rect.right
    
    else:
        screen.blit(sky_surf, (0,0))
        screen.blit(title_surf, title_rect)
        screen.blit(attempt_surf, attempt_rect)
        bird.draw(screen)
        bird.update()
        obstacle.draw(screen)
        obstacle.update()
        screen.blit(ground_surf, (0, 700))
    pygame.display.update()
    clock.tick(60)
