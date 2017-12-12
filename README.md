# sudoku 数独

**Objective**

Fill a 9x9 grid with digits

**Rules**
1. Each row contains the numbers 1 to 9
2. Each column contains the numbers 1 to 9
3. Each box contains the numbers 1 to 9

## Binary Constraint Satisfaction Problem

### Variables

Variable for each tile in the sudoku grid with a total of 81 variables. Variable is a combination of a letter indicating the row, and a digit indicating the column. 

X = {X<sub>1</sub>, X<sub>2</sub>, ..., X<sub>81</sub>}

### Domains

Each variable X<sub>i</sub> has the domain of the digits [1,9]

D = {D<sub>1</sub>, D<sub>2</sub>, ..., D<sub>81</sub>}

D<sub>i</sub> = {1, 2, 3, 4, 5, 6, 7, 8, 9}

### Constraints

The value of each variable X<sub>i</sub> cannot be equal to any value in its:
- Row
- Column
- Box

