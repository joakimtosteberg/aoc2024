import sys

warehouse = {}
robot = None

movements = []
with open(sys.argv[1]) as f:
    # Read map
    y = 0
    while True:
        line = f.readline().strip()
        if not line:
            break
        x = 0
        for c in line:
            if c == '@':
                robot = (x,y)
                warehouse[(x,y)] = '.'
            else:
                warehouse[(x,y)] = c
            x += 1
        y += 1

    width = x
    height = y

    # Read movements
    while True:
        line = f.readline().strip()
        if not line:
            break

        for c in line:
            if c == '^':
                movements.append((0,-1))
            elif c == 'v':
                movements.append((0,1))
            elif c == '<':
                movements.append((-1,0))
            elif c == '>':
                movements.append((1,0))


def print_warehouse(warehouse, width, height, robot):
    for y in range(0, height):
        for x in range(0, width):
            if (x,y) == robot:
                print('@', end='')
            else:
                print(warehouse[(x,y)], end='')
        print()

def find_push_space(warehouse, pos, movement):
    while True:
        next_pos = (pos[0]+movement[0], pos[1]+movement[1])
        if warehouse[next_pos] == '.':
            return next_pos
        if warehouse[next_pos] == '#':
            return None
        pos = next_pos


def sum_box_coords(warehouse):
    coord_sum = 0
    for pos, item in warehouse.items():
        if item != 'O':
            continue
        coord_sum += pos[0] + pos[1]*100
    return coord_sum

for movement in movements:
    next_pos = (robot[0]+movement[0], robot[1]+movement[1])
    if warehouse[next_pos] == '#':
        continue

    if warehouse[next_pos] == 'O':
        free_pos = find_push_space(warehouse, next_pos, movement)
        if free_pos == None:
            continue
        warehouse[next_pos] = '.'
        warehouse[free_pos] = 'O'
        
    robot = next_pos

#print_warehouse(warehouse, width, height, robot)
print(sum_box_coords(warehouse))
