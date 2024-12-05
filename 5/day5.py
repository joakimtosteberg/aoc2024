import sys

def valid_order(pages, rules):
    for i in range(1, len(pages)):
        if pages[i] not in rules:
            continue
        for j in range(0, i):
            if pages[j] in rules[pages[i]]:
                return False
    return True

def fix_order(pages, rules):
    ordered = []
    while pages:
        for page in pages:
            if page not in rules:
                ordered.insert(0, page)
                pages.remove(page)
                break

            found = False
            for other_page in pages:
                if other_page == page:
                    continue
                if other_page in rules[page]:
                    found = True
                    break
            if not found:
                ordered.insert(0, page)
                pages.remove(page)
                break

    return ordered

rules = {}
valid_sum = 0
fixed_sum = 0
with open(sys.argv[1]) as f:
    for line in f:
        row = line.strip()
        if not row:
            break
        rule = [int(p) for p in row.split("|")]
        if rule[0] not in rules:
            rules[rule[0]] = set()
        rules[rule[0]].add(rule[1])

    for line in f:
        pages = [int(p) for p in line.strip().split(",")]
        if valid_order(pages, rules):
            valid_sum += pages[int(len(pages)/2)]
        else:
            pages = fix_order(set(pages), rules)
            fixed_sum += pages[int(len(pages)/2)]


print(f"initial valid: {valid_sum}")
print(f"fixed valid: {fixed_sum}")
