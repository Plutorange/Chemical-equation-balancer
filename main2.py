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


def solve():
    system = ['']
    count = 0
    for i in range(len(elements)):
        for j in range(len(elements[i])):
            for k in elements[i][j]:
                c = 0
                for q in range(len(system)):
                    if k in system[q]:
                        if i == 1 and '=' not in system[q]:
                            system[q] += f'=={chr(ord("a") + count)}*{elements[i][j][k]}'
                        else:
                            system[q] += f'+{chr(ord("a") + count)}*{elements[i][j][k]}'
                        c = 1
                if c == 0:
                    system.append(f'{k} {chr(ord("a") + count)}*{elements[i][j][k]}')
            count += 1
    system = [i.split(' ')[1] for i in system[1:]]
    for a in range(1, 12):
        for b in range(1, 12):
            for c in range(1, bool(count // 3) * 10 + 2):
                for d in range(1, bool(count // 4) * 10 + 2):
                    for e in range(1, bool(count // 5) * 10 + 2):
                        for f in range(1, bool(count // 6) * 10 + 2):
                            for g in range(1, bool(count // 7) * 10 + 2):
                                for h in range(1, bool(count // 8) * 10 + 2):
                                    n = 0
                                    for i in system:
                                        if eval(i):
                                            n += 1
                                    if n == len(system):
                                        return [a, b, c, d, e, f, g, h]


def fin_equation():  # create final balanced equation
    balanced_equation = ''
    c = 0
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
    global equation, indices, reactants, products, elements
    print('How to write chemical equation:')
    print()
    print('Only the first letter of the element should be capitalized:')
    print('He, Li, Be, Ne, Na, Mg')
    print()
    print('Template:')
    print('(reactant 1) + (reactant 2) + ... + (reactant n)'
          ' = (product 1) + (product 2) + ... + (product n)')
    print()
    print('Example:')
    print('Na3PO4 + MgCl2 = NaCl + Mg3(PO4)2')
    print()
    eq = input('Now please enter the equation:\n')
    equation = eq.split(' = ')
    equation = [i.split(' + ') for i in equation]
    reactants, products = [], []
    analyze()
    elements = reactants, products
    indices = solve()
    for i in range(len(indices)):
        if indices[i] == 1:
            indices[i] = ''
    result = fin_equation()
    print(result)


if __name__ == '__main__':
    balancer()
