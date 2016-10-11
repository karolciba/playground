# Markov Desicion Process

Self excercises to dive deep into subject from [Berkeley AI](http://ai.berkeley.edu).
Miniproject from the course deals with limited scope. To widen my understanding I thought about a bit bigger problem.

Pong, despite it's simple rules, has vast state space in naive approach. Sharading board into segments results in hundreds of thousand states anyway.
Newertheless, simples solution will act as a reference point [Pong AI](https://rawcdn.githack.com/karolciba/playground/master/mdp/pong/pong.html).

First small improvements:
- introducting teacher for AI to observe, and learn Q-Values distribution from.
- "retrospective" to improve convergence. Actions outcomes are back-propagated.
Which speed up learning rate, still not allowing to agent to place decenty, though.


Second approach should be approximating agentr. Which should learn how to value state rather than build exact statistics.
