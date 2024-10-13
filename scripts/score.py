#!/usr/bin/python3

import sys
import matplotlib.pyplot as plt
import numpy as np
import statistics

"""
Invariants: The data is valid
"""

questions = np.arange(1, 101, step=1)
answer_frequencies = np.zeros(100, dtype=np.float64)
all_scores = []

def get_val(val: str):
    if val == '0':
        return 1
    elif val == '1':
        return 0
    else:
        print("Invalid value", sys.stderr)
        exit(1)

with open("./logs/score.log") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        date, time, ip, scores = map(str.strip, line.split())
        score = 0
        for i in range(100):
            answer_frequencies[i] += get_val(scores[i])
            score += get_val(scores[i])
        all_scores.append(score)
print(f"Responses: {len(all_scores)}")
print(f"Mean score: {statistics.mean(all_scores)}")
print(f"Standard deviation: {statistics.stdev(all_scores)}")
print(f"Min score: {min(all_scores)}")
print(f"Max score: {max(all_scores)}")
fig, ax = plt.subplots()

ax.bar(questions, answer_frequencies)
ax.set_ylabel("Occurances")
ax.set_xlabel("Question #")
plt.show()
