import re
import sys

with open(sys.argv[1]) as f:
        mem = f.read().strip()

#r = re.compile("mul\((\d{1,3}),(\d{1,3})\)")
#r = re.compile("(?:(mul)\((\d{1,3}),(\d{1,3})\))|(?:(do)\(\))")
r = re.compile("(?:(mul)\((\d{1,3}),(\d{1,3})\))|(?:(do)\(\))|(?:(don\'t)\(\))")
enabled = True
tot = 0
tot_enabled = 0
for match in r.findall(mem):
    if match[0]:
        prod = int(match[1])*int(match[2])
        tot += prod
        if enabled:
            tot_enabled += prod
    elif match[3]:
        enabled = True
    elif match[4]:
        enabled = False

print(tot)
print(tot_enabled)

