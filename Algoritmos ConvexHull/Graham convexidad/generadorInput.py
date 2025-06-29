import numpy as np

with open("input", "w", encoding="utf-8") as f:
    f.write("500\n")
    for i in range(500):
        f.write(f"{np.random.randint(0, 500)} {np.random.randint(0, 500)}\n")
    

import matplotlib.pyplot as plt

points = []
with open("input", "r", encoding="utf-8") as f:
    n = int(f.readline())
    for _ in range(n):
        x, y = map(int, f.readline().split())
        points.append((x, y))

xs, ys = zip(*points)
plt.figure(figsize=(6, 6))
plt.scatter(xs, ys, s=10)
plt.title("Nube de 500 puntos")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.savefig("nube.png")
plt.close()