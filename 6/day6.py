import sys

obstacles = {}
with open(sys.argv[1]) as f:
    y = 0
    for line in f:
        x = 0
        for c in line.strip():
            if c == '#':
               obstacles[(x,y)] = 1
            elif c == '.':
                obstacles[(x,y)] = 0
            else:
                guard = ((x,y),(0,-1))
                obstacles[(x,y)] = 0
            x += 1
        y += 1


def get_next_dir(cur_dir):
    if cur_dir == (0,-1):
        return (1,0)
    if cur_dir == (1,0):
        return (0,1)
    if cur_dir == (0,1):
        return (-1,0)
    if cur_dir == (-1,0):
        return (0,-1)
    print(f"WTF, cur_dir={cur_dir}")


def track_guard(obstacles, guard):
    visited = dict()
    trace = set()
    while True:
        next_pos = (guard[0][0]+guard[1][0],guard[0][1]+guard[1][1])
        if next_pos not in obstacles:
            break

        if obstacles[next_pos]:
            guard = (guard[0],get_next_dir(guard[1]))
            continue

        visited[next_pos] = True
        guard = (next_pos,guard[1])
        if guard in trace:
            return None
        trace.add(guard)

    return visited

visited = track_guard(obstacles, guard)

print(len(visited))

loops = 0
for pos in visited:
    if pos == guard[0]:
        continue
    obstacles[pos] = 1
    if not track_guard(obstacles, guard):
        loops += 1
    obstacles[pos] = 0

print(loops)
