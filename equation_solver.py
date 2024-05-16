import sympy
from sympy.abc import x


def analyze(eq):
    eq = eq.replace('^', '**')
    equation = eq[0]
    for i in range(1, len(eq)):
        if eq[i] == 'x' and eq[i - 1].isdigit():
            equation += '*'
        equation += eq[i]
    equation = equation[:equation.find('=')]
    return equation


def solve(equation):
    print(sympy.solve(eval(equation)))
    print(sympy.nroots(eval(equation)))


def solve_equation():
    eq = input('Please enter equation: ')
    equation = analyze(eq)
    print(equation)
    solve(equation)


if __name__ == "__main__":
    solve_equation()
