K = 5000
C_COMMON = 0.2

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

print("Load words")

f = open("new_clusters_from_5000.txt", "w")

was = set()

cnt_all = 1
cnt_clust = 0
new_clusters = [[]]

for word in id_cluster1:
    if cnt_all % 10000 == 0:
        print("Process %d words" % cnt_all)

    if word in was:
        cnt_all += 1
        continue

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
    if c1 >= C_COMMON and c2 >= C_COMMON:
        new_clusters[cnt_clust] = [[]]
        f.write("Cluster #%d: " % cnt_clust)
        for neighbor in common_neighbors:
            new_clusters.append(neighbor)
            was.add(neighbor)
            f.write(neighbor + " ")
        f.write("\n")
        cnt_clust += 1

    cnt_all += 1

print("Number of new clusters: %d (were %d)\n" % (cnt_clust, K))



