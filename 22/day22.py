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


changes = []
prices = []

secret_sum = 0
for secret in secrets:
    changes.append([])
    last = secret % 10
    prices.append([])
    for i in range(0,2000):
        secret = get_next_secret(secret)
        price = secret % 10
        changes[-1].append(price - last)
        prices[-1].append(price)
        last = price
    secret_sum += secret

print(f"part1: {secret_sum}")

sequence_bananas = {}
for change, price in zip(changes,prices):
    local_lookup = set()
    for i in range(4,len(change)+1):
        sequence = tuple(change[i-4:i])
        if sequence in local_lookup:
            continue
        local_lookup.add(sequence)
        if sequence not in sequence_bananas:
            sequence_bananas[sequence] = price[i-1]
        else:
            sequence_bananas[sequence] += price[i-1]

print(f"part2: {max(sequence_bananas.values())}")
