import random
import numpy as np
from numpy.linalg import *
from numpy import *
import matplotlib.pyplot as plt

def generate():
    N = random.randint(20, 60)
    a = random.randint(1, 10)
    b = random.randint(-15, 15)
    print(a, b)
    x = np.zeros(N)
    y = np.zeros(N)
    for i in range(N):
        x[i] = random.randint(0, 20)
        y[i] = a * x[i] + b + random.randint(-5, 5)

    return x, y

x, y = generate()
n = len(x)
plt.plot(x, y, 'ro')

arr = np.zeros(shape=(n, 2))

for i in range(n):
    arr[i][0] = 1
    arr[i][1] = x[i]

a = np.asmatrix(arr)
at = a.transpose()

mn = inv(matmul(at, a))
w = matmul(matmul(mn, at), y)

a = w.item(1)
b = w.item(0)
print(a, b)

def y(x):
    return a * x + b

t = np.arange(0, 20, 0.1)
plt.plot(t, y(t))

plt.show()


