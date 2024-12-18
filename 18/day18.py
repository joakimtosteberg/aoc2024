import sys

blocked_list = list()

with open(sys.argv[1]) as f:
    for line in f:
        pos_list = line.strip().split(',')
        pos = (int(pos_list[0]), int(pos_list[1]))
        blocked_list.append(pos)

def bfs(blocked_list, size, num_bytes):
    blocked = set(blocked_list[0:num_bytes])
    goal = (size-1,size-1)
    visited = set()
    num_steps = 0
    next_positions = [(0,0)]
    while next_positions:
        positions = next_positions
        next_positions = list()
        num_steps += 1

        for pos in positions:
            for step in [(0,1),(0,-1),(1,0),(-1,0)]:
                next_pos = (pos[0]+step[0], pos[1]+step[1])
                if next_pos in visited:
                    continue
                if next_pos == goal:
                    return num_steps
                if next_pos[0] < 0 or next_pos[0] >= size or next_pos[1] < 0 or next_pos[1] >= size:
                    continue
                if next_pos in blocked:
                    continue
                visited.add(next_pos)
                next_positions.append(next_pos)
    return None

print(f"part1: {bfs(blocked_list, 71, 1024)}")
        
for i in range(1024, len(blocked_list)):
    if bfs(blocked_list, 71, i) == None:
        print(f"part2: {blocked_list[i-1]}")
        break
