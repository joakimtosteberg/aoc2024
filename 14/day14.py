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
