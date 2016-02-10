with open('bad_texts.txt') as bad_file:
    bad = bad_file.readlines()

with open('good_texts.txt') as good_file:
    good = good_file.readlines()

with open('neutral_texts.txt') as neutral_file:
    neutral = neutral_file.readlines()

all_texts = bad + good + neutral
print("Please, enter your review\n")
review = input()

def prob_of_word(word, class_data):
    count_all = 0
    for review in all_texts:
        for w in review.split(" "):
            if (w == word):
                count_all += 1
    count_class = 0
    for review in class_data:
        for w in review.split(" "):
            if (w == word):
                count_class += 1

    if (count_all == 0):
        return 1

    return count_class / count_all



def calc_probability(class_data, review):
    prob = 1 #len(class_data) / len(all_texts)
    print(prob)
    for word in review.split(" "):
        prob *= prob_of_word(word, class_data)
    return prob

print("Unnormalized probability that it is a good review:    %.3lf\n" % (calc_probability(good, review)))
print("Unnormalized probability that it is a bad review:     %.3lf\n" % (calc_probability(bad, review)))
print("Unnormalized probability that it is a neutral review: %.3lf\n" % (calc_probability(neutral, review)))

