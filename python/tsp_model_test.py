import os
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
        "is_valid": data.get("is_valid", False),
        "status": data.get("status", "UNKNOWN")
    }

def runTest(args):
    os.makedirs(args.data, exist_ok=True)
    os.makedirs(args.output, exist_ok=True)

    test_data = []

    eprint(f"--- ROZPOCZĘCIE TESTU MINIZINC (Max N: {args.max_n}) ---")

    for n in range(0, args.max_n + 1, args.step):
        eprint(f"[n={n}] ...")

        record = {
            "n": n,
            "minizinc": {}
        }

        input_file = os.path.join(args.data, f"test_n{n}.json")
        cmd_gen = ["python3", args.gen_script, "-n", str(n), "-o", input_file]
        runCommand(cmd_gen)

        out_mzn = os.path.join(args.output, f"result_n{n}_mzn.json")
        cmd_mzn = [
            "python3", args.model_script,
            "-m", args.model,
            "-d", input_file,
            "-o", out_mzn,
            "-s", args.solver,
            "-t", str(args.timeout)
        ]
        runCommand(cmd_mzn)

        record["minizinc"] = loadResult(out_mzn)
        test_data.append(record)

        eprint(f"   -> Zakończono n={n}")

    eprint("--- ZAPISYWANIE WYNIKÓW ---")

    with open(args.summary_file, 'w') as f:
        json.dump(test_data, f, indent=4)

    eprint(f"Pełny wynik testu zapisano do pliku: {args.summary_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test czasu działania modelu MiniZinc (TSP)")

    parser.add_argument("-m", "--model", required=True, help="Ścieżka do pliku modelu (.mzn)")
    parser.add_argument("--model-script", default="tsp_model_run.py", help="Skrypt uruchamiający MiniZinc")
    parser.add_argument("-s", "--solver", default="coin-bc", help="Nazwa solvera (domyślnie: coin-bc)")
    parser.add_argument("-t", "--timeout", type=int, default=120, help="Limit czasu w sekundach (domyślnie: 120)")

    parser.add_argument("--gen-script", default="tsp_gen.py", help="Skrypt generujący dane")
    parser.add_argument("--max-n", type=int, default=50, help="Maksymalna liczba miast (n)")
    parser.add_argument("--step", type=int, default=5, help="Krok zwiększania n")
    parser.add_argument("-d", "--data", default="data_test", help="Katalog na wygenerowane dane")
    parser.add_argument("-o", "--output", default="results_mzn", help="Katalog na wyniki poszczególnych uruchomień")
    parser.add_argument("--summary-file", default="test_summary_mzn.json", help="Plik końcowy z wynikami")

    args = parser.parse_args()
    runTest(args)
