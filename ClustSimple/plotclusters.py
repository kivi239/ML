import matplotlib.pyplot as plt

colors = ['ro', 'bo', 'go', 'mo', 'co', 'yo']

id_col = -1;

with open('clusters.txt', 'r') as f:
    for line in f:
        if line[0] == 'C':
            id_col += 1
            id_col %= 6
            continue
        vec = []
        for coord in line.split(" "):
            vec.append(float(coord))
        print(vec)
        plt.plot(vec[0], vec[1], colors[id_col])

plt.axis([0, 100, 0, 100])

plt.show()
