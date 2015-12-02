from math import log2

file = open('../DecisionTree/MenNames.txt')

men_names = []
all_men_names = []

id = 0
for line in file:
    if (id % 2 == 0):
        men_names.append(line)
    all_men_names.append(line)
    id += 1

file = open('../DecisionTree/WomenNames.txt')

women_names = []
all_women_names = []

id = 0
for line in file:
    if (id % 2 == 0):
        women_names.append(line)
    all_women_names.append(line)
    id += 1

def count_prob(name, names):
    last = name[len(name) - 2]
    pre_last = name[len(name) - 3]
    prob = -log2(len(names))

    cnt_last = 0
    cnt_pre_last = 0
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

correct = 0
wrong = 0
for name in all_men_names:
    if (count_prob(name, men_names) < count_prob(name, women_names)):
        wrong += 1
    else:
        correct += 1

for name in all_women_names:
    if (count_prob(name, men_names) > count_prob(name, women_names)):
        wrong += 1
    else:
        correct += 1


print("correct: %d\nwrong: %d" % (correct, wrong))
