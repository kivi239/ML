from math import log2

file = open("MenNames.txt")

men_names = []
for line in file:
    men_names.append(line)

file = open("WomenNames.txt")

women_names = []
for line in file:
    women_names.append(line)


def letter_a(name):
    l = len(name)
    return name[l - 2] == 'а'

def letter_not_a(name):
    l = len(name)
    return name[l - 2] != 'а'


def true(name):
    return True


def entropy(f):
    cnt_men = 0
    cnt_women = 0
    for name in men_names:
        cnt_men += f(name);

    for name in women_names:
        cnt_women += f(name)

    cnt_all = cnt_men + cnt_women;
    return -(cnt_men / cnt_all * log2(cnt_men/cnt_all) + cnt_women / cnt_all * log2(cnt_women/cnt_all))

print(entropy(true))

print(entropy(letter_a))
print(entropy(letter_not_a))