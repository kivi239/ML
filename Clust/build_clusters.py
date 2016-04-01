K = 5000

clusters = [[]]
for i in range(K):
    clusters.append([])

def remove_newline(a):
    a = a.split("\n")[0]
    return a

with open("clusters_all_5000_2.txt") as f:
    for line in f:
        data = line.split(" ")
        clusters[int(remove_newline(data[1])) - 1].append(data[0])

f = open("clusters/clusters_all_5000_2_distr.txt", "w")
for i in range(K):
    f.write("Cluster #" + str(i) + ": ")
    for word in clusters[i]:
        f.write(word + ' ')
    f.write('\n')
