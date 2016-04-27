import prepare_sentence_stream
import gensim

#model = gensim.models.Word2Vec.load_word2vec_format('../../Word2Vec/all.s200.w11.n1.v20.cbow.bin', binary=True, unicode_errors='ignore')
#print("Loaded model")

file = '../text/ch.txt'
sentence_stream = prepare_sentence_stream.file_to_stream(file)

print(sentence_stream)

bigram = gensim.models.phrases.Phrases(sentence_stream, min_count=5, threshold=10)
print(bigram)

new_sentences = list(bigram[sentence_stream])

# do we need to convert all words to lower case?
'''for l in new_sentences:
    for i in range(len(l)):
        l[i] = l[i].lower()
'''

print("Read sentences, building model...")

model = gensim.models.word2vec.Word2Vec(new_sentences, size=25)
file_name = 'word2vec/w2v.bin'
model.save_word2vec_format(file_name, binary=True)

text_file_name = 'word2vec/w.txt'
f = open(text_file_name, 'w', encoding='utf-8')
for key in model.vocab.keys():
    f.write(key + ' ')
    for x in model[key]:
        f.write(str(x) + ' ')
    f.write("\n")


print(model.vocab.keys())
