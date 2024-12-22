import sys

sys.setrecursionlimit(10000)

track = {}
start = None

with open(sys.argv[1]) as f:
    y = 0
    for line in f:
        x = 0
        for c in line.strip():
            pos=(x,y)
            if c == 'S':
                track[pos] = '.'
                start = pos
            else:
                track[pos] = c
            x += 1
        y += 1

def find_path(track, path, visited):
    pos = path[-1]
    visited[pos] = len(path)-1
    for step in [(0,1),(0,-1),(1,0),(-1,0)]:
        next_pos = (pos[0]+step[0], pos[1]+step[1])
        if next_pos in visited:
            continue
        s = track.get(next_pos, '#')
        if s == '#':
            continue
        if s == 'E':
            visited[next_pos] = len(path)
            return path
        
        return find_path(track, path + [next_pos], visited)

def find_cheats(start_pos, cheat_time, track, visited, cheats):
    next_positions = [start_pos]
    cheat_visited = set(start_pos)
    for tick in range(1, cheat_time+1):
        positions = next_positions
        next_positions = list()
        for pos in positions:
            for step in [(0,1),(0,-1),(1,0),(-1,0)]:
                next_pos = (pos[0]+step[0], pos[1]+step[1])
                if next_pos in cheat_visited:
                    continue
                cheat_visited.add(next_pos)
                if next_pos not in track:
                    continue
                if next_pos in visited:
                    diff = visited[next_pos] - visited[start_pos] - tick
                    if diff > 0:
                        if not diff in cheats:
                            cheats[diff] = 1
                        else:
                            cheats[diff] += 1

                next_positions.append(next_pos)
        
visited = {}
path = find_path(track, [start], visited)

def calc_num_good_cheats(path, track, visited, cheat_time, cheat_limit):
    cheats = {}
    for pos in path:
        find_cheats(pos, cheat_time, track, visited, cheats)

    num_good_cheats = 0
    for cheat_earn in sorted(cheats):
        if cheat_earn >= cheat_limit:
            num_good_cheats += cheats[cheat_earn]
    return num_good_cheats

print(f"part1: {calc_num_good_cheats(path, track, visited, 2, 100)}")
print(f"part2: {calc_num_good_cheats(path, track, visited, 20, 100)}")
