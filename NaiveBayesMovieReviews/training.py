import math

with open('bad_texts.txt') as bad_file:
    bad = bad_file.readlines()

with open('good_texts.txt') as good_file:
    good = good_file.readlines()

with open('neutral_texts.txt') as neutral_file:
    neutral = neutral_file.readlines()

def count_words(class_data):
    cnt = 0
    for review in class_data:
        for w in review.split(" "):
           cnt += 1
    return cnt

words_in_bad = count_words(bad)
words_in_good = count_words(good)
words_in_neutral = count_words(neutral)

all_texts = bad + good + neutral

dictionary = set()
for review in all_texts:
    for word in review.split(" "):
        if not (word in dictionary):
            dictionary.add(word)

dictionary.remove("")
print(len(dictionary))
V = len(dictionary)

# 'word': (bad, good, neutral)
prob_dict = {}

for review in bad:
    for word in review.split(" "):
        if word == "" : continue
        if not (word in prob_dict):
            prob_dict[word] = (1, 0, 0)
        else:
            (a, b, c) = prob_dict[word]
            prob_dict[word] = (a + 1, b, c)

for review in good:
    for word in review.split(" "):
        if word == "" : continue
        if not (word in prob_dict):
            prob_dict[word] = (0, 1, 0)
        else:
            (a, b, c) = prob_dict[word]
            prob_dict[word] = (a, 1, c)

for review in neutral:
    for word in review.split(" "):
        if word == "" : continue
        if not (word in prob_dict):
            prob_dict[word] = (0, 0, 1)
        else:
            (a, b, c) = prob_dict[word]
            prob_dict[word] = (a, b, c + 1)


print(prob_dict["ужасный"])
count = 0
f = open('weights.in', 'w')
for word in dictionary:
    if (count % 1000 == 0):
        print("%d words were processed" % count)
    probs = prob_dict[word]
    f.write("%s %.5lf %.5lf %.5lf\n" % (word, math.log2(probs[0] + 1) - math.log2(words_in_bad + V),
                                              math.log2(probs[1] + 1) - math.log2(words_in_good + V),
                                              math.log2(probs[2] + 1) - math.log2(words_in_neutral + V) ))

    count += 1
