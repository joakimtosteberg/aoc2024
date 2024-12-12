import sys

garden = {}

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __lt__(self,other):
        return (self.x, self.y) < (other.x , other.y)

    def __add__(self, other):
        return Pos(self.x+other.x, self.y+other.y)

    def __repr__(self):
        return f"({self.x},{self.y})"
        
with open(sys.argv[1]) as f:
    y = 0
    for line in f:
        x = 0
        for c in line.strip():
            garden[Pos(x,y)] = c
            x += 1
        y += 1
        width = x
    height = y

def calculate_sides(fences, prev_step, next_step):
    visited = set()
    sides = 0
    for fence in fences:
        if fence in visited:
            continue
        sides += 1
        pos = fence
        visited.add(pos)
        prev_pos = pos+prev_step
        while prev_pos in fences:
            pos = prev_pos
            visited.add(pos)
            prev_pos = pos+prev_step

        next_pos = pos+next_step
        while next_pos in fences:
            pos = next_pos
            visited.add(pos)
            next_pos = pos+next_step

    return sides

def explore_region(start, plot, garden, visisted):
    area = 1
    perimeter = 0
    next_positions = [start]
    visited.add(start)
    positions = list()
    v_fences = set()
    h_fences = set()
    while next_positions:
        positions = next_positions
        next_positions = list()
        for position in positions:
            for step in [Pos(0,1), Pos(0,-1), Pos(1,0), Pos(-1,0)]:
                next_pos = position + step
                if garden.get(next_pos, None) != plot:
                    fence_pos = position + Pos(step.x/3, step.y/3)
                    if step.x:
                        h_fences.add(fence_pos)
                    else:
                        v_fences.add(fence_pos)
                    perimeter += 1
                    continue

                if next_pos in visited:
                    continue

                area += 1
                visited.add(next_pos)
                next_positions.append(next_pos)

    v_sides = calculate_sides(v_fences, Pos(-1,0), Pos(1,0))
    h_sides = calculate_sides(h_fences, Pos(0,-1), Pos(0,1))
    sides = h_sides+v_sides

    return area,perimeter,sides
        

visited = set()
total_cost = 0
total_cost2 = 0
for pos, plot in garden.items():
    if pos in visited:
        continue

    area, perimeter, sides = explore_region(pos, plot, garden, visited)
    cost = area*perimeter
    total_cost += cost
    cost2 = area*sides
    total_cost2 += cost2

print(total_cost)
print(total_cost2)
