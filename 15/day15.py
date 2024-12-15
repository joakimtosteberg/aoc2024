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

def move_robots_simple(warehouse, robot, movements):
    warehouse = warehouse.copy()
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
    return warehouse

def expand_warehouse(warehouse, robot):
    new_warehouse = {}
    for pos, item in warehouse.items():
        if item in ['#', '.']:
            new_warehouse[(pos[0]*2,pos[1])] = item
            new_warehouse[(pos[0]*2+1,pos[1])] = item
        elif item == 'O':
            new_warehouse[(pos[0]*2,pos[1])] = '['
            new_warehouse[(pos[0]*2+1,pos[1])] = ']'
    return new_warehouse, (robot[0]*2, robot[1])

def do_push(warehouse, pos, movement, dry_run):
    # X-axis movement
    if movement[0]:
        next_pos = (pos[0]+movement[0], pos[1]+movement[1])
        if warehouse[next_pos] == '#':
            return False
        if warehouse[next_pos] == '.' or do_push(warehouse, next_pos, movement, dry_run):
            if not dry_run:
                warehouse[next_pos] = warehouse[pos]
                warehouse[pos] = '.'
            return True
        return False

    # Y-axis movement
    positions = [pos]
    if warehouse[pos] == '[':
        positions.append((pos[0]+1,pos[1]))
    else:
        positions.append((pos[0]-1,pos[1]))

    for pos in positions:
        next_pos = (pos[0]+movement[0], pos[1]+movement[1])
        if warehouse[next_pos] == '#':
            return False
        if warehouse[next_pos] == '.':
            continue
        if not do_push(warehouse, next_pos, movement, dry_run=dry_run):
            return False

    if not dry_run:
        for pos in positions:
            next_pos = (pos[0]+movement[0], pos[1]+movement[1])
            warehouse[next_pos] = warehouse[pos]
            warehouse[pos] = '.'
    return True
        
    

def move_robots_recursive(warehouse, robot, movements):
    warehouse = warehouse.copy()
    for movement in movements:
        next_pos = (robot[0]+movement[0], robot[1]+movement[1])
        if warehouse[next_pos] == '#':
            continue

        if warehouse[next_pos] in ['[', ']']:
            if not do_push(warehouse, next_pos, movement, dry_run=True):
                continue
            do_push(warehouse, next_pos, movement, dry_run=False)

        robot = next_pos
    return warehouse, robot

def sum_box_coords(warehouse):
    coord_sum = 0
    for pos, item in warehouse.items():
        if item not in ['O', '[']:
            continue
        coord_sum += pos[0] + pos[1]*100
    return coord_sum

print(f"part1: {sum_box_coords(move_robots_simple(warehouse, robot, movements))}")
warehouse, robot = expand_warehouse(warehouse, robot)
warehouse, robot = move_robots_recursive(warehouse, robot, movements)
print(f"part2: {sum_box_coords(warehouse)}")
