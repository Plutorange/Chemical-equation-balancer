from functools import reduce


def analyze():  # gives reactants and products
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
                        reactants[-1].update({elem: max(1, int(n)) * scobe})
                        elem, n = k, '0'
                    elif i == 1:
                        products[-1].update({elem: max(1, int(n)) * scobe})
                        elem, n = k, '0'
                elif k.isalpha():
                    elem += k
                elif k.isdigit():
                    n += k
            if i == 0:
                reactants[-1].update({elem: max(1, int(n)) * scobe})
            elif i == 1:
                products[-1].update({elem: max(1, int(n)) * scobe})


def solve(r, p):
    indices = [[[] for _ in range(len(reactants))]] + [[[] for _ in range(len(products))]]
    for _ in range(4):
        for n1, i1 in enumerate(r):
            for j1 in i1:
                for n2, i2 in enumerate(p):
                    for j2 in i2:
                        if j1 == j2 and i1[j1] != i2[j2]:
                            if max(i1[j1], i2[j2]) % min(i1[j1], i2[j2]) == 0:
                                if i1[j1] < i2[j2]:
                                    mult = i2[j2] // i1[j1]
                                    indices[0][n1].append(mult)
                                    for k1 in i1:
                                        i1.update({k1: i1[k1] * mult})
                                else:
                                    mult = i1[j1] // i2[j2]
                                    indices[1][n2].append(mult)
                                    for k2 in i2:
                                        i2.update({k2: mult * i2[k2]})
    return indices


def organize_ind():
    for i in range(len(ind)):
        for j in range(len(ind[i])):
            if not ind[i][j]:
                ind[i][j] = ''
            else:
                ind[i][j] = reduce(lambda x, y: x * y, ind[i][j])


def fin_equation():
    balanced_equation = ''
    for i in range(len(equation)):
        for j in range(len(equation[i])):
            if i == 1 and j == 0:
                balanced_equation += ' = '
            if j != 0:
                balanced_equation += ' + '
            balanced_equation += str(ind[i][j]) + equation[i][j]
    return balanced_equation


def balancer():
    global equation, reactants, products, ind
    ex = ['C + O2 = CO2',  # YES
          'H2 + O2 = H2O',  # YES
          'P4O10 + H2O = H3PO4',  # YES
          'Na3PO4 + MgCl2 = NaCl + Mg3(PO4)2',  # YES
          'ZnS + O2 = ZnO + SO2',  # NO
          'Fe3O4 + CO = FeO + CO2'  # NO
          ]
    for eq in ex:
        equation = eq.split(' = ')
        equation = [i.split(' + ') for i in equation]
        reactants, products = [], []
        analyze()
        ind = solve(reactants, products)
        organize_ind()
        result = fin_equation()
        print('-' * 12, eq, result, '-' * 12, sep='\n')


if __name__ == '__main__':
    balancer()
