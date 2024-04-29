import sys


def analyze():  # gives reactants and products
    reactants, products = [], []
    for i in range(len(equation)):
        for j in equation[i]:
            if i == 0:
                reactants.append({})
            else:
                products.append({})
            elem, n, scobe = '', '0', 1
            for k in j:
                if k == '(':
                    scobe = int(j[j.find(')') + 1:])
                    if i == 0:
                        reactants[-1].update({elem: max(1, int(n))})
                        elem, n = '', '0'
                    else:
                        products[-1].update({elem: max(1, int(n))})
                        elem, n = '', '0'
                elif k == ')':
                    break
                elif k.isalpha() and k == k.capitalize():
                    if elem == '':
                        elem = k
                    elif i == 0:
                        if elem in reactants[-1]:
                            reactants[-1][elem] += max(1, int(n)) * scobe
                        else:
                            reactants[-1].update({elem: max(1, int(n)) * scobe})
                        elem, n = k, '0'
                    elif i == 1:
                        if elem in products[-1]:
                            products[-1][elem] += max(1, int(n)) * scobe
                        else:
                            products[-1].update({elem: max(1, int(n)) * scobe})
                        elem, n = k, '0'
                elif k.isalpha():
                    elem += k
                elif k.isdigit():
                    n += k
            if i == 0:
                if elem in reactants[-1]:
                    reactants[-1][elem] += max(1, int(n)) * scobe
                else:
                    reactants[-1].update({elem: max(1, int(n)) * scobe})
            elif i == 1:
                if elem in products[-1]:
                    products[-1][elem] += max(1, int(n)) * scobe
                else:
                    products[-1].update({elem: max(1, int(n)) * scobe})
    return reactants, products


def create_system():  # create system of equation
    system, count = {}, 0
    for i in range(len(elements)):
        for j in range(len(elements[i])):
            for k in elements[i][j]:
                if k in system:
                    if i == 1:
                        system[k] += f'-{chr(ord("a") + count)}*{elements[i][j][k]}'
                    else:
                        system[k] += f'+{chr(ord("a") + count)}*{elements[i][j][k]}'
                else:
                    system[k] = ''
                    for n in range(count):
                        system[k] = f'{chr(ord("a") + n)}*0+'
                    system[k] += f'{chr(ord("a") + count)}*{elements[i][j][k]}'
            for k in system:
                if chr(ord("a") + count) not in system[k]:
                    system[k] += f'+{chr(ord("a") + count)}*0'
            count += 1
    return system


def create_matrix():
    mt = []
    for i in system:
        mt.append([])
        for j in range(len(system[i])):
            if system[i][j].isdigit() and system[i][j - 1] == '*':
                mt[-1].append(int(system[i][j]))
            elif system[i][j].isdigit():
                mt[-1][-1] = mt[-1][-1] * 10 + int(system[i][j])
    return mt


def solve():
    ind, stage, pos = ['' for _ in range(len(equation[0]) + len(equation[1]) - 1)] + [1], 0, []
    for i in range(len(matrix[0]) - 1):
        c = None
        for j in range(len(matrix)):  # create main diagonal
            if matrix[j][stage] and j not in pos:
                p = matrix[j][stage]
                for k in range(len(matrix[j])):
                    matrix[j][k] /= p
                c = matrix[j]
                pos.append(j)
                break
        for j in range(len(matrix)):  # remove zeros below diagonal 1
            if matrix[j][stage] and matrix[j] != c:
                p = (0 - matrix[j][stage]) / c[stage]
                for k in range(len(matrix[j])):
                    matrix[j][k] += c[k] * p
        stage += 1
    for stage in range(len(ind) - 1):
        for i in range(len(matrix)):
            if matrix[i][stage]:
                ind[stage] = matrix[i][-1]
                break
    for i in ind:
        if type(i) == float and round(i, 4) % 1 != 0:
            p = int(1 / round(i % 1, 4))
            for j in range(len(ind)):
                ind[j] *= p
    for i in range(len(ind)):
        if type(ind[i]) == float:
            ind[i] = abs(int(ind[i]))
        if ind[i] == 1 or ind[i] == 0:
            ind[i] = ''
    return ind


def fin_equation():  # create final balanced equation
    balanced_equation, c = '', 0
    for i in range(len(elements)):
        for j in range(len(elements[i])):
            if i == 1 and j == 0:
                balanced_equation += ' = '
            if j != 0:
                balanced_equation += ' + '
            balanced_equation += str(indices[c]) + equation[i][j]
            c += 1
    return balanced_equation


def balancer():  # create balanced equation
    global equation, elements, indices, system, matrix
    ex = ['C + O2 = CO2',
          'H2 + O2 = H2O',
          'P4O10 + H2O = H3PO4',
          'Na3PO4 + MgCl2 = NaCl + Mg3(PO4)2',
          'ZnS + O2 = ZnO + SO2',
          'Fe3O4 + CO = FeO + CO2',
          'PCl5 + H2O = H3PO4 + HCl',
          'CuCO3 + H2SO4 = CuSO4 + H2O + CO2',
          'Al2(SO4)3 + Ca(OH)2 = Al(OH)3 + CaSO4',
          'CH3OH = CH3OCH3 + H2O']
    for eq in ex:
        if ' = ' not in eq and ' + ' not in eq:
            print('Invalid input')
            sys.exit()
        equation = [i.split(' + ') for i in eq.split(' = ')]
        elements = analyze()  # Formatting equation into more convenient form
        system = create_system()  # Create indices using a system of linear equations
        matrix = create_matrix()
        indices = solve()
        result = fin_equation()  # Combine indices with the original equation
        print('-' * 12, eq, result, '-' * 12, sep='\n')


if __name__ == '__main__':
    balancer()
