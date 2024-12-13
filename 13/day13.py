import numpy as np
import re
import sys

class Claw:
    def __init__(self, buttons, prize):
        self.buttons = buttons
        self.prize = prize

    def min_cost(self):
        s = np.linalg.solve(np.array([[self.buttons[0].x, self.buttons[1].x],
                                     [self.buttons[0].y, self.buttons[1].y]]),
                           np.array([self.prize.x, self.prize.y]))
        a = round(s[0])
        b = round(s[1])

        eps = 0.001
        if abs(a-s[0]) < eps and abs(b-s[1]) < eps and a >= 0 and b >= 0:
            return a*self.buttons[0].cost + b*self.buttons[1].cost
        return -1

class Pair:
    def __init__(self, x, y, cost):
        self.x = x
        self.y = y
        self.cost = cost

def parse_button(line):
    m = re.search(r"^Button (A|B): X\+(\d+), Y\+(\d+)$", line)
    return Pair(int(m.group(2)), int(m.group(3)), 3 if m.group(1) == "A" else 1)

def parse_prize(line):
    m = re.search(r"^Prize: X=(\d+), Y=(\d+)$", line)
    return Pair(int(m.group(1)), int(m.group(2)), 0)

claws = []
with open(sys.argv[1]) as f:
    while True:
        claws.append(Claw([parse_button(f.readline().strip()),
                           parse_button(f.readline().strip())],
                          parse_prize(f.readline().strip())))
        if not f.readline():
            break
        


def best_cost(claws):
    best_cost = 0
    for claw in claws:
        cost = claw.min_cost()
        if cost != -1:
            best_cost += cost
    return best_cost

print(best_cost(claws))
    

for claw in claws:
    claw.prize.x += 10000000000000
    claw.prize.y += 10000000000000

print(best_cost(claws))
