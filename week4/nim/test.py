from nim import *

ai = NimAI(alpha=0.75)
ai.q = {
        ((1, 2, 2, 4), (0, 1)): 0.3,
        ((1, 2, 2, 4), (1, 1)): 0.2,
        ((1, 2, 2, 4), (1, 2)): 0.4,
        ((1, 2, 2, 4), (2, 1)): 0.25,
    }
expected = 0.4

print("Expected result:", expected)
print("Actual result:", ai.best_future_reward([1, 2, 2, 4]))
