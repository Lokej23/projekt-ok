import minizinc
import json
import argparse
import os
from datetime import timedelta
from tsp_utils import eprint 

def reconstructRoute(x_matrix, start_node=0):
    n = len(x_matrix)
    route = [start_node]
    current = start_node
    
    visited_count = 0
    
    while True:
        next_city = -1
        for j in range(n):
            val = x_matrix[current][j]
            if val == 1 or val is True:
                next_city = j
                break
        
        if next_city == -1:
            break
            
        route.append(next_city)
        current = next_city
        visited_count += 1
        
        if current == start_node:
            break
            
        if visited_count > n + 1:
            break

    return route

def solveTspMinizinc(model_path, data_path, solver_name, timeout_sec, output_path):
    eprint(f"Model:   {model_path}")
    eprint(f"Dane:    {data_path}")
    eprint(f"Wynik:   {output_path}")
    eprint(f"Solver:  {solver_name}")
    eprint(f"Timeout: {timeout_sec}s")
    eprint(f"--------------------")

    solver = minizinc.Solver.lookup(solver_name)

    model = minizinc.Model(model_path)
    instance = minizinc.Instance(solver, model)

    with open(data_path, 'r') as f:
        data = json.load(f)

    instance["n"] = data["n"]
    instance["c_matrix"] = data["c_matrix"]
    instance["t_matrix"] = data["t_matrix"]
    instance["t_windows"] = data["t_windows"]
    instance["a"] = data["a"]
    instance["b"] = data["b"]
    instance["M"] = data["M"]

    eprint("Rozpoczynanie obliczeń...")

    result = instance.solve(timeout=timedelta(seconds=timeout_sec))

    output_data = {
        "execution_time": 0.0,
        "is_valid": False,
        "route": [],
        "total_cost": float('inf'),
        "status": str(result.status)
    }

    if result.status == minizinc.Status.OPTIMAL_SOLUTION or result.status == minizinc.Status.SATISFIED:
        eprint("=== WYNIK ===")
        eprint(f"Status: {result.status}")
        eprint(f"Koszt całkowity: {result.objective}")
        
        output_data["total_cost"] = result.objective
        output_data["is_valid"] = True
        
        x_matrix = result["x"]
        route = reconstructRoute(x_matrix)
        output_data["route"] = route
        
        time_stat = result.statistics.get('solveTime')
        if time_stat:
            seconds = time_stat.total_seconds()
            output_data["execution_time"] = seconds
            eprint(f"Czas obliczeń: {seconds:.4f}s")
            
    elif result.status == minizinc.Status.UNSATISFIABLE:
        eprint("=== WYNIK: UNSATISFIABLE ===")
        eprint("Nie znaleziono rozwiązania.")
        output_data["is_valid"] = False
        
    elif result.status == minizinc.Status.UNKNOWN:
        eprint("=== WYNIK: UNKNOWN ===")
        eprint("Upłynął limit czasu.")
        output_data["is_valid"] = False
    else:
        eprint(f"Status końcowy: {result.status}")

    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=4)
        eprint(f"Zapisano wyniki do pliku: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Uruchom model MiniZinc TSP.")
    
    parser.add_argument("-m", "--model", type=str, required=True, help="Ścieżka do pliku modelu (.mzn)")
    parser.add_argument("-d", "--data", type=str, required=True, help="Ścieżka do pliku danych (.json)")    
    parser.add_argument("-o", "--output", type=str, help="Ścieżka do pliku wyjściowego JSON")
    parser.add_argument("-s", "--solver", type=str, default="coin-bc", help="Nazwa solvera (domyślnie: coin-bc)")
    parser.add_argument("-t", "--timeout", type=int, default=120, help="Limit czasu w sekundach (domyślnie: 120)")

    args = parser.parse_args()

    if args.output:
        output_file = args.output
    else:
        base_name = os.path.splitext(args.data)[0]
        output_file = f"{base_name}_result_mzn.json"

    solveTspMinizinc(args.model, args.data, args.solver, args.timeout, output_file)