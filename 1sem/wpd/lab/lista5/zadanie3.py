import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

x1s, x2s = sp.symbols('x1 x2')

Vs = x1s**2 + x2s**2
dV1 = sp.diff(Vs, x1s)   # 2*x1
dV2 = sp.diff(Vs, x2s)   # 2*x2

sym_cases = [
    ("f na zewnatrz", ( x1s,  x2s)),
    ("f do srodka",   (-x1s, -x2s)),
    ("f styczna",     (-x2s,  x1s)),
]

print("V  =", Vs)
print("nabla V = ({}, {})".format(dV1, dV2))
print("-" * 50)
for name, (f1, f2) in sym_cases:
    Vdot = sp.expand(dV1 * f1 + dV2 * f2)
    print(f"{name}:  f = ({f1}, {f2})")
    print(f"  dV/dt = nabla V * f = {Vdot}")
    print()
print("-" * 50)
print()

plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor':   '#f8f8f8',
    'axes.grid':        True,
    'grid.color':       'white',
    'grid.linewidth':   0.8,
    'font.size':        10,
})

x1 = np.linspace(-8, 8, 300)
x2 = np.linspace(-8, 8, 300)
X1, X2 = np.meshgrid(x1, x2)
V = X1**2 + X2**2

# gradient nabla V = (2*x1, 2*x2)
G1 = 2 * X1
G2 = 2 * X2

# punkty na dwoch okregach
angles = np.linspace(np.pi/8, 2*np.pi + np.pi/8, 8, endpoint=False)
pts = np.array(
    [[r * np.cos(a), r * np.sin(a)] for r in [2.5, 5.5] for a in angles]
)

ARROW = dict(angles='xy', scale_units='xy', scale=1,
             headwidth=4, headlength=5, headaxislength=4.5)

cases = [
    ('f na zewnatrz  (dV/dt > 0)',  '#e05c00',  1,   'niestabilny'),
    ('f do srodka    (dV/dt < 0)',  '#1a7a2e',  -1,  'stabilny asymptotycznie'),
    ('f styczne      (dV/dt = 0)',  '#5c3d9e',   0,  'stabilny (nie asymptotycznie)'),
]

fig, axes = plt.subplots(1, 3, figsize=(15, 5.5))

levels = np.linspace(0, 64, 18)[1:]

for ax, (title, color, mode, verdict) in zip(axes, cases):
    cf = ax.contourf(X1, X2, V, levels=levels, cmap='YlOrBr', alpha=0.55)
    ax.contour(X1, X2, V, levels=levels, colors='#7a5200', linewidths=0.6, alpha=0.6)

    # gradient (cienkie szare strzalki)
    s = 25
    ax.quiver(X1[::s, ::s], X2[::s, ::s], G1[::s, ::s], G2[::s, ::s],
              color='#444444', alpha=0.35, scale=120, width=0.003,
              headwidth=3, headlength=4)

    # wektory f
    for p in pts:
        g = np.array([2*p[0], 2*p[1]])
        g_hat = g / np.linalg.norm(g)
        t_hat = np.array([-g_hat[1], g_hat[0]])  # styczny
        if mode == 1:
            f = g_hat * 1.6
        elif mode == -1:
            f = -g_hat * 1.6
        else:
            f = t_hat * 1.6
        ax.quiver(p[0], p[1], f[0], f[1], color=color,
                  width=0.008, **ARROW)

    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.set_aspect('equal')
    ax.set_xlabel('$x_1$')
    ax.set_ylabel('$x_2$', rotation=0, labelpad=10)
    ax.set_title(title, fontsize=10, color=color, fontweight='bold', pad=6)
    ax.text(0.5, -0.13, f'=> {verdict}',
            ha='center', transform=ax.transAxes,
            fontsize=9, color=color, style='italic')

    # opis rownania
    eq_text = r'$\dot{V} > 0$' if mode == 1 else (r'$\dot{V} < 0$' if mode == -1 else r'$\dot{V} = 0$')
    ax.text(0.97, 0.03, eq_text, ha='right', va='bottom',
            transform=ax.transAxes, fontsize=12, color=color)

# wspolny colorbar
cbar = fig.colorbar(cf, ax=axes, fraction=0.015, pad=0.02)
cbar.set_label('V(x1, x2)', fontsize=9)

# wspolna legenda
from matplotlib.lines import Line2D
handles = [
    Line2D([0], [0], color='#444444', alpha=0.6, linewidth=1.5, label='$\\nabla V$ (gradient)'),
    Line2D([0], [0], color='#e05c00', linewidth=2, label='f na zewnatrz'),
    Line2D([0], [0], color='#1a7a2e', linewidth=2, label='f do srodka'),
    Line2D([0], [0], color='#5c3d9e', linewidth=2, label='f styczna'),
]
fig.legend(handles=handles, loc='upper center', ncol=4,
           fontsize=9, bbox_to_anchor=(0.5, 1.0), framealpha=0.9)

fig.suptitle('V(x1, x2) = x1^2 + x2^2  -  kierunki f(x) wzgledem nabla V',
             fontsize=12, y=1.06)
plt.tight_layout()
plt.savefig('V_kierunki.png', dpi=150, bbox_inches='tight')
print("Wykres zapisano: V_kierunki.png")
plt.show()

# plot 3d
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X1, X2, V, cmap='viridis')
ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('V')
ax.view_init(elev=30, azim=45)
plt.savefig('V_3d.png', dpi=150)
print("Wykres zapisano: V_3d.png")
plt.show()