import sys

letters = {}
with open(sys.argv[1]) as f:
    y=0
    for line in f:
       x=0
       for c in line.strip():
           letters[(x,y)] = c
           x+=1
           width = x
       y+=1
       height = y


def find_word(letters, width, height, pos, step, word):
    if not word:
        return True

    if pos[0] < 0 or pos[0] >= width or pos[1] < 0 or pos[1] >= height:
        return False

    if letters[pos] != word[0]:
        return False

    next_pos = (pos[0]+step[0],pos[1]+step[1])
    return find_word(letters, width, height, next_pos, step, word[1:])

num = 0
for y in range(0,height):
    for x in range(0,width):
        for step in [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]:
            if find_word(letters, width, height, (x,y), step, "XMAS"):
                num += 1

print(num)
