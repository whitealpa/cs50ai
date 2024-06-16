import sys

from crossword import *
from collections import OrderedDict


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = OrderedDict(
            (var, self.crossword.words.copy())
            for var in self.crossword.variables
        )

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        
        return self.backtrack(dict())
    
    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for word_list in self.domains:
            inconsistent_words = self.find_inconsistent_words(word_list)
            for word in inconsistent_words:
                self.domains[word_list].remove(word)
                
    def find_inconsistent_words(self, word_list):
        inconsistent_words = set()
        for word in self.domains[word_list]:
            if len(word) != word_list.length:
                inconsistent_words.add(word)
        return inconsistent_words
        
    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
  
        if self.crossword.overlaps[x, y]:
            x_index, y_index = self.crossword.overlaps[x, y]
            
            y_overlap_letter = set()
            for word in self.domains[y]:
                y_overlap_letter.add(word[y_index])
                
            inconsistent_x_list = set()
            for word in self.domains[x]:
                if word[x_index] not in y_overlap_letter:
                    inconsistent_x_list.add(word)

            if inconsistent_x_list:
                self.domains[x] = {word for word in self.domains[x]
                                   if word not in inconsistent_x_list}
                return True
            
        return False
    
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
              
        if arcs is None:
            arcs = [arc for arc in self.domains]

        queue = []
        for x in arcs:
            for y in arcs:
                if x != y:
                    queue.append((x, y))
        
            while queue:
                x, y = queue.pop()
                if self.revise(x, y):
                    if len(self.domains[x]) == 0:
                        return False
                    for x_neigbor in self.crossword.neighbors(x) - {y}:
                        queue.append((x_neigbor, x))
        
        return True
        
    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.domains:
            if variable not in assignment:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        word_list = []
        for variable, word in assignment.items():
            if variable.length != len(word) or word in word_list:
                return False
            word_list.append(word)
            
            neighbours = self.crossword.neighbors(variable)
            for neighbor in neighbours:
                x_index, y_index = self.crossword.overlaps[variable, neighbor]
                if neighbor in assignment:
                    if word[x_index] != assignment[neighbor][y_index]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        values = {}
        for variable in self.domains[var]:
            neighbor_count = 0
            for neighbor in self.crossword.neighbors(var):
                if variable in self.domains[neighbor]:
                    neighbor_count += 1
            values[variable] = neighbor_count     
        return sorted(values, key=lambda key: values[key])

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_variables = set(self.domains.keys()) - set(assignment.keys())
        result = [variable for variable in unassigned_variables]
        result.sort(key=lambda x: (len(self.domains[x]), len(self.crossword.neighbors(x))))
        return result[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        variable = self.select_unassigned_variable(assignment)
        
        for word in self.order_domain_values(variable, assignment):
            assignment[variable] = word
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result:
                    return result
            assignment.pop(variable)
        
        return None     
    
        
def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
