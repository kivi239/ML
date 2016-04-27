import prepare_sentence_stream
import gensim

separators = ['...', '.', '?', '!']
trash = ['"', '--', '(', ')', ':', ',', ';']


file = '../text/ch.txt'
sentence_stream = prepare_sentence_stream.file_to_stream(file)
text = prepare_sentence_stream.file_to_stream(file, seps=separators, trs=trash)

print(sentence_stream)

bigram = gensim.models.phrases.Phrases(sentence_stream, min_count=5, threshold=10)
print(bigram)

new_sentences = list(bigram[text])

new_file = '../text/ch_bigrams.txt'
f = open(new_file, 'w', encoding='utf-8')
for l in new_sentences:
    for word in l:
        f.write(word + ' ')
    f.write('\n')


