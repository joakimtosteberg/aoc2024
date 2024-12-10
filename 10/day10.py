import sys

heightmap = dict()
trailheads = list()
with open(sys.argv[1]) as f:
    y = 0
    for line in f:
        x = 0
        for c in line.strip():
            h = int(c)
            heightmap[(x,y)] = h
            if h == 0:
                trailheads.append((x,y))
            x += 1
        y += 1

def search(heightmap, pos, h, reached):
    if h == 10:
        if reached is None:
            return 1
        new = pos not in reached
        reached.add(pos)
        return 1 if new else 0
    found_trails = 0
    for step in [(0,1),(0,-1),(1,0),(-1,0)]:
        next_pos = (pos[0]+step[0],pos[1]+step[1])
        if heightmap.get(next_pos, -1) != h:
            continue
        found_trails += search(heightmap, next_pos, h+1, reached)
    return found_trails


total_score = 0
total_rating = 0
for trailhead in trailheads:
    total_score += search(heightmap, trailhead, 1, set())
    total_rating += search(heightmap, trailhead, 1, None)

print(f"part1: {total_score}")
print(f"part2: {total_rating}")
