# KenKen Puzzle Solver CSP

Part of assignment for the **Artificial Intelligence I** course (Winter Semester 2022-2023).

The [KenKen Puzzle](https://en.wikipedia.org/wiki/KenKen) is an arithmetic and logic puzzle. Each puzzle has the form of a square grid divided in cages, which are disjoint sets of cells and have a specific target and operator. The goal is to find the values of the cells, so that the result of the operation between each cage's cells is equal to its target, with the constraint that each value should appear only once in each row and column.

## Project structure

```txt
kenken-puzzle-solver-csp/
├── test_cases/  # puzzles and solutions
│
├── kenken.py    # source code for KenKen solver
├── csp.py       # files from AIMA python
├── search.py
├── utils.py
│
├── LICENCE      # MIT licence
└── README.md    # this documentation file
```

## Details about test files

Two files are associated with each test in `test_cases/`; the puzzle file and its solution with `.puzzle` and `.solution` extensions respectively.

The name of each test specifies:
+ the level of difficulty (easiest, easy, medium, hard).
+ the grid size (ranging from 3 to 9).
+ the special number of each puzzle (puzzle #), provided by this [site](https://www.kenkenpuzzle.com/).

e.g. `easy-4-151945.puzzle`
<br></br>

The first line of each `.puzzle` file contains the grid size.

The rest of the file contains information about the cages of the puzzle in the following form:

    <target>#<cells in cage divided with dash>#operator

e.g. `9#24-25#+`
<br></br>

The `.solution` files contain the values of each cell.

## Execution

To execute the program using a backtracking algorithm, run the following command in the `kenken-puzzle-solver-csp/` directory:

    python3 kenken.py <file.puzzle> BT <variable_ordering> <value_ordering> <inference>

where:

- `file.puzzle`: relative path to a `.puzzle` in `test_cases/`

- `variable_ordering`: the first unassigned variable (`FUVAR` option) or LCV (`LCV` option)

- `inference`: no inference (`NOINF` option) or FC (`FC` option) or MAC (`MAC` option)
<br></br>

To execute the program using the local search Min Conflicts algorithm, run the following comamnd in the `kenken-puzzle-solver-csp/` directory:

    python3 kenken.py <file.puzzle> MC

where:

- `file.puzzle`: relative path to a `.puzzle` in `test_cases/`
<br></br>