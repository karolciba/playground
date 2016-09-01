# Sudoku solver
I can't play sudoku (too complicated for me), but I wanted to challenge myself with writing a sudoku solver.

After (highly recommended) watching Berkeley AI lecures was time to implement some solutions.

## Test board
Some "hard" sudoku problem found on the internet.

```
    376
   6   9
  8     4
 9      1
6       9
3      4
7     8
 1   9
  254
```

## Brute solver
Simple to write Depth First Search cheking all combinations was trivial to write but probably won't finish any problem till sun shine. It exponential growing state space (to power of 9!) grows way too fast. 61 nodes each has 9 values.

## Backtraking by filtering
Assign first available, check if doesn't violate any constraints and if not put on the fringe. Will find solution in hours. Better than brute force, but still far from perfect.

## Forward filtering
Each assigment remove inconsitent values in neighbour nodes. Higly depends on the strategy on selecting node to be assiged.

### Selecting first available node to consider
Gives answer after visiting 8 milions of states. On my computer 2 hours.

### Selecting node with fewest possible values
Gives answer after visiting 15 thousands of states in 12 seconds. Hudge improvement

## Arc consitency checking
Like in Forward filtering, but after removing if only one value left assigns it and filters further. With fewest possible values strategy find solution after 540 states in less than 1 second. Impressive.
With less favourable strategy find solution after 22 thousands of states in 1 minute.
