#ifndef TSP_UTILS_HPP
#define TSP_UTILS_HPP

#include "tsp_types.hpp"
#include <string>

/**
 * @file tsp_utils.hpp
 * @brief Deklaracje funkcji pomocniczych.
 */

/**
 * @brief Wczytuje dane problemu z pliku JSON.
 * @param filename Ścieżka do pliku wejściowego.
 * @param data Struktura, do której zostaną zapisane dane.
 * @return `true` jeśli wczytanie i parsowanie zakończyło się powodzeniem.
 * * @par Wymagany format JSON
 * Plik musi zawierać następujące klucze:
 * @code{.json}
 * {
 * "n": 20,              // Liczba miast (int)
 * "c_matrix": [[...]],  // Macierz odległości NxN (double)
 * "t_matrix": [[...]],  // Macierz czasów NxN (double)
 * "t_windows": [        // Tablica okien czasowych Nx2
 * [0.0, 1000.0],    // [start, koniec] dla miasta 0
 * [10.5, 20.0]      // ... dla miasta 1
 * ],
 * "a": 0.5,             // Parametr paliwa liniowy (double)
 * "b": 0.01,            // Parametr paliwa kwadratowy (double)
 * "M": 10000            // Stała Big M (double)
 * }
 * @endcode
 */
bool LoadData(const std::string &filename, ProblemData &data);

/**
 * @brief Oblicza koszt paliwa dla odcinka o zadanej długości.
 *
 * Typowo: $f = a \cdot d + b \cdot d^2$.
 *
 * @param distance Długość odcinka.
 * @param a Parametr liniowy.
 * @param b Parametr kwadratowy.
 * @return Koszt paliwa.
 */
double CalcFuelCost(double distance, double a, double b);

/**
 * @brief Wylicza koszt trasy (odległość + paliwo + kara za okna czasowe).
 * @param data Dane problemu.
 * @param route Trasa (sekwencja indeksów miast).
 * @return Wartość funkcji celu dla trasy.
 */
double EvaluateSolution(const ProblemData &data, const std::vector<int> &route);

#endif