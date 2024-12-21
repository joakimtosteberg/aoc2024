import json
import sys

codes = []
with open(sys.argv[1]) as f:
    for line in f:
        codes.append(line.strip())

numpad = {(0,0): '7', (1,0): '8', (2,0): '9',
         (0,1): '4', (1,1): '5', (2,1): '6',
         (0,2): '1', (1,2): '2', (2,2): '3',
                     (1,3): '0', (2,3): 'A'}

dirpad = { (1,0): '^', (2,0): 'A',
           (0,1): '<', (1,1): 'v', (2,1): '>'}

directions = {(0,-1): '^', (0,1): 'v', (1,0): '>', (-1,0): '<'}


def get_paths(grid, directions):
    grid_paths = {}
    for start_pos in grid:
        next_positions = [start_pos]
        start_val = grid[start_pos]
        while next_positions:
            positions = next_positions
            next_positions = list()

            new_grid_paths = {}
            for pos in positions:
                val = grid[pos]
                for step in directions:
                    next_pos = (pos[0]+step[0], pos[1]+step[1])
                    if next_pos not in grid or next_pos == start_pos:
                        continue
                    next_val = grid[next_pos]
                    if (start_val,next_val) in grid_paths:
                        continue
                    if (start_val,next_val) not in new_grid_paths:
                        new_grid_paths[(start_val,next_val)] = set()
                    new_grid_paths[(start_val,next_val)].update([l + directions[step] for l in grid_paths.get((start_val,val), [""])])
                    next_positions.append(next_pos)

            for key, paths in new_grid_paths.items():
                grid_paths[key] = paths

    return grid_paths

numpad_paths = get_paths(numpad, directions)
dirpad_paths = get_paths(dirpad, directions)

def find_shortest_numpad_sequences(cur_digit, seq, numpad_paths):
    numpad_path = list()
    for next_digit in seq:
        numpad_path.append(numpad_paths[cur_digit,next_digit])
        cur_digit = next_digit
    return numpad_path

def find_shortest_sequences2(cur_value, values, paths):
    sequences = list()
    for next_value in values:
        if next_value == cur_value:
            sequences.append([['A']])
        else:
            sequences.append([path + ['A'] for path in paths[cur_value,next_value]])
        cur_value = next_value

    return build_sequences(sequences)


def find_shortest_sequences(cur_value, values, paths):
    sequences = list()
    for next_value in values:
        if next_value == cur_value:
            sequences.append(['A'])
        else:
            sequences.append([path + 'A' for path in paths[cur_value,next_value]])
        cur_value = next_value

    return sequences

def get_best_sequence_len(sequence, top=True):
    sequence_len = 0
    for step in sequence:
        best_step_len = None
        for step_option in step:
            if type(step_option) is list:
                option_len = get_best_sequence_len(step_option, False)
            else:
                option_len = len(step_option)
            if best_step_len is None or option_len < best_step_len:
                best_step_len = option_len
        sequence_len += best_step_len
    return sequence_len

def find_dirpad_sequences(sequence, dirpad_paths):
    new_sequence = list()
    for step in sequence:
        new_step = list()
        for step_option in step:
            if type(step_option) is list:
                new_step_option = find_dirpad_sequences(step_option, dirpad_paths)
            else:
                new_step_option = find_shortest_sequences('A', step_option, dirpad_paths)
            new_step.append(new_step_option)
        new_sequence.append(new_step)
    return new_sequence

robots = 2
complexity = 0
for code in codes:
    sequences = find_shortest_sequences('A', code, numpad_paths)
    for i in range(0,robots):
        sequences = find_dirpad_sequences(sequences, dirpad_paths)

    complexity += get_best_sequence_len(sequences) * int(code[0:-1])

print(complexity)
