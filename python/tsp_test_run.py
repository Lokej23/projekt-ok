import os
import sys
import subprocess
import json
import argparse
from tsp_utils import loadJson, eprint, runCommand

def loadResult(path):
    if not os.path.exists(path):
        return None
    
    data = loadJson(path)
    return {
        "time": data.get("execution_time", 0.0),
        "cost": data.get("total_cost", 0.0),
        "is_valid": data.get("is_valid", False)
    }

def runTest(args):
    
    os.makedirs(args.data, exist_ok=True)
    os.makedirs(args.output, exist_ok=True)
    
    test_data = []

    eprint(f"--- ROZPOCZĘCIE TESTU (Max N: {args.max_n}) ---")

    for n in range(5, args.max_n + 1, args.step):
        eprint(f"[n={n}] ...")

        record = {
            "n": n,
            "greedy_det": {},
            "greedy_rand": {},
            "sa": {}
        }

        input_file = os.path.join(args.data, f"test_n{n}.json")
        cmd_gen = ["python3", args.gen_script, "-n", str(n), "-o", input_file]
        runCommand(cmd_gen)

        out_greedy_det = os.path.join(args.output, f"result_n{n}_greedy_det.json")
        out_greedy_rand = os.path.join(args.output, f"result_n{n}_greedy_rand.json")
        out_sa = os.path.join(args.output, f"result_n{n}_sa.json")

        cmd_gd = [args.bin, "-d", input_file, "-o", out_greedy_det, "--greedy", 
                  "-k", "1", "--iterations", "1"]
        runCommand(cmd_gd)
        record["greedy_det"] = loadResult(out_greedy_det)

        cmd_gr = [args.bin, "-d", input_file, "-o", out_greedy_rand, "--greedy", 
                  "--iterations", str(args.iterations), "-k", "4"]
        runCommand(cmd_gr)
        record["greedy_rand"] = loadResult(out_greedy_rand)

        cmd_sa = [args.bin, "-d", input_file, "-o", out_sa, "--sa", 
                  "--iterations", str(args.iterations), "-T", "5000", "-c", "0.99"]
        runCommand(cmd_sa)
        record["sa"] = loadResult(out_sa)
        
        test_data.append(record)
        eprint(f"   -> Zakończono n={n}")

    eprint("--- ZAPISYWANIE WYNIKÓW ---")
    
    with open(args.summary_file, 'w') as f:
        json.dump(test_data, f, indent=4)
        
    eprint(f"Pełny wynik testu zapisano do pliku: {args.summary_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatyzacja testów TSP: Generowanie -> Obliczenia -> JSON")

    parser.add_argument("--bin", required=True, help="Ścieżka do pliku wykonywalnego C++")
    parser.add_argument("--gen-script", default="tsp_gen.py", help="Ścieżka do skryptu generującego")
    parser.add_argument("--max-n", type=int, default=50, help="Maksymalna liczba miast (n)")
    parser.add_argument("--step", type=int, default=5, help="Krok zwiększania n")
    parser.add_argument("-d", "--data", default="data_test", help="Katalog na wygenerowane dane")
    parser.add_argument("-o", "--output", default="results_test", help="Katalog na wyniki poszczególnych uruchomień")
    parser.add_argument("--summary-file", default="test_summary.json", help="Plik końcowy z wynikami")
    parser.add_argument("-i", "--iterations", type=int, default=1000, help="Liczba iteracji")

    args = parser.parse_args()
    runTest(args)