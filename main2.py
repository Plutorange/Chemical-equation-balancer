import sys


def update(group, elem, n, scobe, new_elem=''):  # used in analyze() to shorten the code
    """
    This helper function is used to update the count of an element in the group.

    :param group: A list of dictionaries representing the groups of elements.
    :param elem: The current element being processed.
    :param n: The number of atoms of the current element.
    :param scobe: A multiplier for the number of atoms (for handling nested elements).
    :param new_elem: The new element to be processed next (default is an empty string).
    :return: Updated group with the current element count, the next element to be processed,
     reset count for the next element.
    """
    if elem in group[-1]:
        group[-1][elem] += max(1, int(n)) * scobe
    else:
        group[-1][elem] = max(1, int(n)) * scobe
    return group, new_elem, '0'


def analyze(equation):  # gives reactants and products
    """
    Converts the input equation into a structured format for easier processing by breaking down each
    compound into its constituent elements and their counts.

    :param equation: A list of reactants and products, where each element is a list of strings
     representing chemical compounds.
    :return: A list of two lists (one for reactants and one for products), each containing
     dictionaries with elements as keys and their counts as values.
    """
    elements = [[], []]
    for i in range(len(equation)):
        for j in equation[i]:
            elements[i].append({})
            elem, n, scobe = '', '0', 1
            for k in j:
                if k == '(':
                    elements[i], elem, n = update(elements[i], elem, n, scobe)
                    scobe = int(j[j.find(')') + 1:])
                elif k == ')':
                    break
                elif k.isalpha() and k == k.capitalize():
                    if elem == '':
                        elem = k
                    else:
                        elements[i], elem, n = update(elements[i], elem, n, scobe, k)
                elif k.isalpha():
                    elem += k
                elif k.isdigit():
                    n += k
            elements[i], elem, n = update(elements[i], elem, n, scobe)
    return elements


def create_system(elements):  # create system of equation
    """
    Creates a system of linear equations from the parsed elements to represent the conservation of
    each element.

    :param elements: A list of lists containing dictionaries of elements and their counts.
    :return: A dictionary where each key is an element and the value is a string representing the
     linear equation for that element.
    """
    system, count = {}, 0
    for i in range(len(elements)):
        for j in range(len(elements[i])):
            for k in elements[i][j]:
                if k in system:
                    system[k] += \
                        f'{chr(ord("+") + 2 * i)}{chr(ord("a") + count)}*{elements[i][j][k]}'
                else:
                    system[k] = f'a*0+' * bool(count)
                    for q in range(1, count):
                        system[k] += f'{chr(ord("a") + q)}*0+'
                    system[k] += f'{chr(ord("a") + count)}*{elements[i][j][k]}'
            for k in system:
                if chr(ord("a") + count) not in system[k]:
                    system[k] += f'+{chr(ord("a") + count)}*0'
            count += 1
    return system


def create_matrix(system):
    """
    Converts the system of linear equations into a matrix representation suitable for solving.

    :param system: A dictionary representing the system of linear equations.
    :return: A matrix where each inner list represents the coefficients of a linear equation.
    """
    mt = []
    for i in system:
        mt.append([])
        for j in range(len(system[i])):
            if system[i][j].isdigit() and system[i][j - 1] == '*':
                mt[-1].append(int(system[i][j]))
            elif system[i][j].isdigit():
                mt[-1][-1] = mt[-1][-1] * 10 + int(system[i][j])
    return mt


def solve(matrix):
    """
    Solves the matrix of linear equations to find the coefficients that balance the chemical
    equation.

    :param matrix: A matrix representing the system of linear equations.
    :return: A list of coefficients for the reactants and products in the balanced equation.
    """
    ind, pos, c = ['' for _ in range(len(matrix[0]) - 1)] + [1], [], 0
    for i in range(len(matrix[0]) - 1):
        for j in range(len(matrix)):  # create main diagonal
            if matrix[j][i] and j not in pos:
                p = matrix[j][i]
                for k in range(len(matrix[j])):
                    matrix[j][k] /= p
                c = matrix[j]
                pos.append(j)
                break
        for j in range(len(matrix)):  # remove zeros below diagonal 1
            if matrix[j][i] and matrix[j] != c:
                p = (0 - matrix[j][i]) / c[i]
                for k in range(len(matrix[j])):
                    matrix[j][k] += c[k] * p
    for i in range(len(ind) - 1):
        for j in range(len(matrix)):
            if matrix[j][i]:
                ind[i] = matrix[j][-1]
                break
    for i in ind:
        if round(i, 4) % 1 != 0:
            p = float(1 / (i % 1))
            for j in range(len(ind)):
                ind[j] *= p
    for i in range(len(ind)):
        if type(ind[i]) == float:
            ind[i] = abs(int(ind[i]))
        if ind[i] == 1 or ind[i] == 0:
            ind[i] = ''
    return ind


def fin_equation(equation, elements, indices):  # create final balanced equation
    """
    Constructs the final balanced chemical equation using the original equation and the calculated
    coefficients.

    :param equation: The original input equation as a list of lists of strings.
    :param elements: The parsed elements and their counts.
    :param indices: The list of coefficients.
    :return: A string representing the balanced chemical equation.
    """
    balanced_equation, c = '', 0
    for i in range(len(elements)):
        for j in range(len(elements[i])):
            if i == 1 and j == 0:
                balanced_equation += ' = '
            elif j != 0:
                balanced_equation += ' + '
            balanced_equation += str(indices[c]) + equation[i][j]
            c += 1
    return balanced_equation


def balancer():  # create balanced equation
    """
    Main function to interact with the user, process the input, and produce the balanced equation.

    Prompts the user for input.
    Validates the input format.
    Analyzes the input equation.
    Creates the system of linear equations.
    Creates the matrix.
    Solves the matrix.
    Prints the balanced equation.

    :return:
    """
    print('''How to write chemical equation:

Only the first letter of the element should be capitalized:
He, Li, Be, Ne, Na, Mg

You do not need to write coefficients.
You must write the subscript as a regular number (without parentheses) to the right of the element:
H2, O2, CO2

Also, "+", "-" and "=" should be isolated with one space from each side.

Example:
Na3PO4 + MgCl2 = NaCl + Mg3(PO4)2
''')
    eq = input('Now please enter the equation:\n')
    if ' = ' not in eq and ' + ' not in eq:
        print('Invalid input')
        sys.exit()
    equation = [i.split(' + ') for i in eq.split(' = ')]
    elements = analyze(equation)  # Formatting equation into more convenient form
    system = create_system(elements)  # Create system of linear equations
    matrix = create_matrix(system)  # Create matrix from system of linear equations
    indices = solve(matrix)  # Get indices by solving the matrix
    result = fin_equation(equation, elements, indices)  # Combine indices with the original equation
    print(result)


if __name__ == '__main__':
    balancer()
