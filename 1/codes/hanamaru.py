import matplotlib.pyplot as plt
import numpy as np

n = 1000

theta = np.linspace(0, 2 * np.pi, n)
x1 = np.cos(theta)
y1 = np.sin(theta)

phi = np.linspace(0, 5 * 2 * np.pi, n)
x2 = (phi / (2 * np.pi) * 0.2) * np.cos(phi)
y2 = (phi / (2 * np.pi) * 0.2) * np.sin(phi)

psi = np.linspace(0, 2 * np.pi, n)
#beta = np.linspace(0, 5 * 2 * np.pi, n)
x3 = (0.5 * np.abs(np.cos(5 * psi)) + 1) *  np.cos(psi)
y3 = (0.5 * np.abs(np.cos(5 * psi)) + 1) * np.sin(psi)

plt.plot(x1, y1)
plt.plot(x2, y2)
plt.plot(x3, y3)

plt.show()

plt.savefig("hanamaru.pdf")


