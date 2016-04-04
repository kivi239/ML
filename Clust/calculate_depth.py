from operator import itemgetter
K = 5000

# for every node (cluster) save links to its 2 children
tree = [None] * (2 * K)
# depth for each node
d = [-1] * (2 * K)


def dfs(v):
    if tree[v] is None:
        return
    d[tree[v][0]] = d[v] + 1
    d[tree[v][1]] = d[v] + 1

    dfs(tree[v][0])
    dfs(tree[v][1])


with open("clusters/cluster_tree.txt") as f:
    root_node = -1
    for line in f:
        data = line.split(" ")
        node = int(data[0])
        v1 = int(data[1])
        v2 = int(data[2])
        root_node = max(root_node, node)
        tree[node] = (v1, v2)

d[root_node] = 0
dfs(root_node)

node_with_d = [(-1, -1)] * (2 * K)
for i in range(2 * K):
    node_with_d[i] = (d[i], i)


def comp(x, y):
    return y[0] - x[0]


node_with_d.sort(key=itemgetter(0), reverse=True)

f = open("clusters/depth_of_clusters.txt", "w")

for i in range(2 * K):
    if node_with_d[i][0] == -1:
        continue
    f.write(str(node_with_d[i][1]) + " " + str(node_with_d[i][0]))
    f.write('\n')