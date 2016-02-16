# coding=utf-8
import pymorphy2

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
    letters = list(u".,!?-()$#;:+=%^&*<>\"'[]{}\\/~—«»")
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

def prob_of_word(word, class_data):
    count_class = 0
    for norm_review in class_data:
        for w in norm_review.split(" "):
            if (w == word):
                count_class += 1

    count_all_words = count_words(class_data)
    return (count_class + 1) / (count_all_words + 1)

def calc_probability(class_data, review):
    prob = len(class_data) / len(all_texts)
    for word in review.split(" "):
        prob *= prob_of_word(word, class_data)
    return prob

prob_good = calc_probability(good, norm_review)
prob_bad = calc_probability(bad, norm_review)
prob_neutral = calc_probability(neutral, norm_review)
print("Unnormalized probability that it is a good review:    %.15lf\n" % (prob_good))
print("Unnormalized probability that it is a bad review:     %.15lf\n" % (prob_bad))
print("Unnormalized probability that it is a neutral review: %.15lf\n" % (prob_neutral))

if (prob_good > prob_bad and prob_good > prob_neutral):
    print("Good review")
if (prob_bad > prob_good and prob_bad > prob_neutral):
    print("Bad review")
if (prob_neutral > prob_bad and prob_neutral > prob_good):
    print("Neutral review")
