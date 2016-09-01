# playground
Playground on various subjects.

## sudoku

I can't play sudoku, but can I write program that can play sudoku?

Current solvers are:
- brute solver, which probably won't find solution till sun shines
- naive filtering (check is state is consistent before processing), which should be better
- forward filtering - remove unconsistent values in neighour nodes - blazingly fast
  (simple problem in 300 tries, hard in tens of thousands)
- arc consistency checking

Further notes in subdirectory [sudoku](sudoku/README.md)

## eucliderer
Graphics renderer capable of drawing geometry primitives: dots, lines, boxes, curves.
First implementation is to be 2D.

Visualization tool needed for other projects.

## kohonen
Exercises with Kohonen Self Organizing Maps. Mapping colour space to 2D graph,
maping linear functions, etc.

To be done (in emulated space):
- space learning "robotic arm"
- balancing robot

## mendelputer
Bayesian Network computer for finding genetic traits in ancestry tree (e.g. child blood type).

## perceptron
Plays with one of the simples neural models.
