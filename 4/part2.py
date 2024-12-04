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

def check_mas(letters, pos, step):
    pos_1 = (pos[0]+step[0], pos[1]+step[1])
    pos_2 = (pos[0]-step[0], pos[1]-step[1])

    return (letters[pos_1] == 'M' and letters[pos_2] == 'S') or (letters[pos_1] == 'S' and letters[pos_2] == 'M')
       
def check_x_mas(letters, pos):
    if letters[pos] != "A":
        return False

    return check_mas(letters, pos, (1,1)) and check_mas(letters, pos, (1,-1))

num = 0
for y in range(1,height-1):
    for x in range(1,width-1):
        if check_x_mas(letters, (x,y)):
            num += 1
            
print(num)
