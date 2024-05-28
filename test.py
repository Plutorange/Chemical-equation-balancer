import sys

import main2


def balancer():  # create balanced equation
    ex = ['C + O2 = CO2',
          'H2 + O2 = H2O',
          'P4O10 + H2O = H3PO4',
          'Na3PO4 + MgCl2 = NaCl + Mg3(PO4)2',
          'ZnS + O2 = ZnO + SO2',
          'Fe3O4 + CO = FeO + CO2',
          'PCl5 + H2O = H3PO4 + HCl',
          'CuCO3 + H2SO4 = CuSO4 + H2O + CO2',
          'Al2(SO4)3 + Ca(OH)2 = Al(OH)3 + CaSO4',
          'CH3OH = CH3OCH3 + H2O',
          'Fe2O3 + C = Fe + CO2',
          'NH3 + O2 = H2O + NO',
          'K4Fe(SCN)6 + K2Cr2O7 + H2SO4 = Fe2(SO4)3 + Cr2(SO4)3 + CO2 + H2O + K2SO4 + KNO3',
          'Al + KOH + H2SO4 = H2 + KAl(SO4)2 + H2O']
    for eq in ex:
        if ' = ' not in eq and ' + ' not in eq:
            print('Invalid input')
            sys.exit()
        equation = [i.split(' + ') for i in eq.split(' = ')]
        elements = main2.analyze(equation)  # Formatting equation into more convenient form
        system = main2.create_system(elements)  # Create system of linear equations
        matrix = main2.create_matrix(system)  # Create matrix from system of linear equations
        indices = main2.solve(matrix)  # Get indices by solving the matrix
        result = main2.fin_equation(equation, elements,
                                    indices)  # Combine indices with the original equation
        print('-' * 12, eq, result, '-' * 12, sep='\n')


if __name__ == '__main__':
    balancer()
