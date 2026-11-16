"""
Rozwiazanie ukladu Lorenza metoda ode45 (RK45).

Uklad:
    x' = sigma*(y - x)
    y' = r*x - y - x*z
    z' = x*y - b*z

Parametry: sigma=10, b=8/3, r=0.5
Warunki poczatkowe: x0=0.00001, y0=0, z0=0
Przedział czasu: t in [0, 50]
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# parametry
sigma = 10.0
b     = 8.0 / 3.0
r     = 0.5

def lorenz(t, state):
    x, y, z = state
    return [
        sigma * (y - x),
        r * x - y - x * z,
        x * y - b * z,
    ]

# warunki poczatkowe i przedział czasu
y0     = [0.00001, 0.0, 0.0]
t_span = (0, 50)
t_eval = np.linspace(0, 50, 10000)

# rozwiazanie (RK45 - odpowiednik ode45 z MATLABa)
sol = solve_ivp(lorenz, t_span, y0, method='RK45',
                t_eval=t_eval, rtol=1e-15, atol=1e-15)

# verify the solution converged to equilibrium point
equilibrium_point = [0.0, 0.0, 0.0]
delta = np.abs(sol.y[0][-1] - equilibrium_point[0])
print(f"Delta: {delta}")

print(f"Solver: {sol.message}")
print(f"Liczba krokow: {sol.t.shape[0]}")

# wykresy x(t), y(t), z(t)
fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

labels = ['x(t)', 'y(t)', 'z(t)']
colors = ['tab:blue', 'tab:orange', 'tab:green']

for i in range(3):
    axes[i].plot(sol.t, sol.y[i], color=colors[i], lw=0.8)
    axes[i].set_ylabel(labels[i])
    axes[i].grid(True, alpha=0.3)

axes[2].set_xlabel('t')
fig.suptitle(
    f'Uklad Lorenza (sigma={sigma}, b={b:.4f}, r={r})\n'
    f'IC: x0={y0[0]}, y0={y0[1]}, z0={y0[2]},  t in [0, 50]',
    fontsize=11
)
plt.tight_layout()
plt.savefig('lorenz_ode45.png', dpi=150)
print("Wykres zapisano: lorenz_ode45.png")
plt.show()

# plot trajectory in 3d
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(sol.y[0], sol.y[1], sol.y[2])
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.view_init(elev=30, azim=45)
plt.savefig('lorenz_3d.png', dpi=150)
print("Wykres zapisano: lorenz_3d.png")
plt.show()