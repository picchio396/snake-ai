# Snake AI project:

My project to start working with ML algorithms. This is a program using a deep reinforcement learning to play a snake game.

## Dependencies

- python 3.7.2
- gym
- pygame
- my custom gym environment
    ( ex: `pip3 install -e ./gym-snake` )

## How to run

For now, run test.py

## Issues

- According to this [article](https://towardsdatascience.com/how-to-teach-an-ai-to-play-games-deep-reinforcement-learning-28f9b920440a), there can be results of 45 in only 150 games.<br />
I ran the test more than 1000 and did not get a highscore greater than 3...
I'm not sure if it is because my environment variables (alpha, gamma and epsilon) are wrong or if the whole flow is wrong.
- I save the observation space as an array and store all possible values. I don't think this is a good approach because it generates a massive array and there is probably a better way to do it. 
- Now that I think about, the whole reward system might be broken. Currently, the state is the relative tail position and the relative distance to the food and that is it (no knowledge of the board).


