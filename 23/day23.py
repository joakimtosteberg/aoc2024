import sys

connections = {}
with open(sys.argv[1]) as f:
    for line in f:
        connection = line.strip().split('-')
        if not connection[0] in connections:
            connections[connection[0]] = set()
        if not connection[1] in connections:
            connections[connection[1]] = set()
        connections[connection[0]].add(connection[1])
        connections[connection[1]].add(connection[0])

def get_tri_connected_sets(computer, connections):
    connected_sets = set()
    for other in connections[computer]:
        for third in connections[other]:
            if third in connections[computer]:
                sorted_set = sorted([computer, other, third])
                connected_sets.add((sorted_set[0], sorted_set[1], sorted_set[2]))
    return connected_sets


tri_connected_sets = set()
for computer in set(connections):
   tri_connected_sets.update(get_tri_connected_sets(computer, connections))


filtered_tri_sets = list()
for tri_connected_set in tri_connected_sets:
    if tri_connected_set[0][0] == 't' or tri_connected_set[1][0] == 't' or tri_connected_set[2][0] == 't':
        filtered_tri_sets.append(tri_connected_set)

print(f"part1: {len(filtered_tri_sets)}")


def get_best_set(connected_set, candidates, connections, best_set_len):
    if len(connected_set) + len(candidates) <= best_set_len:
        return set()
    if not candidates:
        return connected_set.copy()
    connected_sets = list()
    best_set = set()
    for i in range(0, len(candidates)):
        candidate = candidates[i]
        for other in connected_set:
            if candidate not in connections[other]:
                break
        else:
            connected_set.add(candidate)
            found = get_best_set(connected_set, candidates[i+1:], connections, best_set_len)
            if len(found) > len(best_set):
                best_set = found
            connected_set.remove(candidate)
        found = get_best_set(connected_set, candidates[i+1:], connections, best_set_len)
        if len(found) > len(best_set):
                best_set = found
    return best_set

best_set = set()
for computer in set(connections):
    found = get_best_set(set([computer]), list(connections[computer]), connections, len(best_set))
    if len(found) > len(best_set):
        best_set = found
    del connections[computer]
    for connection in connections.values():
        connection.discard(computer)

print(f"part2: {','.join(sorted(best_set))}")
