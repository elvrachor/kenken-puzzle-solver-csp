import sys
import copy
import time

from csp import *

# search options available that should be given as command line arguments
heuristics = {'FUVAR': first_unassigned_variable, 'MRV': mrv,
              'UDV': unordered_domain_values, 'LCV':lcv,
              'NOINF': no_inference, 'FC': forward_checking, 'MAC': mac}

class KenKen(CSP):
    """KenKen implemented as a CSP problem"""
    
    def __init__(self, puzzle):
        """Initializes a KenKen puzzle as a CSP problem"""

        # parse grid size
        gridSize = int(puzzle[0])
        puzzle.remove(puzzle[0])

        # map cell numbers to variable i, j
        self.grid_map = self.make_grid_map(gridSize)

        variables = [] # initialize problem variables
        for i in range(0, gridSize):
            for j in range(0, gridSize):
                variable = "X" + str(i) + str(j)
                variables.append(variable)

        domains = {} # initialize problem variable domains
        for variable in variables:
            domains[variable] = set(range(1, gridSize + 1))

        neighbors = {varij: [] for varij in variables}

        # all variables in each row and column should have different values
        for i in range(0, gridSize):
            x = [] # variables in row
            y = [] # variables in column
            for j in range(0, gridSize):
                varij = "X" + str(i) + str(j)
                varji = "X" + str(j) + str(i)
                x.append(varij)
                y.append(varji)

            for varij in x:
                l = copy.deepcopy(x)
                l.remove(varij)
                neighbors[varij] += l

            for varji in y:
                l = copy.deepcopy(y)
                l.remove(varji)
                neighbors[varji] += l

        # split each cage into cage variables, value and operator
        cages = [] # vatiables in all cages
        for _, cage in enumerate(puzzle):
            c = [] # variables in cage
            cage = cage.split('#')
            cageValue = int(cage[0])
            cageVariables = cage[1].split('-')

            for k in cageVariables:
                i, j = self.grid_map[int(k)]
                varij = "X" + str(i) + str(j)
                c.append(varij)
            
            cageOperator = cage[2]

            for varij in c:
                l = copy.deepcopy(c)
                l.remove(varij)
                neighbors[varij] += l
                s = set(neighbors[varij])
                neighbors[varij] = list(s)

            cages.append([tuple(c), cageOperator, cageValue])

        self.gridSize = gridSize

        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors

        self.cages = cages
        self.puzzle = puzzle

        self.nchecks = 0 # number of times checked if constraints are satisfied

        super().__init__(None, domains, neighbors, self.constraints)


    def constraints(self, A, a, B, b):
        """Constraint function for KenKen CSP problem
        (refer to CSP.constraints for more information)"""

        self.nchecks += 1

        def get_cage(var):
            """Return cage of given variable"""

            for cage in self.cages:
                if var in cage[0]:
                    return cage

        def is_in_same_row_or_column():
            """Return true if A and B are in the same row or column"""

            ai, aj = int(A[1]), int(A[2])
            bi, bj = int(B[1]), int(B[2])

            return (ai == bi) or (aj == bj)

        def is_in_same_cage():
            """Return true if A and B are in the same cage"""
            
            return cageA == cageB

        def same_row_or_column_constraints():
            """Return true if a and b are legal values for A and B respectively"""
            
            return a != b

        def sum_constraint():
            """Return false if all cage variables are assigned and the sum of their
            values is not equal to cage value"""

            result = a + b
            for var in cageVariables:
                if var != A and var != B and var not in assignmentKeys:
                    return True
                if var != A and var != B:
                    result += assignment[var]

            return result == cageValue

        def difference_constraint():
            """Return false if all cage variables are assigned and the difference of their
            values is not equal to cage value"""

            values = [a, b]

            for var in cageVariables:
                if var != A and var != B and var not in assignmentKeys:
                    return True
                if var != A and var != B:
                    values.append(assignment[var])

            return abs(a - b) == cageValue

        def product_constraint():
            """Return false if all cage variables are assigned and the product of their
            values is not equal to cage value"""

            result = a * b
            for var in cageVariables:
                if var != A and var != B and var not in assignmentKeys:
                    return True
                if var != A and var != B:
                    result *= assignment[var]

            return result == cageValue

        def quotient_constraint():
            """Return false if all cage variables are assigned and the quotient of their
            values is not equal to cage value"""

            values = [a, b]
            for var in cageVariables:
                if var != A and var != B and var not in assignmentKeys:
                    return True
                if var != A and var != B:
                    values.append(assignment[var])

            return (max(a, b) / min(a, b)) == cageValue

        def equal_constraint(val):
            """Return true if the given value is equal to cage value"""

            return val == cageValue
        
        def same_cage_constraints():
            """Return true if cage variables satisfy the cage constraints"""

            if operator == '+':
                return sum_constraint()
            elif operator == '-':
                return difference_constraint()
            elif operator == '*':
                return product_constraint()
            elif operator == '/':
                return quotient_constraint()

        # get cages of variables A and B
        cageA = get_cage(A)
        cageB = get_cage(B)
        assignment = self.infer_assignment()

        # if A and B are in different cages, since they are neighbours,
        # either one of them is in a cage with operator '=' 
        # or they are only in the same row or column
        if not is_in_same_cage():
            operatorA = cageA[len(cageA) - 2]
            operatorB = cageB[len(cageB) - 2]

            if operatorA == '=':
                cageValue = cageA[len(cageA) - 1]
                return same_row_or_column_constraints() and equal_constraint(a)
            if operatorB == '=':
                cageValue = cageB[len(cageB) - 1]
                return same_row_or_column_constraints() and equal_constraint(b)

            return same_row_or_column_constraints()

        # else both of them are in the same cage
        cage = cageA

        cageVariables = cage[0]
        operator = cage[len(cage) - 2]
        cageValue = cage[len(cage) - 1]
        assignmentKeys = list(assignment.keys())

        # if A and B are in the same cage, but not in the same column
        if not is_in_same_row_or_column():
            return same_cage_constraints()

        # else, both constraints should be satisfied
        return same_cage_constraints() and same_row_or_column_constraints()

    def display(self, assignment):
        """Show the assignment of the variables in a more readable form (in a grid)"""

        assignmentKeys = list(assignment.keys())

        for i in range(0, self.gridSize):
            output = str()
            for j in range(0, self.gridSize):
                varij = "X" + str(i) + str(j)
                if varij in assignmentKeys:
                    output += str(assignment[varij]) + " "
                else:
                    output += "   "
            print(output)

    def make_grid_map(self, gridSize):
        """Return a dictionary that maps a cell number to a tuple (i, j) in grid
        (helpful for parsing puzzle from file in init())"""

        map = {}
        cell_no = 0
        for i in range(0, gridSize):
            for j in range(0, gridSize):
                map[cell_no] = (i, j)
                cell_no += 1

        return map


