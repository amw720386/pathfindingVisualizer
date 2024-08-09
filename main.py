import pygame
from pygame.locals import *
import time
import screeninfo
import sys
import heapq
import threading

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
RED = (255,0,0)
GREY = (128,128,128)
GREEN = (0,255,0)
BLUE = (0,0,255)

class Avatar:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.renderx = self.x*scaled_block_width
        self.rendery = self.y*scaled_block_width
        self.size = scaled_block_width - border_width*2
        self.rect = pygame.Rect(self.renderx + border_width,self.rendery + border_width,self.size,self.size)
        self.color = WHITE
    
    def update(self, x, y):
        self.renderx = x*scaled_block_width
        self.rendery = y*scaled_block_width
        self.rect = pygame.Rect(self.renderx,self.rendery,self.size,self.size)

    def draw(self, screen):
        pygame.draw.rect(screen,self.color,self.rect)

class Goal:
    def __init__(self, x, y):
        self.x = x 
        self.y = y
        self.size = scaled_block_width - border_width*2
        self.color = RED
        self.rect = pygame.Rect(self.x*scaled_block_width + border_width,self.y*scaled_block_height + border_width,self.size,self.size)

    def draw(self,screen):
        pygame.draw.rect(screen,self.color,self.rect)

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        defineRatios(width,height)
        self.render = [['' for _ in range(width)] for _ in range(height)]
        for row_index, row in enumerate(self.render):
            for column_index, column in enumerate(row):
                if column_index == 0 or row_index == 0 or row_index == height-1 or column_index == width-1:
                    self.render[row_index][column_index] = Block(column_index,row_index, 2)
                else:
                    self.render[row_index][column_index] = Block(column_index,row_index, 1)

class Block:
    def __init__(self, x, y, type):
        self.types = {1: '',2:'WALL',3:'WEIGHTED'}
        self.type = type
        self.x = x
        self.y = y
        self.renderx = x*scaled_block_width
        self.rendery = y*scaled_block_height
        self.border_width = border_width
        self.hover = False
        self.path = False
        self.border_rect = pygame.Rect(self.renderx,self.rendery,scaled_block_width,scaled_block_height)
        self.inner_rect = pygame.Rect(self.renderx + self.border_width, self.rendery + self.border_width, scaled_block_width - self.border_width*2, scaled_block_height - self.border_width*2)
        self.hover_rect = pygame.Surface((scaled_block_width, scaled_block_height))
        self.hover_rect.set_alpha(128)
        self.hover_rect.fill((255,255,255))
        self.path_rect = pygame.Surface((scaled_block_width, scaled_block_height))
        self.path_rect.set_alpha(100)
        self.path_rect.fill((0,0,255))
        self.pathUse = False

    def draw(self, screen):
        pygame.draw.rect(screen,WHITE,self.border_rect)
        if self.type == 1: #walkable
            pygame.draw.rect(screen,BLACK,self.inner_rect)
        if self.type == 2: #wall
            pygame.draw.rect(screen,GREEN,self.inner_rect)
        if self.path: #considered in path
            screen.blit(self.path_rect,(self.renderx, self.rendery))
        if self.pathUse: #used in path
            pygame.draw.rect(screen,BLUE,self.inner_rect)
        if self.type == 3: #weighted
            pygame.draw.rect(screen,GREY,self.inner_rect)
        if self.hover: #hovered over
            screen.blit(self.hover_rect,(self.renderx, self.rendery))

def defineRatios(x,y):   
    global scaled_block_height 
    scaled_block_height = round(screen_height/y)
    global scaled_block_width 
    scaled_block_width = round(screen_width/x)
    global border_width
    border_width = round(scaled_block_height/40) + 0.01

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0 
        self.h = 0  
        self.f = 0  

    def __lt__(self, other):
        return self.f < other.f

def astar(grid, start, goal):
    start_node = Node(start)
    goal_node = Node(goal)

    open_list = []
    closed_list = set()

    heapq.heappush(open_list, start_node)
    
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node.position == goal_node.position:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent

            for position in path:
                map.render[position[1]][position[0]].pathUse = True 
                time.sleep(0.2)

            return path[::-1]  

        closed_list.add(current_node.position)

        for direction in directions:
            new_position = (current_node.position[0] + direction[0], current_node.position[1] + direction[1])

            if (0 <= new_position[0] < len(grid[0]) and 0 <= new_position[1] < len(grid)):
                if grid[new_position[1]][new_position[0]].type == 1:  
                    if new_position in closed_list:
                        continue
                    grid[new_position[1]][new_position[0]].path = True
                    time.sleep(0.05)
                    neighbor_node = Node(new_position, current_node)

                    neighbor_node.g = current_node.g + 1
                    neighbor_node.h = abs(neighbor_node.position[1] - goal_node.position[1]) + abs(neighbor_node.position[0] - goal_node.position[0])
                    neighbor_node.f = neighbor_node.g + neighbor_node.h

                    if all(neighbor_node.f < node.f for node in open_list if node.position == neighbor_node.position):
                        heapq.heappush(open_list, neighbor_node)
    return []  

map = Map(256,144) #OUTER IS NON EXLCUSIVE I.E 512 and 288 or 256 and 144 < SET DIMENSIONS
player = Avatar(15,2) # < SET PLAYER STARTING POSITION
goal = Goal(134,112) # < SET GOAL POSITION

if not (0 < goal.x < map.width) or not (0 < goal.y < map.height):
    sys.exit('goal not in range')
if not (0 < player.x < map.width) or not (0 < player.y < map.height):
    sys.exit('player not in range')

pathfinding_thread = threading.Thread(target=astar,args=(map.render, (player.x,player.y), (goal.x,goal.y)), daemon=True)

while True:
    keys = pygame.key.get_pressed()
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYUP:   
            if event.key == pygame.K_z:     
                for row in map.render:
                    for column in row:
                        column.path = False
                        column.pathUse = False
                pathfinding_thread.start()

    if pygame.mouse.get_pos()[0] > 0 and pygame.mouse.get_pos()[0] < screen_width:
        if pygame.mouse.get_pos()[1] > 0 and pygame.mouse.get_pos()[1] < screen_height:
            mouse_pos_x = int(pygame.mouse.get_pos()[0]/scaled_block_width)
            mouse_pos_y = int(pygame.mouse.get_pos()[1]/scaled_block_height)
            map.render[mouse_pos_y][mouse_pos_x].hover = True
            if pygame.mouse.get_pressed()[0]:
                map.render[mouse_pos_y][mouse_pos_x].type = 2
            if pygame.mouse.get_pressed()[2]:
                map.render[mouse_pos_y][mouse_pos_x].type = 1

    for row in map.render:
        for column in row:
            column.draw(screen)
            column.hover = False

    player.draw(screen)
    goal.draw(screen)

    pygame.display.flip()
    screen.fill(WHITE)
    clock.tick(60)