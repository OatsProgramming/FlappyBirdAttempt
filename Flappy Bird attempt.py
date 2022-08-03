import pygame, os
from sys import exit
from random import randint

os.system('clear')
os.chdir('/Users/username/Documents/Python_Files/Python Lessons and notes/Pygame Tutorial/Flappy Bird')


'''
Changed the selves in the Bird Class; 
that was the reason why it was using too much memory.
Too many selves
Aug 2
'''

class Bird(pygame.sprite.Sprite):
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
            print('pressed')
            rotation = 0
            rotation += 25
            if rotation == 85:
                rotation = 85
            self.gravity -= 10
            
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
        self.destroy()
        if game_active:
            self.rect.x -= 2
        

def collision():
    if pygame.sprite.spritecollide(bird.sprite, obstacle, False):
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
bird2 = pygame.image.load('flappy bird imgs/bird2.png').convert_alpha()
bird3 = pygame.image.load('flappy bird imgs/bird3.png').convert_alpha()

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
        
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                obstacle.empty()
                game_active = True

    if game_active:

        screen.blit(sky_surf, (0,0))
        

        bird.draw(screen)
        bird.update()
    
        obstacle.draw(screen)
        obstacle.update()
        
        
        screen.blit(ground_surf, ground_rect)
        
        game_active = collision()
    
    else:
        screen.blit(sky_surf, (0,0))
        bird.draw(screen)
        bird.update()
        obstacle.draw(screen)
        obstacle.update()
        screen.blit(ground_surf, (0, 700))
    pygame.display.update()
    clock.tick(60)
