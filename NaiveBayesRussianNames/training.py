from math import log2

file = open('../DecisionTree/MenNames.txt')

men_names = []

for line in file:
    men_names.append(line)

file = open('../DecisionTree/WomenNames.txt')

women_names = []

for line in file:
    women_names.append(line)

name = input()

last = name[len(name) - 1]
pre_last = name[len(name) - 2]

def count_prob(name, names):
    last = name[len(name) - 1]
    pre_last = name[len(name) - 2]
    prob = -log2(len(names));

    cnt_last = 0;
    cnt_pre_last = 0;
    for line in names:
        if line[len(line) - 2] == last:
            cnt_last += 1
        if line[len(line) - 3] == pre_last:
            cnt_pre_last += 1

    if (cnt_last > 0):
        prob += log2(cnt_last) - log2(len(names))
    else:
        prob -= (1e9)

    if (cnt_pre_last > 0):
        prob += log2(cnt_pre_last) - log2(len(names))
    else:
        prob -= (1e9)

    return prob


if count_prob(name, men_names) < count_prob(name, women_names):
    print("Woman")
else:
    print("Man")