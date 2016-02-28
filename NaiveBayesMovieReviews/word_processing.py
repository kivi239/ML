import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def word_remove_symbols(word):
    letters = list(u".,…!?-()$#;:+=%^&*<>\"'[]{}\\/~—«»“„\n")
    cnt = 0
    for letter in letters:
        if word.find(letter) != -1:
            word = word.replace(letter, '')
            cnt += 1
    return word, cnt


def norm(word, morph):
    return set(map(lambda w: w.normal_form, morph.parse(word)))

def process_reviews(filename, output):
    with open(filename, 'r') as f:
        cnt = 0
        for line in f:
            if cnt % 100 == 0:
                print("%d reviews were proceeded" % cnt)
            norm_review = ""
            for word in line.split(" "):
                word, pnt_cnt = word_remove_symbols(word)
                norm_review += list(norm(word, morph))[0] + " "
            output.write(norm_review + '\n')
            cnt += 1

bad_reviews = open('bad_texts.txt', 'w')
#good_reviews = open('good_texts.txt', 'w')
#neutral_reviews = open('neutral_texts.txt', 'w')

process_reviews('bad_texts_not_proc.txt', bad_reviews)
#process_reviews('good_texts_not_proc.txt', good_reviews)
#process_reviews('neutral_texts_not_proc.txt', neutral_reviews)