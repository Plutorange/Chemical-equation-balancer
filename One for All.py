import equation_solver
import main2
import sys
import test2

if __name__ == '__main__':
    print('''Welcome to our program.
We offer several options:
1. We can solve your polynomial equation;
2. We can balance your chemical equation;
3. We can provide you with several examples of how we balance chemical equations.\n''')
    while True:
        action = input('Enter the number of the action you want to do (1/2/3/quit): ')
        print()
        if action == '1':
            equation_solver.solve_equation()
            sys.exit()
        elif action == '2':
            main2.balancer()
            sys.exit()
        elif action == '3':
            test2.balancer()
            sys.exit()
        elif action == 'quit':
            print('Bye, have a nice day!')
            sys.exit()
        else:
            print('Please read instructions carefully and try again.')
