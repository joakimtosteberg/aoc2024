import sys

designs = []
with open(sys.argv[1]) as f:
    patterns = f.readline().strip().split(', ')
    f.readline()
    for line in f:
        designs.append(line.strip())


def check_design(design, patterns, lookup):
    if design in lookup:
        return lookup[design]
    if not design:
        return 1
    possible = 0
    for pattern in patterns:
        if design.startswith(pattern):
            possible += check_design(design[len(pattern):], patterns, lookup)
    lookup[design] = possible
    return possible

possible_designs = 0
possible_design_combos = 0
lookup = {}
for design in designs:
    num = check_design(design, patterns, lookup)
    if num:
        possible_designs += 1
        possible_design_combos += num

print(f"part1: {possible_designs}")
print(f"part2: {possible_design_combos}")
