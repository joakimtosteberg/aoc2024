import re
import sys

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x},{self.y})"

class Robot:
    def __init__(self, pos, speed):
        self.pos = pos
        self.speed = speed

    def __repr__(self):
        return f"{self.pos}:{self.speed}"

r = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")
robots = []
with open(sys.argv[1]) as f:
    for line in f:
        m = r.match(line)
        robot = Robot(Vec2(int(m.group(1)), int(m.group(2))),
                      Vec2(int(m.group(3)), int(m.group(4))))
        robots.append(robot)

seconds = 100
width = 101
height = 103

def move_robots(robots, seconds):
    new_robots = []
    for robot in robots:
        new_robots.append(Robot(Vec2((robot.pos.x + robot.speed.x*seconds) %  width,
                                     (robot.pos.y + robot.speed.y*seconds) % height),
                                robot.speed))
    return new_robots


def calculate_safety(robots, width, height):
    x_middle = int(width/2)
    y_middle = int(height/2)
    quadrants = {(0,0): 0, (0,1): 0, (1,0): 0, (1,1): 0}
    for robot in robots:
        if robot.pos.x == x_middle  or robot.pos.y == y_middle:
            continue
        quadrant = (0 if robot.pos.x < x_middle else 1,
                    0 if robot.pos.y < y_middle else 1)
        quadrants[quadrant] += 1

    safety_score = 1
    for num_robots in quadrants.values():
        safety_score *= num_robots
    return safety_score
        
print(f"part1: {calculate_safety(move_robots(robots, 100), width, height)}")

def draw_robots(s, robots, width, height, bs):
    grid = {}
    for robot in robots:
        rect = pygame.Rect(robot.pos.x*bs, robot.pos.y*bs, bs, bs)
        pygame.draw.rect(s, (200,200,200), rect)


import pygame
pygame.init()
s = pygame.display.set_mode((width*6, height*6))

clock = pygame.time.Clock()
i = 0
direction = 0
while True:
    clock.tick(30)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                i-=1
            elif event.key == pygame.K_RIGHT:
                i+=1
            elif event.key == pygame.K_UP:
                direction = 1
            elif event.key == pygame.K_DOWN:
                direction = -1
        if event.type == pygame.KEYUP:
            direction = 0

    pygame.display.set_caption(str(i))
    s.fill((0,0,0))
    draw_robots(s, move_robots(robots, i), width, height, 5)
    pygame.display.flip()
    i+=direction
