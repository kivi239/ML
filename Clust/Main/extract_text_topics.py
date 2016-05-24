import gensim
import math
import pymorphy2
from sklearn.cluster import MiniBatchKMeans
from operator import itemgetter

D = 200 + 25
INF = 1e9


def extract_text_topics(file, type_file, K, user_id, model):
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
        product = 0
        for i in range(D):
            product += x[i] * y[i]
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
    def minimum_tuple(t1, t2):
        if t1[0] < t2[0]:
            return t1

        return t2

    print("Building model")

    small_model = gensim.models.Word2Vec.load_word2vec_format('word2vec/w2v_' + type_file + '.bin', binary=True, unicode_errors='ignore')

    print("Built model")

    morph = pymorphy2.MorphAnalyzer()

    separators = ['...', '.', '?', '!']
    trash = ['"', '--', '(', ')', ',', ';', ':', ':']

    # we will cache normal forms of words
    normal_forms = dict()
    id_words = dict()
    word_ids = []

    cur_id = 0
    data = []

    with open(file, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip("\n")
            for sep in separators:
                line = line.replace(sep, '|')
            paragraph = line.split('|')
            for sentence in paragraph:
                words = sentence.split(" ")
                for word in words:
                    for t in trash:
                        word = word.replace(t, "")
                    if word == "":
                        continue
                    if word not in normal_forms:
                        unnorm = word
                        norm_word = morph.parse(word)[0].normal_form
                        normal_forms[word] = norm_word
                        word = norm_word

                        tags = morph.parse(word)[0].tag
                        if 'NOUN' not in tags and 'LATN' not in tags: # and 'ADJF' not in tags: # and 'VERB' not in tags and 'INFN' not in tags:
                            continue
                        if norm_word not in model:
                            continue
                        if word in id_words:
                            continue

                        x = []
                        for c in model[word]:
                            x.append(c)
                        if word not in small_model:
                            word = unnorm

                        if word not in small_model:
                            # print("WTF???" + word)
                            # print(norm_word)
                            continue

                        id_words[norm_word] = cur_id
                        word_ids.append(norm_word)
                        cur_id += 1

                        for c in small_model[word]:
                            x.append(c)
                        x_norm = norm(x)
                        data.append(division(x, x_norm))

    # print("#####")
    # print(len(normal_forms))
    # print(len(word_ids))
    # print(len(id_words))
    # print("#####")

    K = min(K, len(id_words))
    print(K)
    clust = MiniBatchKMeans(n_clusters=K, init='k-means++', max_iter=100, batch_size=10000)

    res = clust.fit(data)

    print("Finish clusterization")

    for i in range(len(data)):
        cluster_id = res.labels_[i]
        x = data[i]
        vec_norm = norm(x)
        add(centers[cluster_id], division(x, vec_norm))
        clusters_size[cluster_id] += 1

    #print("Load clusters")

    for i in range(K):
        if clusters_size[i] > 0:
            division(centers[i], clusters_size[i])
        else:
            active_clusters[i] = False

    #print("Compute distances")

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

            min_tuple = minimum_tuple(min_dist[i], min_tuple)

        #print("Iteration #%d" % cnt)
        #print(min_tuple[1])

        if min_tuple[1] == -1:
            break
        #print(min_dist[min_tuple[1]][1])
        #print(min_tuple[0])
        merge_clusters(min_tuple[1], min_dist[min_tuple[1]][1])

        for i in range(cnt_clusters + 1):
            if not active_clusters[i]:
                continue

            if i != cnt_clusters:
                d = cosine_distance(centers[i], centers[cnt_clusters])
                min_dist[i] = minimum_tuple(min_dist[i], (d, cnt_clusters))
                min_dist[cnt_clusters] = minimum_tuple(min_dist[cnt_clusters], (d, i))

            if not active_clusters[min_dist[i][1]]:
                min_dist[i] = (INF, -1)
                for j in range(2 * K):
                    if not active_clusters[j]:
                        continue
                    if i == j:
                        continue

                    d = cosine_distance(centers[i], centers[j])
                    min_dist[i] = minimum_tuple(min_dist[i], (d, j))

        cnt_clusters += 1
        cnt += 1

    print("Built clusters tree")

    d = [-1] * (2 * K)

    def dfs(v):
        if tree[v] is None:
            return
        d[tree[v][0]] = d[v] + 1
        d[tree[v][1]] = d[v] + 1

        dfs(tree[v][0])
        dfs(tree[v][1])

    dfs(cnt_clusters - 1)
    depth = [-1] * len(word_ids)
    max_depth = -1
    for i in range(len(word_ids)):
        depth[i] = d[res.labels_[i]]
        max_depth = max(max_depth, depth[i])

    degree = dict()
    max_degree = -1

    with open('../OK_recommend/user' + user_id + '/words_degrees_' + type_file + '.txt', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip("\n")
            data = line.split(" ")
            degree[data[0]] = int(data[1])
            max_degree = max(max_degree, int(data[1]))

    max_degree = math.log(1 + max_degree)

    score = [None] * len(word_ids)

    for i in range(len(word_ids)):
        #print(word_ids[i])
        #print(degree[word_ids[i]])

        score[i] = ((depth[i] / max_depth) * (math.log(1 + degree[word_ids[i]]) / max_degree), word_ids[i])

    score.sort(key=itemgetter(0), reverse=True)

    g = open('../OK_recommend/user' + user_id + '/words_scoring_' + type_file + str(K) + '.txt', 'w', encoding='utf-8')
    for t in score:
        g.write(t[1] + ' ' + str("%.10f" % t[0]) + '\n')

    topic_score = [0] * K
    words_in_topic = [None] * K
    for i in range(len(score)):
        id_cluster = res.labels_[id_words[score[i][1]]]
        topic_score[id_cluster] += score[i][0]
        if words_in_topic[id_cluster] is None:
            words_in_topic[id_cluster] = []
        words_in_topic[id_cluster].append(score[i])

    for i in range(K):
        if len(words_in_topic[i]) != 0:
            topic_score[i] /= len(words_in_topic[i])

    topic_score_sort = [None] * K
    for i in range(K):
        topic_score_sort[i] = (topic_score[i], i)

    topic_score_sort.sort(key=itemgetter(0), reverse=True)

    h = open('../OK_recommend/user' + user_id + '/topics_scoring_' + type_file + str(K) + '.txt', 'w', encoding='utf-8')
    for i in range(K):
        id_topic = topic_score_sort[i][1]
        h.write("Topic #" + str(id_topic) + ": " + str("%.5f" % topic_score_sort[i][0]) + "\n")
        h.write(" ")
        for j in range(min(20, len(words_in_topic[id_topic]))):
            h.write(words_in_topic[id_topic][j][1] + " ")
        h.write("\n")

    return topic_score, words_in_topic, score, word_ids, id_words, K

