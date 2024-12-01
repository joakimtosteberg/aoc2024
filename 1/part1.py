import sys
h1 = []
h2 = []
with open(sys.argv[1], "r") as f:
    for line in f:
        pair = line.split()
        h1.append(int(pair[0]))
        h2.append(int(pair[1]))


dist = 0
for a, b in zip(sorted(h1), sorted(h2)):
    dist += abs(a-b)

print(dist)
