import random
probability = {'a': 0.001, 'b': 0.005, 'c': 0.01, 'd': 0.1}

minProbability = probability['a']
for k, v in probability.items():
    if v < minProbability:
        minProbability = v
total = int(1 / minProbability)
number = random.randint(1, total)
rightProbability = 0
leftProbability = 0
for k, v in probability.items():
    rightProbability += v
    leftProbability = rightProbability - v
    if leftProbability* total < number <= rightProbability * total:
        print(f'{k}等奖，号码{number}')
        break

