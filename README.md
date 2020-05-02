# Snake AI project:

A project to start working with ML algorithms. This is a program using a deep reinforcement learning to play a snake game. There are a billion articles about this, this project is meant to learn different approaches to solving the snake game using reiforcement learning.

## How to run

Argparser is pretty cool
```
usage: simpleQ.py | deepQ.py [-h] [--display bool] [--wait int]

Run simple Q learning algorithm

optional arguments:
  -h, --help      show this help message and exit
  --display bool  If you want a ui or not
  --wait int      how long to wait till next action (bigger the number slower
```

## Notes
### General flow

1. Initialize the Q-table by all zeros.
2. Start exploring actions: For each state, select any one among all possible actions for the current state (S).
3. Travel to the next state (S') as alpha result of that action (alpha).
4. For all possible actions from the state (S') select the one with the highest Q-value.
5. Update Q-table values using the equation.
6. Set the next state as the current state.
7. If goal state is reached, then end and repeat the process.

## References

- According to this [article](https://towardsdatascience.com/how-to-teach-an-ai-to-play-games-deep-reinforcement-learning-28f9b920440a), there can be results of 45 with only 150 games...




