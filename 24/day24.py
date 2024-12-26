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

    def __repr__(self):
        return f"{self.x} {self.op} {self.y} -> {self.out}"

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

swap = [('ffj','z08'), ('gjh','z22'), ('jdr','z31'),('kfm','dwp')]
swap_list = []
swap_dict = {}
for pair in swap:
    swap_dict[pair[0]] = pair[1]
    swap_dict[pair[1]] = pair[0]
    swap_list.append(pair[0])
    swap_list.append(pair[1])

print(f"part2: {','.join(sorted(swap_list))}")

for gate in gates:
    if gate.out in swap_dict:
        gate.out = swap_dict[gate.out]

gate_dict = {}
for gate in gates:
    gate_dict[gate.out] = gate

adders = {}
local_carry = {}
carry_outs = {}
bad_gates = list()
for gate in gates:
    if gate.x[0] in ['x','y']:
        if gate.op == "XOR":
            adders[gate.out] = gate
        elif gate.op == "AND":
            local_carry[gate.out] = gate
        elif gate.op == "OR":
            carry_outs[gate.out] = gate
        else:
            print(f"Bad gate: {gate}")
        if gate.out[0] == 'z' and gate.out != 'z00':
            print(f"Exepcted input gate to not go to output: {gate}")
            bad_gates.append(gate)


carry_adders = {}
carry_overs = {}
for gate in gates:
    if gate.op == "XOR" and gate.out not in adders:
        carry_adders[gate.out] = gate
    elif gate.op == "AND" and gate.out not in local_carry:
        carry_overs[gate.out] = gate


for adder in adders.values():
    if adder.out not in gate_dict:
        print(f"Adder directly output to final: {adder}")

    if gate_dict[adder.out].op != "XOR":
        print(f"Adder not outputting to carry adder: {adder}")


for carry_adder in carry_adders.values():
    if carry_adder.out[0] != 'z':
        bad_gates.append(carry_adder)
        print(f"Exepcted carry adder to go to output: {carry_adder}")

    add_in = None
    if carry_adder.x in adders:
        add_in = carry_adder.x
    if carry_adder.y in adders:
        add_in = carry_adder.y

    if not add_in:
        print(f"Carry adder has no adders as input: {carry_adder}")

    carry_in = None
    if carry_adder.x in carry_outs:
        carry_in = carry_adder.x
    if carry_adder.y in carry_outs:
        carry_in = carry_adder.y

    if not add_in:
        print(f"Carry adder has no carry as input: {carry_adder}")
