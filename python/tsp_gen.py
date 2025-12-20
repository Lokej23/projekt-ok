import json
import random
import math
import argparse
from tsp_utils import eprint

def checkJson(name: str) -> str:
    if not name.lower().endswith(".json"):
        return name + ".json"
    return name

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def generateData(n_cities, filename, no_fuel=False, no_time=False):
    width, height = 100, 100
    coords = []
    
    for _ in range(n_cities):
        coords.append((random.uniform(0, width), random.uniform(0, height)))
    
    c_matrix = [] # odległości
    t_matrix = [] # czas
    
    speed = 1.0 # d/t
    
    for i in range(n_cities):
        row_c = []
        row_t = []
        for j in range(n_cities):
            if i == j:
                d = 0
                t = 0
            else:
                d = distance(coords[i], coords[j])
                t = (d / speed)
            row_c.append(round(d, 2))
            row_t.append(round(t, 2))
        c_matrix.append(row_c)
        t_matrix.append(row_t)

    t_windows = []
    horizon = n_cities * 20 # przybliżony czas na odwiedzenie wszystkich miast
    
    for i in range(n_cities):
        if no_time:
            t_windows.append([0, horizon * 100])
        else:
            if i == 0:
                t_windows.append([0, horizon]) # baza ma najszersze okno czasowe aby dało się odwiedzić wszystkie miasta
            else:
                start = random.uniform(0, horizon * 0.7)
                duration = random.uniform(10, 30)
                t_windows.append([round(start, 2), round(start + duration, 2)])

    if no_fuel:
        a = 0.0
        b = 0.0
    else:
        a = 0.5
        b = 0.01

    data = {
        "n": n_cities,
        "c_matrix": c_matrix, # c_ij
        "t_matrix": t_matrix, # t_ij
        "t_windows": t_windows, # [e_i, l_i]
        "a": a, # paliwo liniowy
        "b": b, # paliwo kwadratowy
        "M": 10000 # stała
    }

    filename = checkJson(filename)
    path = filename
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
    
    eprint(f"Wygenerowano plik {path} dla {n_cities} miast.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Data for TSP problem")
    parser.add_argument("-n", "--n-cities", type=int, default=20, help="Number of cities")
    parser.add_argument("-o", "--output", type=str, default="tsp_data.json", help="Output file name")
    
    parser.add_argument("--no-fuel", action="store_true", help="Generate data without fuel constraints")
    parser.add_argument("--no-time", action="store_true", help="Generate data without time constraints")
    args = parser.parse_args()
    generateData(args.n_cities, args.output, args.no_fuel, args.no_time)
