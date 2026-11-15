# Homework 2 — A/B Testing 

This homework compares two ways of choosing between four advertisements: **Epsilon-Greedy** and **Thompson Sampling**. The goal is to learn which advertisement gives the highest average reward while avoiding too many selections of less effective advertisements.

## Experiment setup

- Four bandits with true average rewards of **1, 2, 3, and 4**.
- **20,000 trials per algorithm**.
- Each reward is drawn from a normal distribution with standard deviation **1**.
- Epsilon-Greedy explores with probability **1/t**, where `t` is the trial number. Otherwise, it chooses the bandit with the highest estimated average reward.
- Thompson Sampling uses a normal prior with mean **0** and precision **0.1**. Reward precision is known and set to **1**. It samples a possible mean from each posterior, chooses the highest sample, and updates that band's posterior after observing the reward.
- The comparison starts with random seed **42**, so repeated runs in the same environment give the same results.

## How to run

From the `HW2` folder, install the dependencies and run:

```bash
python -m pip install -r requirements.txt
python Bandit.py
```

The script uses Loguru to show the results in the terminal and creates the `outputs/` folder automatically.

## Output files

The program saves:

- `epsilon_greedy_rewards.csv` and `thompson_sampling_rewards.csv`: rewards from each algorithm.
- `bandit_rewards.csv`: both algorithms together, with the required `Bandit`, `Reward`, and `Algorithm` columns.
- `epsilon_greedy_learning.png` and `thompson_sampling_learning.png`: how the estimates change over time, shown with linear and logarithmic trial axes.
- `cumulative_rewards.png`: how much reward each algorithm earns over time.
- `cumulative_regrets.png`: how much expected reward each algorithm loses by not always choosing the best bandit.

## Understanding the measures

**Cumulative reward** is the sum of the rewards actually observed. Higher is better.

**Cumulative pseudo-regret** is the sum of the differences between the best band's true mean (4) and the true mean of the selected bandit. Lower is better. Using the true means for *evaluation* does not give the algorithms that information when they make their choices.

## Results from a run with seed 42

| Measure | Epsilon-Greedy | Thompson Sampling |
| --- | ---: | ---: |
| Cumulative observed reward | 79,734.47 | 79,925.13 |
| Cumulative pseudo-regret | 135 | 42 |

In this run, Thompson Sampling earned more reward and had less pseudo-regret. Epsilon-Greedy's exploration probability drops quickly with `1/t`, which can make it commit to an early estimate. Results can differ with other random seeds, so a single run does not prove that one algorithm always wins.

