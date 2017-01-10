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

## Markov Decision Process
Playing with MDP. AI learning to play classical PONG game.
Available in browser [Pong AI](https://rawcdn.githack.com/karolciba/playground/master/mdp/pong/pong.html)

Further notes in subdirectory [mdp](mdk/README.md)

## Hidden Markov Model for Electrocardiogram
Attempts to model heart rythm with HMM for inference on pulse state.

Currently exercises with HMM algorithm in Crooked Casino from [Bioinformatics Algorithms](https://www.youtube.com/channel/UCKSUVRs2N2FdDNvQoRWKhoQ) course.

## neural networks
AI learning to play Google TRex. Attempts to learn to play using 2 layer backpropagated network.
In a kind of a reinfored learning (simplified [Pong from Pixels](http://karpathy.github.io/2016/05/31/rl/))

Further notes in subdirectory [neural](neural/README.md)

## kohonen
Exercises with Kohonen Self Organizing Maps. Mapping colour space to 2D graph,
maping linear functions, etc. More in subdirectory [kohonen](kohonen/README.mb)

### color space
Two dimensional kohonen map learning color space.
[![color space](http://img.youtube.com/vi/x50dj8LxJyI/0.jpg)](https://youtu.be/x50dj8LxJyI)
CLICK TO PLAY

To be done:
- space learning "robotic arm"
- balancing robot

## eucliderer
Graphics renderer capable of drawing geometry primitives: dots, lines, boxes, curves.
First implementation is to be 2D.

Visualization tool needed for other projects.

## mendelputer
Bayesian Network computer for finding genetic traits in ancestry tree (e.g. child blood type).

## perceptron
Plays with one of the simples neural models.
