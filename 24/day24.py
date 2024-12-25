import re
import sys

wires = {}

gates = []

class Gate:
    def __init__(self, x, y, op, out):
        self.x = x
        self.y = y
        self.op = op
        self.out = out

with open(sys.argv[1]) as f:
    for line in f:
        row = line.strip()
        if not row:
            break
        item = row.split(': ')
        wires[item[0]] = int(item[1])


    gate_re = re.compile("^(\w+) (\w+) (\w+) -> (\w+)$")
    for line in f:
        m = gate_re.match(line.strip())
        gates.append(Gate(m.group(1),m.group(3), m.group(2), m.group(4)))

def simulate(input_gates, input_wires):
    gates = input_gates.copy()
    wires = input_wires.copy()
    while gates:
        remaining_gates = list() 
        for gate in gates:
            if not (gate.x in wires and gate.y in wires):
                remaining_gates.append(gate)
                continue

            if gate.op == 'AND':
                wires[gate.out] = wires[gate.x] & wires[gate.y]
            elif gate.op == 'OR':
                wires[gate.out] = wires[gate.x] | wires[gate.y]
            elif gate.op == 'XOR':
                wires[gate.out] = wires[gate.x] ^ wires[gate.y]
        gates = remaining_gates

    out_value = 0
    for wire,value in wires.items():
        if wire[0] != 'z':
            continue
        out_value += value*(2**int(wire[1:]))

    return out_value

print(f"part1: {simulate(gates, wires)}")

def simulate_input(gates, x, y):
    wires = {}
    for i in range(0,45):
        wires[f"x{i:0>2}"] = 1 if x & 2**i else 0
        wires[f"y{i:0>2}"] = 1 if y & 2**i else 0

    return simulate(gates, wires)


print(f"0x{simulate_input(gates, 0, 0xFFFFFFFFFFFFF):02x}")
