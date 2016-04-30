from ExtractBigrams import prepare_sentence_stream
import gensim

separators = ['...', '.', '?', '!']
trash = ['"', '--', '(', ')', ':', ',', ';']

file = '../text/ch.txt'

text = prepare_sentence_stream.file_to_stream(file, seps=separators, trs=trash)

file_txt = 'word2vec/text.txt'
f = open(file_txt, 'w', encoding='utf-8')
f.write(str(text))

model = gensim.models.word2vec.Word2Vec(text, min_count=1, size=25)
file_name = 'word2vec/w2v.bin'
model.save_word2vec_format(file_name, binary=True)
print(model.vocab.keys())
text_file_name = 'word2vec/w.txt'
f = open(text_file_name, 'w', encoding='utf-8')
for key in model.vocab.keys():
    f.write(key + ' ')

    for x in model[key]:
        f.write(str(x) + ' ')
    f.write("\n")


