import re
import sys

reg_re = re.compile(r"^Register (.*?): (\d+)$")
program_re = re.compile("^Program: (\d+(?:,\d+)*)$")

registers = {}
program = []
with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        m = reg_re.match(line)
        if m:
            registers[m.group(1)] = int(m.group(2))
            continue

        m = program_re.match(line)
        if m:
            program = [int(p) for p in m.group(1).split(',')]
            continue

        print(f"bad line: {line}")

def get_combo_operand(program, registers, ip):
    val = program[ip]
    if val < 4:
        return val
    if val == 4:
        return registers['A']
    if val == 5:
        return registers['B']
    if val == 6:
        return registers['C']
    print("Invalid combo operand")

def get_literal_operand(program, ip):
    return program[ip]

#bst 4
#bxl #4
#cdv 5
#bxc 1
#bxl #4
#out 5
#adv 3
#jnz #0

#B = A%8
#B = B^4 = (B+4)%8
#C = A/2**B
#B = B^C
#B = B^4
#print B
#A = int(A/8)
#if A==0 exit

#B=(A%8+4)%8=(A+4)%8
#C=int(A/2**(A+4)%8)


def run_program(program, registers, return_on_output=False):
    ip = 0
    start = registers['A']
    output = []
    while ip < len(program):
        instruction = program[ip]
        ip += 1
        if instruction in [0, 6, 7]:
            dst = 'A' if instruction == 0 else 'B' if instruction == 6 else 'C'
            registers[dst] = int(registers['A'] / pow(2,get_combo_operand(program, registers, ip)))
        elif instruction == 1:
            registers['B'] = registers['B'] ^ get_literal_operand(program, ip)
        elif instruction == 2:
            registers['B'] = get_combo_operand(program, registers, ip) % 8
        elif instruction == 3:
            if registers['A']:
                ip = get_literal_operand(program, ip)
                continue
        elif instruction == 4:
            registers['B'] = registers['B'] ^ registers['C']
        elif instruction == 5:
            out = get_combo_operand(program, registers, ip) % 8
            if return_on_output:
                return out
            output.append(out)
        else:
            print("Unknown instruction")
        ip += 1
 
    return output


print(f"part1: {','.join([str(o) for o in run_program(program, registers)])}")


def find_value(program, registers, a, pos):
    if pos == -1:
        return a

    best = None
    wanted = program[pos]
    for j in range(0,8):
        if a == 0 and j == 0:
            continue
        next_a = (a << 3) | j
        registers['A'] = next_a
        got = run_program(program, registers, True)
        if got == wanted:
            found = find_value(program, registers, next_a, pos-1)
            if found is not None:
                if not best or found < best:
                    best = found
            
    return best

print(f"part2: {find_value(program, registers, 0, len(program)-1)}")

