import copy
import string

grid = [['-', '-', '-', '-', 'Y'],
        ['R', 'A', '-', '-', '-'],
        ['-', '-', '-', '-', '-'],
        ['-', 'E', '-', '-', '-'],
        ['-', '-', '-', '-', 'K']]

alphabet = list(string.ascii_uppercase)[:-1]


def getNextStates(cell):
    """
    Return all the vertical and horizontal neighbors of given cell
    """
    neighbours = []
    if cell[0] > 0:
        neighbours.append((cell[0] - 1, cell[1]))
    if cell[1] > 0:
        neighbours.append((cell[0], cell[1] - 1))
    if cell[0] < 4:
        neighbours.append((cell[0] + 1, cell[1]))
    if cell[1] < 4:
        neighbours.append((cell[0], cell[1] + 1))
    return neighbours


def getLetters(letter):
    """
    Returns a list of all letters that can be assigned to the cell at the given index
    """
    index = alphabet.index(letter)
    nextLetters = []
    if index > 0:
        nextLetters.append(alphabet[index - 1])
    if index < 24:
        nextLetters.append(alphabet[index + 1])
    return nextLetters


def getOutput(result):
    """
        Prints the modified grid row by row.
    """
    for cell, value in result.items():
        grid[cell[0]][cell[1]] = value
    for row in grid:
        print(row)


class startCSP:
    def __init__(self, variables, domains, alphabets, visited):
        self.variables = variables
        self.domains = domains
        self.alphabets = alphabets
        self.visited = visited

    # Assigns the given value to the cell at the given coordinates and updates the domains of all neighboring cells.
    def addValue(self, value, letter):
        self.domains[value][0] = [letter]
        self.visited.append(value)
        for cell in self.variables:
            if cell not in self.visited and letter in self.domains[cell][0]:
                self.domains[cell][0].remove(letter)
        for neighbor in self.domains[value][1]:
            self.domains[neighbor][2].append(letter)

    def startSearch(self, assignment={}):
        """
            Perform a backtracking search to find a valid solution for the puzzle.
        """
        if len(assignment) == len(self.variables):
            return assignment

        cell = self.getMRV()
        orderedDomain = self.getLCV(cell)

        for letter in orderedDomain:
            if self.checkConsistency(cell, letter):
                newDomain = copy.deepcopy(self.domains)
                assign = assignment.copy()

                # Assigning the letter to the cell
                assign[cell] = letter
                self.addValue(cell, letter)

                if self.backcheck(cell):
                    result = self.startSearch(assign)
                    if result is not None:
                        return result
                self.domains = newDomain
                self.visited.remove(cell)

        return None

    def backcheck(self, selected):
        for value in self.domains[selected][1]:
            if len(self.domains[value][1]) > len(self.domains[value][2]):
                continue
            # All value are filled
            elif len(self.domains[value][1]) == len(self.domains[value][2]):
                required = []
                for c in self.domains[value][2]:
                    required += getLetters(c)
                self.domains[value][0] = [
                    i for i in self.domains[value][0] if i in required]
                if len(self.domains[value][0]) == 0:
                    return False
                else:
                    continue
        return True

    def checkConsistency(self, selected, letter):
        if len(self.domains[selected][1]) > len(self.domains[selected][2]):
            return True
        for c in self.domains[selected][2]:
            # if letter satisfied constraint
            if letter in getLetters(c):
                return True
        return False

    def getMRV(self):
        # get MRV
        mcv = [(i, j[2])
               for i, j in self.domains.items() if i not in self.visited]

        mcv.sort(key=lambda elem: len(elem[1]), reverse=True)
        return mcv[0][0]

    def getLCV(self, cell):
        values = []
        constraints = []
        for c in self.domains[cell][2]:
            constraints += getLetters(c)
        for letter in self.domains[cell][0]:
            consistent = 0
            for c in self.domains[cell][2]:
                if letter in getLetters(c):
                    consistent += 1
            values.append((letter, consistent))
        values.sort(key=lambda k: k[1], reverse=True)
        return [i[0] for i in values]


def main():
    closedStates = []
    constraints = {}
    alphabets = list(string.ascii_uppercase)[:-1]  # the letters
    variables = []
    allCells = []
    domains = {}  # domains of each cell

    for i, row in enumerate(grid):
        for j in range(5):
            if row[j] != '-':
                alphabets.remove(row[j])
                constraints[(i, j)] = row[j]
                closedStates.append((i, j))
            else:
                variables.append((i, j))
            allCells.append((i, j))

    for cells in allCells:
        next_states = getNextStates(cells)
        constraintList = []
        for states in next_states:
            if states in constraints:
                constraintList.append(constraints[states])
        if cells in constraints:
            domains[cells] = [[constraints[cells]], next_states, constraintList]
        else:
            domains[cells] = [[i for i in alphabets], next_states, constraintList]
    cspResult = startCSP(variables, domains, alphabets, closedStates)

    result = cspResult.startSearch()

    if result is None:
        print("No Solutions")
    else:
        getOutput(result)


if __name__ == '__main__':
    main()