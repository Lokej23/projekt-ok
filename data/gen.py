import json
import random
import math
import argparse

def checkJson(name: str) -> str:
    if not name.lower().endswith(".json"):
        return name + ".json"
    return name

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def generate_data(n_cities, filename):
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
        if i == 0:
            t_windows.append([0, horizon]) # baza ma najszersze okno czasowe aby dało się odwiedzić wszystkie miasta
        else:
            start = random.uniform(0, horizon * 0.7)
            duration = random.uniform(10, 30)
            t_windows.append([round(start, 2), round(start + duration, 2)])

    data = {
        "n": n_cities,
        "c_matrix": c_matrix, # c_ij
        "t_matrix": t_matrix, # t_ij
        "t_windows": t_windows, # [e_i, l_i]
        "a": 0.5, # paliwo liniowy
        "b": 0.01, # paliwo kwadratowy
        "M": 10000 # stała
    }

    filename = checkJson(filename)
    path = "data/" + filename
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Wygenerowano plik {path} dla {n_cities} miast.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Data for TSP problem")
    parser.add_argument("-n", "--n-cities", type=int, default=20, help="Number of cities")
    parser.add_argument("-o", "--output", type=str, default="tsp_data.json", help="Output file name")
    args = parser.parse_args()
    generate_data(args.n_cities, args.output)
