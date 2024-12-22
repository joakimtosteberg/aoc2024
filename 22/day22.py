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


sequence_bananas = {}
secret_sum = 0
for secret in secrets:
    last = secret % 10
    local_lookup = set()
    seq_queue = collections.deque(maxlen=4)
    for i in range(0,2000):
        secret = get_next_secret(secret)
        price = secret % 10
        change = price - last
        last = price

        seq_queue.appendleft(change)
        if i < 3:
            continue
        seq = tuple(seq_queue)
        if seq not in local_lookup:
            local_lookup.add(seq)
            if seq not in sequence_bananas:
                sequence_bananas[seq] = price
            else:
                sequence_bananas[seq] += price

    secret_sum += secret

print(f"part1: {secret_sum}")
print(f"part2: {max(sequence_bananas.values())}")
