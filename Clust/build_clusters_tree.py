import gensim
import math

K = 5000
D = 200
INF = 1e9

centers = [None] * (2 * K)
for i in range(2 * K):
    centers[i] = [0.0] * D

clusters_size = [0] * (2 * K)

# for every cluster save the nearest cluster and the distance between them
min_dist = [(INF, -1)] * (2 * K)

# for every node (cluster) save links to its 2 children
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


def norm(v):
    n = 0
    for i in range(D):
        n += v[i]*v[i]
    return math.sqrt(n)


def cosine_distance(x, y):
    dist = 1
    #norm_x = norm(x)
    #norm_y = norm(y)
    product = 0
    for i in range(D):
        product += x[i] * y[i]
    #product /= (norm_x * norm_y)
    return dist - product


cnt_clusters = K


# merge clusters with numbers j and k to one new cluster
def merge_clusters(j, k):
    j = int(j)
    k = int(k)
    centers[cnt_clusters] = [0.0] * D
    add(centers[cnt_clusters], multiplication(centers[j], clusters_size[j]))
    add(centers[cnt_clusters], multiplication(centers[k], clusters_size[k]))
    clusters_size[cnt_clusters] = clusters_size[j] + clusters_size[k]
    division(centers[cnt_clusters], norm(centers[cnt_clusters]))
    tree[cnt_clusters] = (j, k)
    active_clusters[cnt_clusters] = True
    active_clusters[j] = False
    active_clusters[k] = False


# minimum for tuples
def min(t1, t2):
    if t1[0] < t2[0]:
        return t1

    return t2

print("Building model")

model = gensim.models.Word2Vec.load_word2vec_format('../Word2Vec/all.s200.w11.n1.v20.cbow.bin', binary=True, unicode_errors='ignore')

print("Built model")


cnt = 0
with open('clusters/clusters_all.txt') as f:
    for line in f:
        data = line.split(" ")
        cluster_id = int(data[1])
        if cluster_id >= K:
            continue
        word = data[0]
        x = model[word]
        vec_norm = norm(x)
        add(centers[cluster_id], division(x, vec_norm))
        clusters_size[cluster_id] += 1
        cnt += 1
        if cnt % 100000 == 0:
            print("Load %d words\n" % cnt)

print("Load clusters")

for i in range(K):
    if clusters_size[i] > 0:
        division(centers[i], clusters_size[i])
    else:
        active_clusters[i] = False

print("Compute distances")

for i in range(K):
    if not active_clusters[i]:
        continue
    for j in range(i + 1, K):
        if not active_clusters[j]:
            continue
        dist = cosine_distance(centers[i], centers[j])
        if min_dist[i][0] > dist:
            min_dist[i] = (dist, j)
        if min_dist[j][0] > dist:
            min_dist[j] = (dist, i)


print("Building clusters tree...")

cnt = 0
for it in range(K - 1):
    min_tuple = (INF, -1)
    dist = INF
    for i in range(2 * K):
        if not active_clusters[i]:
            continue

        min_tuple = min(min_dist[i], min_tuple)

    print("Iteration #%d" % cnt)
    print(min_tuple[1])

    if min_tuple[1] == -1:
        break
    print(min_dist[min_tuple[1]][1])
    print(min_tuple[0])
    merge_clusters(min_tuple[1], min_dist[min_tuple[1]][1])

    for i in range(cnt_clusters + 1):
        if not active_clusters[i]:
            continue

        if i != cnt_clusters:
            d = cosine_distance(centers[i], centers[cnt_clusters])
            min_dist[i] = min(min_dist[i], (d, cnt_clusters))
            min_dist[cnt_clusters] = min(min_dist[cnt_clusters], (d, i))

        if not active_clusters[min_dist[i][1]]:
            min_dist[i] = (INF, -1)
            for j in range(2 * K):
                if not active_clusters[j]:
                    continue
                if i == j:
                    continue

                d = cosine_distance(centers[i], centers[j])
                min_dist[i] = min(min_dist[i], (d, j))

    cnt_clusters += 1
    cnt += 1

print("Built clusters tree")
f = open("clusters/cluster_tree.txt", "w")

for i in range(2 * K):
    if tree[i] is not None:
        f.write(str(i) + " ")
        f.write(str(tree[i][0]) + " " + str(tree[i][1]))
        f.write("\n")


