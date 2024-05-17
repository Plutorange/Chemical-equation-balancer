import sympy
from sympy.abc import x
import matplotlib.pyplot as plt


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
    while True:
        if view == 'algebraic':
            try:
                float(algebraic[0])
            except TypeError:
                algebraic = numeric
                print('Unable to get roots in algebraic form.')
                print('Printing numeric ones.')
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
    graph = input('Do you want to see the graph of the function? ')
    while True:
        if graph == 'yes':
            x_coords, y_coords = [], []
            for i in range(-50, 51):
                x_coords.append(i / 10)
                y_coords.append(eval(equation.replace('x', str(i / 10))))
            zeros = []
            for i in answers:
                try:
                    zeros.append(eval(equation.replace('x', str(i))))
                    zeros[-1] = i
                except NameError:
                    pass
            plt.title(eq)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid()
            plt.plot(zeros, [0] * len(zeros), 'ob')
            plt.plot(x_coords, y_coords, 'b')
            plt.plot([min(0, min(x_coords)), max(0, max(x_coords))], [0, 0], 'k')
            plt.plot([0, 0], [min(0, min(y_coords)), max(0, max(y_coords))], 'k')
            plt.show()
            return input('Type any key to leave.')
        elif graph != 'no':
            print('There is no such option, try again.')
            graph = input('Do you want to see the graph of the function? ')
        else:
            break


if __name__ == "__main__":
    solve_equation()
