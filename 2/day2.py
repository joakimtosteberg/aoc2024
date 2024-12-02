import sys

reports = []
with open(sys.argv[1]) as f:
    for line in f:
        reports.append([int(n) for n in line.split()])

def is_safe(report, dampen, skip=None):
    safe = True
    report_direction = 0
    for i in range(0,len(report)-1):
        if i == skip:
            if i == 0:
                continue
            prev = report[i-1]
            cur = report[i+1]
        elif i+1 == skip:
            if skip==len(report)-1:
                continue
            prev = report[i]
            cur = report[i+2]
        else:
            prev = report[i]
            cur = report[i+1]
        diff = prev-cur
        diff_abs = abs(diff)
        direction = -1 if diff < 0 else 1
        if report_direction == 0:
            report_direction = direction

        if diff_abs == 0 or diff_abs > 3 or direction != report_direction:
            if dampen:
                for j in range(0,len(report)):
                    if is_safe(report, False, j):
                        return True
            return False

    return True

num_safe = 0
num_safe_dampened = 0
for report in reports:
    if is_safe(report, False):
        num_safe += 1

    if is_safe(report, True):
        num_safe_dampened += 1
        

print(f"part1: {num_safe}")
print(f"part2: {num_safe_dampened}")
