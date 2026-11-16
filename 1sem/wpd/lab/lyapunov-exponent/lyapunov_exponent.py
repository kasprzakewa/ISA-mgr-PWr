import csv
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Parametr masowy układu Ziemia-Księżyc
mu = 0.01215

# Funkcja obliczająca odległości od mas głównych
def get_distances(x, y, mu):
    r1 = np.sqrt((x + mu)**2 + y**2)
    r2 = np.sqrt((x - 1 + mu)**2 + y**2)
    return r1, r2

# Równania ruchu PCR3BP + równania wariacyjne
def pcr3bp_lyapunov(t, state):
    # Rozpakowanie stanu: pierwsze 4 to położenie/prędkość, kolejne 4 to perturbacja
    x, y, vx, vy = state[0:4]
    dx, dy, dvx, dvy = state[4:8]
    
    r1, r2 = get_distances(x, y, mu)
    
    # 1. Równania ruchu (nieliniowe)
    x_dot = vx
    y_dot = vy
    vx_dot = 2*vy + x - ((1-mu)*(x+mu))/r1**3 - (mu*(x-1+mu))/r2**3
    vy_dot = -2*vx + y - ((1-mu)*y)/r1**3 - (mu*y)/r2**3
    
    # 2. Elementy macierzy Jacobiego układu
    # (Pochodne cząstkowe sił względem x i y)
    U_xx = 1 - (1-mu)*(1/r1**3 - 3*(x+mu)**2/r1**5) - mu*(1/r2**3 - 3*(x-1+mu)**2/r2**5)
    U_yy = 1 - (1-mu)*(1/r1**3 - 3*y**2/r1**5) - mu*(1/r2**3 - 3*y**2/r2**5)
    U_xy = 3*(1-mu)*(x+mu)*y/r1**5 + 3*mu*(x-1+mu)*y/r2**5
    
    # 3. Równania wariacyjne (liniowe dla perturbacji)
    dx_dot = dvx
    dy_dot = dvy
    dvx_dot = U_xx * dx + U_xy * dy + 2 * dvy
    dvy_dot = U_xy * dx + U_yy * dy - 2 * dvx
    
    return np.array([x_dot, y_dot, vx_dot, vy_dot, dx_dot, dy_dot, dvx_dot, dvy_dot])

# ---- PARAMETRY SYMULACJI ----
T_total = 100.0       # Całkowity czas symulacji (w jednostkach bezwymiarowych)
dt = 0.1             # Krok renormalizacji
steps = int(T_total / dt)

# Warunki początkowe blisko punktu Lagrange'a (obszar potencjalnie chaotyczny)
# Przyjmujemy zlinearyzowany stan blisko L1 z Twojej pracy
state = np.array([0.836, 0.0, 0.0, 0.01]) 

# Inicjalizacja małego wektora perturbacji (norma = 1)
perturbation = np.array([1.0, 0.0, 0.0, 0.0])
state = np.concatenate((state, perturbation))

lyapunov_sum = 0.0
lyapunov_exponents = []
time_array = []

# Pętla całkująca z renormalizacją
for i in range(steps):
    t_span = [i*dt, (i+1)*dt]
    
    # Całkowanie układu
    sol = solve_ivp(pcr3bp_lyapunov, t_span, state, method='RK45', rtol=1e-9, atol=1e-9)
    
    # Aktualizacja wektora stanu po kroku dt
    state = sol.y[:, -1]
    
    # Wektor perturbacji po ewolucji
    delta_X = state[4:8]
    
    # Obliczenie normy i logarytmu do MLE
    norm_delta = np.linalg.norm(delta_X)
    lyapunov_sum += np.log(norm_delta)
    
    # Renormalizacja perturbacji, aby uniknąć przepełnienia numerycznego
    state[4:8] = delta_X / norm_delta
    
    # Obliczanie aktualnego MLE średniego w czasie
    current_time = (i+1)*dt
    current_mle = lyapunov_sum / current_time
    
    lyapunov_exponents.append(current_mle)
    time_array.append(current_time)

# Wynik końcowy
final_mle = lyapunov_exponents[-1]
print(f"Oszacowany największy wykładnik Lapunowa (MLE): {final_mle:.5f}")

# Zapis danych do pliku CSV
csv_filename = "lyapunov_exponents.csv"
with open(csv_filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["czas", "MLE"])
    writer.writerows(zip(time_array, lyapunov_exponents))
print(f"Dane zapisane do pliku: {csv_filename}")

# Wygenerowanie wykresu zbieżności MLE
plt.figure(figsize=(8, 4))
plt.plot(time_array, lyapunov_exponents, color='limegreen', label=f"MLE(t)  [końcowa wartość: {final_mle:.5f}]")
plt.axhline(0, color='magenta', linestyle='--', label="MLE = 0 (granica chaosu)")
plt.title(f"Zbieżność największego wykładnika Lapunowa (t = {T_total}, perturbacja = {perturbation[0]})")
plt.xlabel("Czas (jednostki bezwymiarowe)")
plt.ylabel("MLE (\u03BB)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("lyapunov_exponents.png")
plt.show()