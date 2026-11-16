import matplotlib.pyplot as plt

r = 0.7

def logistics_func(x):
    return r * x * (1 - x)

x = [0.5]

for i in range(10000):
    x.append(logistics_func(x[i]))
    print(x[i])

plt.plot(x)
plt.show()
    