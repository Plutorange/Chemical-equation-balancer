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
    algebraic = sympy.solve(eval(equation))
    numeric = sympy.nroots(eval(equation))
    view = input('Do you want the answers in the algebraic or numeric form? ')
    if view == 'algebraic':
        return algebraic
    elif view == 'numeric':
        return numeric
    else:
        print('There is no such option, try again.')
        view = input('Do you want the answers in the algebraic or numeric form? ')


def solve_equation():
    eq = input('Please enter equation: ')
    equation = analyze(eq)
    answers = solve(equation)
    [print(f'Root {i + 1}: {answers[i]}') for i in range(len(answers))]


if __name__ == "__main__":
    solve_equation()
