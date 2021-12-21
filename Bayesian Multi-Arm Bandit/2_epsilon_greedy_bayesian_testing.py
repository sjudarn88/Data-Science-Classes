# -*- coding: utf-8 -*-
"""Bayesian ML Class Code 2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fHXE8f_TNCS9iqW8bRHyoBjuIBN01PvW

**Class code 1: Epsilon-Greedy Bayesian Testing**
"""

import numpy as np
import random
import matplotlib.pyplot as plt

# set starting params
NUM_TRIALS =10000
EPS = 0.1
# win rate probability of each bandit, here we have 3 bandits.
BANDIT_PROBABILITIES = [0.2, 0.5, 0.75]

class BanditArm:
  def __init__(self,p):
    # p: the win rate
    self.p = p 
    # p_estimate: current estimated win rate
    self.p_estimate = 0
    # N: numbers of samples collected so far
    self.N = 0
  
  def pull(self):
    # daw a 1 with probability p
    return np.random.random() < self.p
  
  # update the bandit after one pull, and x can be 0 or 1 from pull() function.
  def update(self,x):
    # add 1 to N, since we just collected 1 more sample.
    self.N += 1
    # update p_estimate for the new current win rate
    self.p_estimate = (self.p_estimate * (self.N - 1) + x) / self.N

def experiment():
  # initialize bandit objects with the expected probabilities
  bandits = [BanditArm(p) for p in BANDIT_PROBABILITIES]
  # rewards array stores the all rewards collected in each trial
  rewards = np.zeros(NUM_TRIALS)

  num_times_explored = 0
  num_times_exploited = 0
  # the number of time we chose the optimal bandit
  num_optimal = 0
  # retrieve the index corresponding to the bandit with the maximum true mean
  optimal_j = np.argmax([b.p for b in bandits])
  print("optimal j:",optimal_j)

  for i in range(NUM_TRIALS):
    # use epsilon-greedy to select the next bandit
    if np.random.random() <EPS:
      # if 1, we increase the counter for the number of times we explored
      num_times_explored += 1
      # if 1, we chose the bandit at random 
      j = np.random.randint(len(bandits))
    else:
      # if 2, we increase the counter for the number of times we exploited
      num_times_exploited += 1
      # if 2, we choose our current best bandit based on estimate of p
      j = np.argmax([b.p_estimate for b in bandits])

   # this only works due to simulation that we know the p for each bandit,
   # but in real work, we cannot know this since we don't know p.
   # optimal_j is fixed in this simulation, which is bandit 3 with 0.75 win rate.
    if j == optimal_j:
      num_optimal += 1

    # pull the the bandit of j by calling pull() function
    # we can reward from this pull, either 0 or 1
    x = bandits[j].pull()

    # we assign reward to the array of index i. 
    # reward array is an array consisting a bunch of 0s or 1s from each pull function.
    rewards[i] = x

    # update the distribution for the badit whose arm we just pulled
    bandits[j].update(x)

  # print mean estimates for each bandit
  for b in bandits:
    print("mean estimate:", b.p_estimate)

  # print total reward
  print("total reward earned:", rewards.sum())
  print("overall win rate:", rewards.sum() / NUM_TRIALS)
  print("num_times_explored:", num_times_explored)
  print("num_times_exploited:", num_times_exploited)
  print("num times selected optimal bandit:", num_optimal)

  # plot the results
  cumulative_rewards = np.cumsum(rewards)
  # accumulative win rate per iteration
  win_rates = cumulative_rewards / (np.arange(NUM_TRIALS) + 1)
  plt.plot(win_rates)
  plt.plot(np.ones(NUM_TRIALS)*np.max(BANDIT_PROBABILITIES))
  plt.show()

if __name__ == "__main__":
  experiment()