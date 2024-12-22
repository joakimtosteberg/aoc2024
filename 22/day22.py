import collections
import sys

secrets =[]
with open(sys.argv[1]) as f:
    for line in f:
        secrets.append(int(line.strip()))


def get_next_secret(secret):
    secret = ((secret << 6) ^ secret) & 0xffffff
    secret = ((secret >> 5) ^ secret) & 0xffffff
    secret = ((secret << 11) ^ secret) & 0xffffff
    return secret


secret_sum = 0
lookup = {}
for i in range(-9,10):
    lookup[i] = dict()
    for j in range(-9,10):
        lookup[i][j] = dict()
        for k in range(-9,10):
            lookup[i][j][k] = dict()
            for l in range(-9,10):
                lookup[i][j][k][l] = 0

max_bananas = 0
for secret in secrets:
    last = secret % 10
    local_lookup = set()
    seq = (0,0,0,0)
    for i in range(0,3):
        secret = get_next_secret(secret)
        price = secret % 10
        change = price - last
        last = price

        seq = (seq[1], seq[2], seq[3], change)
    for i in range(3,2000):
        secret = get_next_secret(secret)
        price = secret % 10
        change = price - last
        last = price

        seq = (seq[1], seq[2], seq[3], change)
        if seq not in local_lookup:
            local_lookup.add(seq)
            lookup[seq[0]][seq[1]][seq[2]][seq[3]] += price

    secret_sum += secret

print(f"part1: {secret_sum}")
max_bananas = 0
for i in lookup.values():
    for j in i.values():
        for k in j.values():
            for l in k.values():
               max_bananas = max(max_bananas, l) 
print(f"part2: {max_bananas}")
