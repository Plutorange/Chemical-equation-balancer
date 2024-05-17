from matplotlib import pyplot as plt


def analyze(eq):
    equation, var, num, side = [{}, {}], '', '', 0
    for i in eq:
        if i.isalpha() or i == '^':
            var += i
        elif i.isdigit() and '^' in var:
            var += i
        elif i.isdigit() or i == '.':
            num += i
        elif i in '-+':
            if num == '':
                num = '1'
            equation[side][var] = num
            var, num = '', ''
            if i == '-':
                num = '-'
        elif i == '=':
            if num == '':
                num = '1'
            equation[side][var] = num
            side += 1
            var, num = '', ''
        elif i == ' ':
            continue
        else:
            print(i, 'unexpected value')
    equation[side][var] = num
    return equation


def solve(equation):
    solution, roots = {}, []
    for i in range(-10, 10):
        res = 0
        for j in equation[0]:
            if '^' in j:
                res += i ** int(j.split('^')[1]) * float(equation[0][j])
            elif j == '':
                res += float(equation[0][j])
            else:
                res += i * float(equation[0][j])
        if res == 0:
            roots.append(i)
            multiplicators = [float(equation[0][max(equation[0].keys())])]
            equation[0].pop(max(equation[0].keys()))
            for j in sorted(equation[0].keys(), reverse=True):
                multiplicators.append(multiplicators[-1] * i + float(equation[0][j]))
            for j in zip(sorted(equation[0].keys(), reverse=True), multiplicators):
                equation[0][j[0]] = j[1]
            if not equation[0]:
                break
    return equation, roots


def solve_equation():
    eq = input('Please enter equation: ')
    equation = analyze(eq)
    equation, roots = solve(equation)
    print(equation)
    print(roots)
    fin_equation = ''
    for i in roots:
        if i < 0:
            fin_equation += f'(x - {abs(i)})'
        elif i > 0:
            fin_equation += f'(x + {abs(i)})'
        else:
            fin_equation += 'x'
    print(fin_equation)
    if equation[0]:
        fin_equation += '('
        for i in equation[0]:
            if equation[0][i] == 0:
                continue
            elif equation[0][i] == 1:
                fin_equation += i
            else:
                if equation[0][i] % 1 == 0:
                    equation[0][i] = int(equation[0][i])
                fin_equation += str(equation[0][i]) + i
        fin_equation += ')'
    print(fin_equation)
    graph = input('Do you want to see the graph? (yes/no): ')
    if graph == 'yes':
        equation = analyze(eq)
        x_coords, y_coords = [], []
        for i in range(-10, 11):
            res = 0
            for j in equation[0]:
                if '^' in j:
                    res += i ** int(j.split('^')[1]) * float(equation[0][j])
                elif j == '':
                    res += float(equation[0][j])
                else:
                    res += i * float(equation[0][j])
            x_coords.append(i)
            y_coords.append(res)
        plt.title(eq)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.plot(roots, [0] * len(roots), 'ob')
        plt.plot(x_coords, y_coords, 'b')
        plt.plot([min(0, min(x_coords)), max(0, max(x_coords))], [0, 0], 'k')
        plt.plot([0, 0], [min(0, min(y_coords)), max(0, max(y_coords))], 'k')
        plt.grid()
        plt.show()


if __name__ == '__main__':
    solve_equation()
