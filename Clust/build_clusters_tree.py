import gensim
import math

K = 5000
D = 200
INF = 1e9

centers = [None] * (2 * K)
for i in range(2 * K):
    centers[i] = [0.0] * D

clusters_size = [0] * K

min_dist = [(INF, -1)] * (2 * K)

tree = [None] * (2 * K)

active_clusters = [True] * (2 * K)
for i in range(K, 2 * K):
    active_clusters[i] = False


def add(x, y):
    for i in range(D):
        x[i] += y[i]
    return x


def division(x, n):
    for i in range(D):
        x[i] /= n
    return x


def multiplication(x, n):
    y = [0.0] * D
    for i in range(D):
        y[i] = x[i] * n
    return y


def norm(x):
    n = 0
    for c in x:
        n += c**2
    return math.sqrt(n)


def cosine_distance(x, y):
    dist = 1
    norm_x = norm(x)
    norm_y = norm(y)
    product = 0
    for i in range(D):
        product += x[i] * y[i]
    product /= (norm_x * norm_y)
    return dist - product


cnt_clusters = K


# merge clusters with numbers j and k to one new cluster
def merge_clusters(j, k):
    add(centers[cnt_clusters], multiplication(centers[j], clusters_size[j]))
    add(centers[cnt_clusters], multiplication(centers[k], clusters_size[k]))
    clusters_size[cnt_clusters] = clusters_size[j] + clusters_size[k]
    division(centers[cnt_clusters], clusters_size[cnt_clusters])
    tree[cnt_clusters] = (j, k)
    active_clusters[cnt_clusters] = True
    active_clusters[j] = False
    active_clusters[k] = False

print("Building model")

model = gensim.models.Word2Vec.load_word2vec_format('../Word2Vec/all.s200.w11.n1.v20.cbow.bin', binary=True, unicode_errors='ignore')

print("Built model")


with open('clusters/clusters_all.txt') as f:
    for line in f:
        data = line.split(" ")
        cluster_id = int(data[1])
        word = data[0]
        x = model[word]
        vec_norm = norm(x)
        add(centers[cluster_id], division(x, vec_norm))
        clusters_size[cluster_id] += 1


print("Load clusters")

for i in range(K):
    division(centers[i], clusters_size[i])


print("Compute distances")

for i in range(K):
    for j in range(i + 1, K):
        dist = cosine_distance(centers[i], centers[j])
        if min_dist[i][0] > dist:
            min_dist[i] = (dist, j)
        if min_dist[j][0] > dist:
            min_dist[j] = (dist, i)


print("Building clusters tree...")

for it in range(K):
    min_tuple = (-1, -1)
    dist = INF
    for i in range(2 * K):
        if not active_clusters[i]:
            continue

        if min_dist[i][0] < dist:
            min_tuple = (i, min_dist[i][1])
            dist = min_dist[i][0]

    print(min_tuple)
    merge_clusters(min_tuple[0], min_tuple[1])
    cnt_clusters += 1

print("Built clusters tree")
f = open("clusters/cluster_tree.txt", "w")

for i in range(2 * K):
    if tree[i] is not None:
        f.write(str(i) + " ")
        f.write(str(tree[i][0]) + " " + str(tree[i][1]))


