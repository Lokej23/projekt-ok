import argparse
from tsp_utils import eprint, loadJson, calcFuelCost


def validateSolution(data_path, solution_path):
    eprint(f"--- WALIDATOR TSP ---")
    eprint(f"Dane: {data_path}")
    eprint(f"Rozwiązanie: {solution_path}")

    data = loadJson(data_path) 
    sol = loadJson(solution_path)

    n = data['n']
    c_matrix = data['c_matrix']
    t_matrix = data['t_matrix']
    windows = data['t_windows']
    a = data['a']
    b = data['b']
    
    route = sol['route']
    reported_cost = sol['total_cost']

    errors = []

    # Weryfikacja struktury trasy
    
    # Sprawdzenie długości
    if len(route) != n + 1:
        errors.append(f"Długość trasy wynosi {len(route)}, oczekiwano {n + 1}.")
    
    # Sprawdzenie startu i końca
    if route[0] != 0 or route[-1] != 0:
        errors.append("Trasa musi zaczynać się i kończyć w wierzchołku 0.")

    # Sprawdzenie czy odwiedzono wszystkie miasta 0..n-1
    unique_cities = set(route)
    if len(unique_cities) != n:
        missing = set(range(n)) - unique_cities
        errors.append(f"Nie odwiedzono wszystkich miast. Brakujące: {missing}")
    
    if len(route) > 1 and len(set(route[:-1])) != len(route[:-1]):
         errors.append("W trasie występują powtórzenia miast (nie licząc powrotu do bazy).")

    if errors:
        eprint(f"[BŁĄD STRUKTURY TRASY]")
        for e in errors:
            eprint(f"- {e}")
        return False

    # Symulacja trasy
    calculated_cost = 0.0
    current_time = 0.0
    
    eprint("--- Symulacja Przejścia ---")
    eprint(f"{'Odcinek':<15} | {'Dyst.':<8} | {'Paliwo':<8} | {'Przyjazd':<10} | {'Okno':<15} | {'Kara':<8}")
    eprint("-" * 80)

    for i in range(len(route) - 1):
        u = route[i]
        v = route[i+1]

        dist = c_matrix[u][v]
        travel_time = t_matrix[u][v]
        
        fuel = calcFuelCost(dist, a, b)
        step_cost = dist + fuel
        
        arrival_time = current_time + travel_time
        
        e_v = windows[v][0]
        l_v = windows[v][1]
        
        wait_time = 0.0
        penalty = 0.0
        
        actual_arrival = arrival_time
        
        # Przyjazd za wcześnie
        if actual_arrival < e_v:
            wait_time = e_v - actual_arrival
            actual_arrival = e_v
        
        # Przyjazd za późno
        if actual_arrival > l_v:
            penalty = actual_arrival - l_v
        
        calculated_cost += step_cost + penalty
        
        win_str = f"[{e_v:.1f}, {l_v:.1f}]"
        eprint(f"{u:>3} -> {v:<3}     | {dist:<8.2f} | {fuel:<8.2f} | {actual_arrival:<10.2f} | {win_str:<15} | {penalty:<8.2f}")

        current_time = actual_arrival

    eprint("-" * 80)

    # Porównanie wyników
    diff = abs(calculated_cost - reported_cost)
    epsilon = 0.05 # Tolerancja na błędy zmiennoprzecinkowe

    eprint(f"Koszt zgłoszony w pliku:   {reported_cost:.4f}")
    eprint(f"Koszt obliczony przez walidator: {calculated_cost:.4f}")
    eprint(f"Różnica: {diff:.6f}")

    if diff < epsilon:
        eprint(f"=== WERYFIKACJA POZYTYWNA (OK) ===")
        return True
    else:
        eprint(f"=== WERYFIKACJA NEGATYWNA (BŁĄD KOSZTÓW) ===")
        eprint(f"Rozbieżność przekracza tolerancję ({epsilon}).")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validator dla problemu TSP z ograniczeniami czasu i paliwa.")
    parser.add_argument("-d", "--data", required=True, help="Plik JSON z danymi wejściowymi")
    parser.add_argument("-s", "--solution", required=True, help="Plik JSON z rozwiązaniem")
    
    args = parser.parse_args()
    
    if (validateSolution(args.data, args.solution)):
        exit(0)
    else:
        exit(1)
