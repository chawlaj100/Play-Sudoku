# Play-Sudoku
The sudoku is solved by an agent using Constraint Propagation
Here the sudoku is solved by applying various constraints like
1. Elimination (We eliminate the numbers form peers of all the fixed boxes)
2. Only_choice (Here in each unit, if we have a number that can belong to only ne box then it is assigned to that box)
3. Reduce_Puzzle (It checks and iteratively runs the above 2 algorithms and looks for changes)
3. Searching for the best solution using DFS in case of tough sudoku.

You can use the sudoku_test for seeing the algorithms used for solving the sudoku.
sudoku_utils consists of the variables used in the whole project.
