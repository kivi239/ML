import matplotlib.pyplot as plt

x = []
y = []

with open('sample2d.in') as f:
    for line in f:
        data = []
        for numb in line.split(" "):
            data.append(float(numb))
        x.append(data[0])
        y.append(data[1])

plt.plot(x, y, 'bo')

with open('centers.txt') as g:
    for line in g:
        data = []
        for numb in line.split(" "):
            data.append(float(numb))
        plt.plot(data[0], data[1], 'rD')
plt.axis([0, 100, 0, 100])

plt.show()

