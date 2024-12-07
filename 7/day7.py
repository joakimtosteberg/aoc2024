import sys

equations = []
with open(sys.argv[1]) as f:
    for line in f:
        s = line.strip().split(':')
        result = int(s[0])
        numbers = [int(n) for n in s[1].strip().split(' ')]
        equations.append((result, numbers))

operators = [lambda x, y: x + y,
             lambda x, y: x * y]


def operate(total, numbers, index, expected, operators):
    if index == len(numbers):
        return total == expected
    if total > expected:
        return False

    for operator in operators:
        if operate(operator(total, numbers[index]), numbers, index+1, expected, operators):
            return True

    return False
    

def test_equations(equations, operators):
    ok_sum = 0
    for equation in equations:
        if operate(equation[1][0], equation[1], 1, equation[0], operators):
            ok_sum += equation[0] 
    return ok_sum
        
print(test_equations(equations, operators))

operators.append(lambda x, y: int(str(x) + str(y)))
print(test_equations(equations, operators))
