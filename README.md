# Play-Sudoku
### The Sudoku is solved by an algorithm using Constraint Propagation.
#### These are the various modules made to solve the sudoku with any difficulty levels.
1. Elimination (We eliminate the numbers form peers of all the fixed boxes)
2. Only_choice (Here in each unit, if we have a number that can belong to only one box then it is assigned to that box)
3. Reduce_Puzzle (It checks and iteratively runs the above 2 algorithms and looks for changes)
3. Searching for the best solution using DFS in case of more difficult sudoku.

- You can use the sudoku_test for seeing the algorithms used for solving the sudoku.
- The sudoku_utils.py consists of the variables used in the algorithm.
#### The input sudoku can be provided in the file sudoku_test.py in the form of a string, with numbers and a "." (dot) in place of an empty slot.
