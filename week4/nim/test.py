from nim import *

ai = NimAI(alpha=0.75)
ai.q = {
        ((1, 2, 2, 4), (0, 1)): 0.3,
        ((1, 2, 2, 4), (1, 1)): 0.2,
        ((1, 2, 2, 4), (1, 2)): 0.4,
        ((1, 2, 2, 4), (2, 1)): 0.25,
        ((1, 2, 2, 5), (2, 1)): 0.5,
    }
expected = (1, 2)
total = 1000
count = 0
for i in range(total):
    action = ai.choose_action([1, 2, 2, 4], epsilon=True)
    if action == expected:
        count += 1

print("Expected result:", expected)
print(count / total, 0.5, 0.3, "proportion of greedy moves")
