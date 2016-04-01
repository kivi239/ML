# coding=utf-8
import math
import gensim
import pymorphy2
import time
from sklearn.cluster import MiniBatchKMeans

K = 5000
D = 200


def division(x, n):
    for i in range(D):
        x[i] /= n
    return x


def norm(x):
    n = 0
    for c in x:
        n += c**2
    return math.sqrt(n)


t = time.time()

print("Building model")

model = gensim.models.Word2Vec.load_word2vec_format('../Word2Vec/all.s200.w11.n1.v20.cbow.bin', binary=True, unicode_errors='ignore')

print("Built model")

print(time.time() - t)
t = time.time()

clust = MiniBatchKMeans(n_clusters=5000, init='k-means++', max_iter=60, batch_size=10000)

data = [] #[[0, 2], [1, 1], [5, 5], [4, 6]]

words = []

morph = pymorphy2.MorphAnalyzer()

for word in model.vocab.keys():
    if word == morph.parse(word)[0].normal_form:
        x = model[word]
        words.append(word)
        vec_norm = norm(x)
        data.append(division(x, vec_norm))


print("Start clustering, %d words" % len(words))

res = clust.fit(data)

print("finish clustering")
print(time.time() - t)

f = open('clusters_all_5000_2.txt', 'w')

for i in range(len(data)):
    try:
        f.write(words[i] + ' ')
        f.write(str(res.labels_[i]))
        f.write('\n')
    except UnicodeEncodeError:
        print("can't encode")

