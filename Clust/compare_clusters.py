K = 5000
C_COMMON = 0.4

clusters1 = [[]]
id_cluster1 = dict()

clusters2 = [[]]
id_cluster2 = dict()


for i in range(K):
    clusters1.append([])
    clusters2.append([])

with open("clusters_all_5000.txt") as f:
    for line in f:
        data = line.split(" ")
        id = int((data[1]).rstrip("\n")) - 1
        word = data[0]
        clusters1[id].append(word)
        id_cluster1[word] = id

with open("clusters_all_5000_2.txt") as f:
    for line in f:
        data = line.split(" ")
        id = int((data[1]).rstrip("\n")) - 1
        word = data[0]
        clusters2[id].append(word)
        id_cluster2[word] = id


f = open("restless_words.txt", "w")

cnt = 0
cnt_all = 1
for word in id_cluster1:
    if cnt_all % 10000 == 0:
        print("Process %d words" % cnt_all)
    id1 = id_cluster1[word]
    neighbors1 = set()
    for neighbor in clusters1[id1]:
        neighbors1.add(neighbor)

    id2 = id_cluster2[word]
    neighbors2 = set()
    for neighbor in clusters2[id2]:
        neighbors2.add(neighbor)
    common_neighbors = neighbors1.intersection(neighbors2)

    c1 = len(common_neighbors) / len(neighbors1)
    c2 = len(common_neighbors) / len(neighbors2)
    if c1 <= C_COMMON or c2 <= C_COMMON:
        f.write(word + ' ' + ("%.3f " % c1) + ("%.3f " % c2) + '\n')
        cnt += 1
    cnt_all += 1

print("Number of restless words: %d out of %d\n" % (cnt, len(id_cluster1)))