if __name__ == '__main__':
    n = len(sys.argv)

    if n != 3 and n != 6:
        print("Usage: python3 kenken.py <file.puzzle> MC")
        print("or     python3 kenken.py <file.puzzle> BT <variable_ordering> <value_ordering> <inference>")
        print("Argument options :")
        print("variable_ordering: FUVAR, MRV")
        print("value ordering   : UDV, LCV")
        print("inference        : NOINF, FC, MAC")
        exit()
    
    file = open(sys.argv[1])
    data = file.read()
    puzzle = data.splitlines()

    kenken = KenKen(puzzle)

    # options given from command line
    solve = sys.argv[2]
    if solve == "BT":
        variable_ordering = heuristics[sys.argv[3]]
        value_ordering = heuristics[sys.argv[4]]
        inference = heuristics[sys.argv[5]]

        # count search time
        start = time.time()
        search_result = backtracking_search(kenken, variable_ordering, value_ordering, inference)
        end = time.time()

        # print result
        print("Solution:")
        kenken.display(kenken.infer_assignment())

    elif solve == "MC":
        # count search time
        start = time.time()
        search_result = min_conflicts(kenken)
        end = time.time()

        # print result
        print("Best result from hill climbing:")
        kenken.display(kenken.current)

    else:
        print("Error: wrong arguments given")

    # print statistics
    dt = end - start
    print("Search time: ", dt, "s")
    print("Nodes      : ", kenken.nassigns)
    print("Checks     : ", kenken.nchecks)