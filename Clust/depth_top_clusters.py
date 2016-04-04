K = 5000
TOP = 1000


clusters = [[]]
for i in range(K):
    clusters.append([])


g = open("clusters/top" + str(TOP) + "_clusters.txt", "w")

with open("clusters/clusters_all_distr.txt") as f:
    for line in f:
        line = line.lstrip("Cluster #")
        line.rstrip(" \n")

        data = line.split(" ")
        data[0] = data[0].rstrip(":")
        cluster_id =int(data[0])
        for i in range(1, len(data) - 1):
            clusters[cluster_id].append(data[i])

with open('clusters/depth_of_clusters.txt') as f:
    cnt = 0
    for line in f:
        cluster_id = line.split(" ")[0]
        cluster_id = int(cluster_id)
        if cluster_id >= K:
            continue
        g.write("Cluster #%d: " % cluster_id)
        for word in clusters[cluster_id]:
            g.write(word + " ")
        g.write("\n")
        cnt += 1
        if cnt == TOP:
            break