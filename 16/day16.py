import sys

sys.setrecursionlimit(10000)

maze = {}
reindeer = None

with open(sys.argv[1]) as f:
    y = 0
    for line in f:
        x = 0
        for c in line.strip():
            pos=(x,y)
            if c == 'S':
                maze[pos] = '.'
                reindeer = (pos,(1,0),0)
            else:
                maze[pos] = c
            x += 1
        y += 1

best = {}

def get_next_states(reindeer):
    cur_pos = reindeer[0]
    cur_dir = reindeer[1]
    cur_cost = reindeer[2]
    steps = [((cur_pos[0]+cur_dir[0],cur_pos[1]+cur_dir[1]), cur_dir, cur_cost+1)]
    if cur_dir[0]:
        steps.append((cur_pos, (0,1), cur_cost+1000))
        steps.append((cur_pos, (0,-1), cur_cost+1000))
        steps.append((cur_pos, (-cur_dir[0],0), cur_cost+2000))
    else:
        steps.append((cur_pos, (1,0), cur_cost+1000))
        steps.append((cur_pos, (-1,0), cur_cost+1000))
        steps.append((cur_pos, (0,-cur_dir[1]), cur_cost+2000))
    return steps

def find_path(reindeer, maze, costs):
    next_states = get_next_states(reindeer)
    recurse_states = list()
    for state_cost in next_states:
        state = (state_cost[0],state_cost[1])
        pos = state_cost[0]

        if maze[pos] == '#':
            continue

        if state in costs['costs'] and state_cost[2] > costs['costs'][state]:
            continue

        if costs['best'] and state_cost[2] > costs['best']:
            continue

        costs['costs'][state] = state_cost[2]
        if maze[pos] == 'E':
            costs['best'] = state_cost[2]
            return state_cost[2], {pos}

        recurse_states.append(state_cost)

    min_cost = None
    min_cost_tiles = set()
    for recurse_state in recurse_states:
        cost, tiles = find_path(recurse_state, maze, costs)
        if not cost:
            continue

        if not min_cost or cost < min_cost:
            min_cost = cost
            min_cost_tiles = tiles
            min_cost_tiles.add(recurse_state[0])
            min_cost_tiles.add(reindeer[0])
        elif cost == min_cost:
            min_cost_tiles.update(tiles)
            min_cost_tiles.add(recurse_state[0])
            min_cost_tiles.add(reindeer[0])

    return min_cost, min_cost_tiles

costs = {'best': None, 'costs': dict()}
min_cost, min_cost_tiles = find_path(reindeer, maze, costs)
print(f"part1: {min_cost}")
print(f"part2: {len(min_cost_tiles)}")
