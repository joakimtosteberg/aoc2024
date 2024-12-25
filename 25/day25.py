import sys

def read_schematic(f):
    type_line = f.readline().strip()
    if not type_line:
        return None, None

    is_lock = type_line[0] == '#'
    heights = [0 if is_lock else 5]*5
    for i in range(0,5):
        pins = f.readline().strip()
        for pin in range(0,5):
            if is_lock and pins[pin] == '#':
                heights[pin] += 1
            elif not is_lock and pins[pin] == '.':
                heights[pin] -= 1
    f.readline()
    f.readline()
    return heights, is_lock


locks = []
keys = []

with open(sys.argv[1]) as f:
    while True:
        heights, is_lock = read_schematic(f)
        if not heights:
            break
        if is_lock:
            locks.append(heights)
        else:
            keys.append(heights)


def no_overlap(lock, key):
    for lock_pin_height, key_pin_height in zip(lock, key):
        if lock_pin_height + key_pin_height > 5:
            return False

    return True

fits = 0
for key in keys:
    for lock in locks:
        if no_overlap(lock, key):
            fits += 1

print(f"part1: {fits}")
