import sys

with open(sys.argv[1]) as f:
    stones = f.read().strip().split(' ')

def transform(stone):
    if stone == "0":
        return ["1"]
    if len(stone)%2 == 0:
        half = int(len(stone)/2)
        sec = stone[half:].lstrip("0")
        if not sec:
            sec = "0"
        return [stone[0:half], sec]
    return [str(int(stone) * 2024)]

def count_after_blinks(stones, blinks, lookup):
    total_count = 0
    if blinks == 0:
        return len(stones)
    for stone in stones:
        if (stone,blinks) not in lookup:
            lookup[(stone,blinks)] = count_after_blinks(transform(stone), blinks-1, lookup)
        total_count += lookup[(stone,blinks)]
    return total_count

print(count_after_blinks(stones, 25, dict()))
print(count_after_blinks(stones, 75, dict()))
