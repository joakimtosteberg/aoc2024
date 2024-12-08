import sys

antennas = {}

with open(sys.argv[1]) as f:
    y = 0
    for line in f:
        x = 0
        for c in line.strip():
            if c != '.':
                if c not in antennas:
                    antennas[c] = [(x,y)]
                else:
                    antennas[c].append((x,y))

            x += 1
        y += 1
        width = x
    height = y

def within_bounds(pos, width, height):
    return pos[0] >= 0 and pos[0] < width and pos[1] >= 0 and pos[1] < height

def get_antinodes(pos1, pos2, width, height):
    dx = pos1[0]-pos2[0]
    dy = pos1[1]-pos2[1]
    a1 = (pos1[0]+dx,pos1[1]+dy)
    a2 = (pos2[0]-dx,pos2[1]-dy)
    antinodes = set()
    if within_bounds(a1, width, height):
        antinodes.add(a1)
    if within_bounds(a2, width, height):
        antinodes.add(a2)
    return antinodes

def get_all_antinodes(pos1, pos2, width, height):
    dx = pos1[0]-pos2[0]
    dy = pos1[1]-pos2[1]
    i = 0
    antinodes = set()
    while True:
        antinode = (pos1[0]+dx*i,pos1[1]+dy*i)
        if not within_bounds(antinode, width, height):
            break
        antinodes.add(antinode)
        i += 1

    i = -1
    while True:
        antinode = (pos1[0]+dx*i,pos1[1]+dy*i)
        if not within_bounds(antinode, width, height):
            break
        antinodes.add(antinode)
        i -= 1
    return antinodes

antinodes = set()
all_antinodes = set()
for freq,positions in antennas.items():
    for i in range(0, len(positions)):
        for j in range(i+1, len(positions)):
            antinodes.update(get_antinodes(positions[i], positions[j], width, height))
            all_antinodes.update(get_all_antinodes(positions[i], positions[j], width, height))


print(f"part1: {len(antinodes)}")
print(f"part2: {len(all_antinodes)}")
