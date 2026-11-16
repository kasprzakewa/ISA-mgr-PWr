import math

def optimal_purchasing_strategy():
    n = 6
    K = 10
    xa = 2
    
    c = [4, 3, 5, 3, 4, 2]
    v = [6, 7, 4, 2, 4, 3]
    
    phi = [[0] * (K + 1) for _ in range(n + 1)]
    u_star = [[None] * (K + 1) for _ in range(n + 1)]
    
    for j in range(n - 1, -1, -1): 
        for x_prev in range(K + 1):
            
            if j == 0 and x_prev != xa:
                continue
                
            min_cost = math.inf
            best_u = None
            
            min_u = max(0, v[j] - x_prev)
            max_u = K - x_prev
            
            for u in range(min_u, max_u + 1):
                c_new = c[j] * u
                x_new = x_prev + u - v[j]
                
                c_total = c_new + phi[j + 1][x_new]
                
                if c_total < min_cost:
                    min_cost = c_total
                    best_u = u
            
            if best_u is not None:
                phi[j][x_prev] = min_cost
                u_star[j][x_prev] = best_u

    optimal_purchase = []
    warehouse_state = [xa]
    
    curr_state = xa
    
    for j in range(n):
        best_choice = u_star[j][curr_state]
        optimal_purchase.append(best_choice)
        
        curr_state = curr_state + best_choice - v[j]
        warehouse_state.append(curr_state)

    print(f"Minimalny koszt całkowity: {phi[0][xa]}")
    print(f"Optymalna strategia zakupów (u1...u6): {optimal_purchase}")
    print(f"Przewidywane stany magazynu (x0...x6): {warehouse_state}")
    print()
    print("phi:")
    print(phi)
    print("u_star:")
    print(u_star)

optimal_purchasing_strategy()