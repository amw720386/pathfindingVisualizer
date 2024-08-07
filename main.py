import pygame
from pygame.locals import *
import time
import screeninfo
import sys

pygame.init()
clock = pygame.time.Clock()
screen_width = screeninfo.get_monitors()[0].width
screen_height = screeninfo.get_monitors()[0].height
if not screen_width/screen_height == 16/9:
    screen_width = 1920
    screen_height = 1080
    if screen_width > screeninfo.get_monitors()[0].width:
        screen_width = 1280
        screen_height = 768
        if screen_width > screeninfo.get_monitors()[0].width:
            print('res unsupported')
            sys.exit()

screen = pygame.display.set_mode((screen_width,screen_height))

WHITE = (255,255,255)
BLACK = (0,0,0)

class Avatar:
    def __init__(self, start_x, start_y, size):
        self.x = start_x
        self.y = start_y
        self.renderx = self.x*scaled_block_width
        self.rendery = self.y*scaled_block_width
        self.size = size
        self.rect = pygame.Rect(self.renderx,self.rendery,self.size,self.size)
        self.color = WHITE
    
    def update(self):
        self.renderx = self.x*scaled_block_width
        self.rendery = self.y*scaled_block_width
        self.rect = pygame.Rect(self.renderx,self.rendery,self.size,self.size)

    def draw(self, screen):
        pygame.draw.rect(screen,self.color,self.rect)

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        defineRatios(width,height)
        self.render = [['' for _ in range(width)] for _ in range(height)]
        for row_index, row in enumerate(self.render):
            for column_index, column in enumerate(row):
                self.render[row_index][column_index] = Block(column_index,row_index)

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.renderx = x*scaled_block_width
        self.rendery = y*scaled_block_height
        self.border_width = int(scaled_block_height/40)
        self.border_rect = pygame.Rect(self.renderx,self.rendery,scaled_block_width,scaled_block_height)
        self.inner_rect = pygame.Rect(self.renderx + self.border_width, self.rendery + self.border_width, scaled_block_width - self.border_width*2, scaled_block_height - self.border_width*2)

    def draw(self, screen):
        pygame.draw.rect(screen,WHITE,self.border_rect)
        pygame.draw.rect(screen,BLACK,self.inner_rect)

def defineRatios(x,y):   
    global scaled_block_height 
    scaled_block_height = int(screen_height/y)
    global scaled_block_width 
    scaled_block_width = int(screen_width/x)

map = Map(16,9)

print(scaled_block_height)
print(scaled_block_width)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()

    for row in map.render:
        for column in row:
            column.draw(screen)

    pygame.display.flip()
    clock.tick(60)