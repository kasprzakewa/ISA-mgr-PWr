import sympy as sp

# parametry i zmienne
sigma = sp.Rational(10)
b     = sp.Rational(8, 3)
r_val = sp.Rational(1, 2)

x, y, z = sp.symbols('x y z')

f = sigma * (y - x)
g = r_val * x - y - x * z
h = x * y - b * z

# punkty rownowagi
print("=" * 56)
print("PUNKTY ROWNOWAGI")
print("=" * 56)

equilibria_all = sp.solve([f, g, h], [x, y, z], dict=True)

# rzeczywiste punkty rownowagi
equilibria = [
    eq for eq in equilibria_all
    if all(v.is_real for v in eq.values())
]

print(f"\nWszystkie rozwiazania (w tym zespolone): {len(equilibria_all)}")
for i, eq in enumerate(equilibria_all):
    print(f"  {eq}")

print(f"\nRzeczywiste punkty rownowagi: {len(equilibria)}")
for i, eq in enumerate(equilibria):
    print(f"  E{i} = {eq}")

# macierz Jacobiego
print("\n" + "=" * 56)
print("MACIERZ JACOBIEGO")
print("=" * 56)

J = sp.Matrix([
    [sp.diff(f, x), sp.diff(f, y), sp.diff(f, z)],
    [sp.diff(g, x), sp.diff(g, y), sp.diff(g, z)],
    [sp.diff(h, x), sp.diff(h, y), sp.diff(h, z)],
])
print("\nJ(x, y, z) =")
sp.pprint(J)

# wartosci wlasne i stabilnosc
print("\n" + "=" * 56)
print("WARTOSCI WLASNE I OCENA STABILNOSCI")
print("=" * 56)

lam = sp.Symbol('lambda')

for i, eq in enumerate(equilibria):
    x0, y0, z0 = eq[x], eq[y], eq[z]
    print(f"\n{'-'*50}")
    print(f"Punkt E{i} = ({x0}, {y0}, {z0})")
    print(f"{'-'*50}")

    J0 = J.subs([(x, x0), (y, y0), (z, z0)])
    print("\nJ(E) =")
    sp.pprint(J0)

    # wielomian charakterystyczny
    char_poly = sp.expand(sp.det(J0 - lam * sp.eye(3)))
    print(f"\nWielomian charakterystyczny:")
    print(f"  p(lambda) = {char_poly}")

    # wartości własne (dokładne)
    eigs_sym = J0.eigenvals(multiple=True)
    print(f"\nWartosci wlasne (symboliczne):")
    for j, ev in enumerate(eigs_sym):
        print(f"  lambda{j+1} = {sp.simplify(ev)}")

    # wartosci wlasne (numeryczne)
    eigs_num = [complex(ev.evalf()) for ev in eigs_sym]
    print(f"\nWartosci wlasne (numeryczne):")
    for j, ev in enumerate(eigs_num):
        re, im = ev.real, ev.imag
        if abs(im) < 1e-10:
            print(f"  lambda{j+1} = {re:+.6f}")
        else:
            print(f"  lambda{j+1} = {re:+.6f} {'+' if im>=0 else '-'} {abs(im):.6f}j")

    max_re = max(ev.real for ev in eigs_num)
    print(f"\n  max Re(lambda) = {max_re:.6f}")
    if max_re < -1e-12:
        print(f"  Wszystkie Re(lambda) < 0  ->  E{i} jest ASYMPTOTYCZNIE STABILNY")
    elif abs(max_re) < 1e-12:
        print(f"  Re(lambda_max) ~ 0  ->  metoda linearyzacji nieostateczna")
    else:
        print(f"  Re(lambda_max) > 0  ->  E{i} jest NIESTABILNY")
