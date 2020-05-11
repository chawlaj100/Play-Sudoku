from sudoku_utils import *
def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """
    rows = 'ABCDEFGHI'
    cols = '123456789'
    dict1 = {}
    list1 = cross(rows, cols)
    for i in range(len(list1)):
        dict1[list1[i]] = grid[i]
    return dict1

# def updated_grid_values(grid):
#     """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

#     Args:
#         grid: Sudoku grid in string form, 81 characters long
#     Returns:
#         Sudoku grid in dictionary form:
#         - keys: Box labels, e.g. 'A1'
#         - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
#     """
#     rows = 'ABCDEFGHI'
#     cols = '123456789'
#     dict = {}
#     for i in range(len(grid)):
#         if(grid[i]=='.'):
#             dict[boxes[i]] = cols
#         else:
#             dict[boxes[i]] = grid[i]
#     return dict

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    rows = 'ABCDEFGHI'
    cols = '123456789'
    rows_grp = ['ABC', 'DEF', 'GHI']
    cols_grp = ['123', '456', '789']
    for i in values:
        if len(values[i]) == 1:
            index = i
            b,c = index[0],index[1]
            for j in index:
                if j in rows:
                    for k in cols:
                        a = j+k
                        if a == index:
                            pass
                        else:
                            if values[index] in values[a]:
                                temp = ''
                                for z in values[a]:
                                    if z == values[index]:
                                        temp = temp
                                    else:
                                        temp = temp + z
                                values[a] = temp
                            else:
                                pass
                else:
                    for l in rows:
                        a = l+j
                        if a == index:
                            pass
                        else:
                            if values[index] in values[a]:
                                temp = ''
                                for z in values[a]:
                                    if z == values[index]:
                                        temp = temp
                                    else:
                                        temp = temp + z
                                values[a] = temp
                            else:
                                pass
            for abc in rows_grp:
                if b in abc:
                    inter1 = abc
            for abc in cols_grp:
                if c in abc:
                    inter2 = abc
            list_inter = cross(inter1, inter2)
            for y in list_inter:
                if y == index:
                    pass
                else:
                    if values[index] in values[y]:
                        temp = ''
                        for z in values[y]:
                            if z == values[index]:
                                temp = temp
                            else:
                                temp = temp + z
                        values[y] = temp
                    else:
                        pass   
        else:
            pass
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    # TODO: Implement only choice strategy here
    #units = [cross(abc,xyz) for abc in ('ABC', 'DEF', 'GHI') for xyz in ('123','456','789')]
    for i in unitlist:
        subset = i
        for j in subset:
            if len(values[j]) == 1:
                pass
            else:
                inter = values[j]
                flag = {}
                for i in inter:
                    flag[i] = 0
                for l in inter:
                    for k in subset:
                        if k==j:
                            pass
                        else:
                            if l in values[k]:
                                flag[l] = 1
                                break
                            else:
                                pass
                    if flag[l] == 0:
                        values[j] = l
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers
    """
    out = values.copy()
    for i in out:
        if len(out[i])>=2:
            peer = peers[i]
            for j in peer:
                if len(out[i])==2 and out[i]==out[j]:
                    inter = out[i]
                    a,b = inter[0],inter[1]
                    peer1 = peers[i]
                    peer2 = peers[j]
                    for x in peer1:
                        if x in peer2:
                            temp=''
                            if a in out[x]:
                                for y in out[x]:
                                    if a==y:
                                        temp = temp
                                    else:
                                        temp = temp + y
                                out[x]=temp
                            temp=''
                            if b in out[x]:
                                for z in out[x]:
                                    if b==z:
                                        temp = temp
                                    else:
                                        temp = temp + z
                                out[x]=temp
                        else: 
                            pass
                        
                else:
                    pass
        else:
            pass
    return out

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the naked_twins to remove them from peers
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values): # When sudoku is hard and it doesn't change the values when we use reduce_puzzle even after many iterations
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[a])==1 for a in boxes):
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    _,y = min((len(values[a]), a) for a in boxes if len(values[a]) > 1)
                
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for temp in values[y]:
        new_sudoku = values.copy()
        new_sudoku[y] = temp
        solved = search(new_sudoku)
        if solved:
            return solved

string = '.2.6.8...58...97......4....37....5..6.......4..8....13....2......98...36...3.6.9.'
string2 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
string3 = '.2..4...7..1.2.......8...657.4...58.6..4.........3....5.89..4.....6.7.......5..3.'
values = grid_values(string)
print(input("Press Enter to view the Sudoku"))
#print("Solve this sudoku")
display(values)
print("\nDone")
values = updated_grid_values(string)
values = search(values)
print(input("\nPress Enter to get the result"))
display(values)
#print("Sudoku Solved")