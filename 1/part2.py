import sys
h1 = dict()
h2 = dict()
with open(sys.argv[1], "r") as f:
    for line in f:
        a, b = [int(n) for n in line.split()]
        if a in h1:
            h1[a] += 1
        else:
            h1[a] = 1

        if b in h2:
            h2[b] += 1
        else:
            h2[b] = 1


score = 0
for val,cnt in h1.items():
    score += val*cnt*h2.get(val,0)

print(score)
