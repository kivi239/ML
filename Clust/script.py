import gensim
import pymorphy2
from sklearn.cluster import MiniBatchKMeans
print("Building model")

model = gensim.models.Word2Vec.load_word2vec_format('../Word2Vec/all.s300.w11.n1.v30.cbow.bin', binary=True, unicode_errors='ignore')

print("Built model")

clust = MiniBatchKMeans(n_clusters=5000, init='k-means++', max_iter=60, batch_size=10000)

data = [] #[[0, 2], [1, 1], [5, 5], [4, 6]]

words = []

morph = pymorphy2.MorphAnalyzer()

for word in model.vocab.keys():
    if word == morph.parse(word)[0].normal_form:
        data.append(model[word])
        words.append(word)

print("Start clustering, %d words" % len(words))

res = clust.fit(data)

print("finish clustering")

f = open('clusters_all_5000.txt', 'w')

for i in range(len(data)):
    f.write(words[i] + ' ')
    f.write(str(res.labels_[i]))
    f.write('\n')








