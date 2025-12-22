# Algorytm napisany przy użyciu Gemini Pro 3
import json
import math
import sys

def nint(x):
    """Standardowa funkcja zaokrąglania TSPLIB do najbliższej liczby całkowitej."""
    return int(x + 0.5)

def dist_euc_2d(c1, c2):
    """Oblicza odległość Euklidesową (płaską)."""
    xd = c1[0] - c2[0]
    yd = c1[1] - c2[1]
    # Wg standardu TSPLIB odległości są często zaokrąglane do całkowitych
    return nint(math.sqrt(xd*xd + yd*yd))

def dist_geo(c1, c2):
    """Oblicza odległość Geograficzną (dla problemów typu Ulysses16)."""
    # Konwersja ze stopni na radiany wg specyfikacji TSPLIB
    def to_rad(x):
        deg = int(x)
        min_val = x - deg
        return math.pi * (deg + 5.0 * min_val / 3.0) / 180.0

    lat1, lon1 = to_rad(c1[0]), to_rad(c1[1])
    lat2, lon2 = to_rad(c2[0]), to_rad(c2[1])
    
    RRR = 6378.388 # Promień Ziemi
    
    q1 = math.cos(lon1 - lon2)
    q2 = math.cos(lat1 - lat2)
    q3 = math.cos(lat1 + lat2)
    
    return int(RRR * math.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)

def convert_tsp_to_json(tsp_filename, json_filename):
    coords = []
    edge_weight_type = "EUC_2D" # Domyślny
    dimension = 0

    print(f"Konwertowanie {tsp_filename}...")

    with open(tsp_filename, 'r') as f:
        lines = f.readlines()
        
        in_coord_section = False
        
        for line in lines:
            line = line.strip()
            if not line or line == "EOF":
                continue
            
            if line.startswith("EDGE_WEIGHT_TYPE"):
                parts = line.split(":")
                edge_weight_type = parts[1].strip()
            
            elif line.startswith("DIMENSION"):
                parts = line.split(":")
                dimension = int(parts[1].strip())

            elif line.startswith("NODE_COORD_SECTION"):
                in_coord_section = True
                continue
            
            elif in_coord_section:
                # Format: ID X Y
                parts = line.split()
                if len(parts) >= 3:
                    # Ignorujemy ID (parts[0]), bierzemy X i Y
                    try:
                        x = float(parts[1])
                        y = float(parts[2])
                        coords.append((x, y))
                    except ValueError:
                        continue

    if len(coords) != dimension:
        print(f"Uwaga: Oczekiwano {dimension} miast, wczytano {len(coords)}.")
        dimension = len(coords)

    # Budowanie macierzy
    c_matrix = []
    t_matrix = []
    
    for i in range(dimension):
        row_c = []
        row_t = []
        for j in range(dimension):
            if i == j:
                d = 0.0
            else:
                if edge_weight_type == "GEO":
                    d = float(dist_geo(coords[i], coords[j]))
                else:
                    # Domyślnie EUC_2D
                    d = float(dist_euc_2d(coords[i], coords[j]))
            
            row_c.append(d)
            row_t.append(d) # Zakładamy prędkość 1.0
        c_matrix.append(row_c)
        t_matrix.append(row_t)

    # Generowanie danych "dummy" dla Twojego specyficznego solvera
    # Wyłączamy paliwo i okna czasowe
    t_windows = [[0.0, 1000000.0] for _ in range(dimension)]
    
    data = {
        "n": dimension,
        "c_matrix": c_matrix,
        "t_matrix": t_matrix,
        "t_windows": t_windows,
        "a": 0.0,
        "b": 0.0,
        "M": 10000
    }

    with open(json_filename, 'w') as f:
        json.dump(data, f, indent=4)
        
    print(f"Gotowe! Zapisano jako {json_filename}")
    print(f"Typ odległości: {edge_weight_type}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Użycie: python tsplib_to_json.py <plik.tsp>")
    else:
        input_file = sys.argv[1]
        output_file = input_file.replace(".tsp", ".json")
        if output_file == input_file:
             output_file += ".json"
        
        convert_tsp_to_json(input_file, output_file)