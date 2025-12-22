import matplotlib.pyplot as plt
import argparse
import os
from tsp_utils import eprint, loadJson

def plotCharts(json_file, output_dir):
    if not os.path.exists(json_file):
        eprint(f"Błąd: Nie znaleziono pliku {json_file}")
        return

    data = loadJson(json_file)
    data.sort(key=lambda x: x['n'])

    ns = [d['n'] for d in data]
    
    time_gd = [d['greedy_det']['time'] for d in data]
    time_gr = [d['greedy_rand']['time'] for d in data]
    time_sa = [d['sa']['time'] for d in data]

    cost_gd = [d['greedy_det']['cost'] for d in data]
    cost_gr = [d['greedy_rand']['cost'] for d in data]
    cost_sa = [d['sa']['cost'] for d in data]

    plt.style.use('seaborn-v0_8-whitegrid')

    # Czas obliczeń (Skala liniowa)
    plt.figure(figsize=(10, 6))
    plt.plot(ns, time_gd, 'o-', label='Zachłanny Deterministyczny')
    plt.plot(ns, time_gr, 's-', label='Zachłanny Ulosowiony')
    plt.plot(ns, time_sa, '^-', label='Symulowane Wyżarzanie')
    plt.xlabel('Liczba miast (n)')
    plt.ylabel('Czas wykonania [s]')
    plt.title('Złożoność czasowa algorytmów')
    plt.legend()
    plt.savefig(os.path.join(output_dir, "wykres_czas_lin.png"))
    plt.close()

    # Czas obliczeń (Skala logarytmiczna)
    plt.figure(figsize=(10, 6))
    plt.plot(ns, time_gd, 'o-', label='Zachłanny Deterministyczny')
    plt.plot(ns, time_gr, 's-', label='Zachłanny Ulosowiony')
    plt.plot(ns, time_sa, '^-', label='Symulowane Wyżarzanie')
    plt.xlabel('Liczba miast (n)')
    plt.ylabel('Czas wykonania [s] (log)')
    plt.yscale('log')
    plt.title('Złożoność czasowa (skala logarytmiczna)')
    plt.legend()
    plt.savefig(os.path.join(output_dir, "wykres_czas_log.png"))
    plt.close()

    # Jakość rozwiązań
    plt.figure(figsize=(10, 6))
    plt.plot(ns, cost_gd, 'o--', label='Zachłanny Deterministyczny', alpha=0.7)
    plt.plot(ns, cost_gr, 's-', label='Zachłanny Ulosowiony')
    plt.plot(ns, cost_sa, '^-', label='Symulowane Wyżarzanie', linewidth=2)
    plt.xlabel('Liczba miast (n)')
    plt.ylabel('Całkowity koszt trasy')
    plt.title('Porównanie jakości rozwiązań')
    plt.legend()
    plt.savefig(os.path.join(output_dir, "wykres_jakosc.png"))
    plt.close()

    eprint(f"Wygenerowano 3 wykresy w katalogu: {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generowanie wykresów z wyników JSON")
    parser.add_argument("-d", "--data", required=True, help="Plik JSON z wynikami zbiorczymi")
    parser.add_argument("-o", "--output-dir", default=".", help="Katalog wyjściowy na obrazki")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    plotCharts(args.data, args.output_dir)