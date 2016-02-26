# coding=utf-8
import pymorphy2
import math

with open('bad_texts.txt') as bad_file:
    bad = bad_file.readlines()

with open('good_texts.txt') as good_file:
    good = good_file.readlines()

with open('neutral_texts.txt') as neutral_file:
    neutral = neutral_file.readlines()

morph = pymorphy2.MorphAnalyzer()

def count_words(class_data):
    cnt = 0
    for review in class_data:
        for w in review.split(" "):
           cnt += 1
    return cnt

all_texts = bad + good + neutral
print("Please, enter your review\n")
review = input()

def word_remove_symbols(word):
    letters = list(u".,…!?-()$#;:+=%^&*<>\"'[]{}\\/~—«»")
    cnt = 0
    for letter in letters:
        if word.find(letter) != -1:
            word = word.replace(letter, '')
            cnt += 1
    return word, cnt

def norm(word, morph):
    return set(map(lambda w: w.normal_form, morph.parse(word)))

norm_review = ""
for word in review.split(" "):
    word, pnt_cnt = word_remove_symbols(word)
    norm_review += list(norm(word, morph))[0] + " "

print(norm_review)

# 'word': (bad, good, neutral)
prob_dict = {}
with open('weights.in', 'r') as f:
    for line in f:
        data = line.split(" ")
        word = data[0]
        a = float(data[1])
        b = float(data[2])
        c = float(data[3])

        prob_dict[word] = (a, b, c)

print("Finish reading the weights")


words_in = [count_words(bad), count_words(good), count_words(neutral)]
V = len(prob_dict)

def calc_probability(class_data, review, class_id):
    prob = math.log2(len(class_data)) - math.log2(len(all_texts))
    for word in review.split(" "):
        if (word == ""): continue
        if (word not in prob_dict): continue

        prob += prob_dict[word][class_id]

    return prob


prob_good = calc_probability(good, norm_review, 1)
prob_bad = calc_probability(bad, norm_review, 0)
prob_neutral = calc_probability(neutral, norm_review, 2)
print("Log of probability that it is a good review:    %.5lf\n" % (prob_good))
print("Log of probability that it is a bad review:     %.5lf\n" % (prob_bad))
print("Log of probability that it is a neutral review: %.5lf\n" % (prob_neutral))

if (prob_good > prob_bad and prob_good > prob_neutral):
    print("Good review")
if (prob_bad > prob_good and prob_bad > prob_neutral):
    print("Bad review")
if (prob_neutral > prob_bad and prob_neutral > prob_good):
    print("Neutral review")
