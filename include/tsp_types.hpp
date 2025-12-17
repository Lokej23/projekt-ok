/**
 * @file tsp_types.hpp
 * @brief Definicje typów dla problemu TSP z ograniczeniami czasu i paliwa.
 */

#ifndef TSP_TYPES_HPP
#define TSP_TYPES_HPP

#include <vector>
#include <string>

/**
 * @brief Dane wejściowe problemu TSP.
 *
 * Zawiera macierze kosztów i czasów podróży, okna czasowe oraz parametry kosztu paliwa.
 */
struct ProblemData
{
    int n;                                          ///< Liczba miast.
    std::vector<std::vector<double>> c_matrix;      ///< Macierz odległości/kosztów $c_{ij}$.
    std::vector<std::vector<double>> t_matrix;      ///< Macierz czasów przejazdu $t_{ij}$.
    std::vector<std::pair<double, double>> windows; ///< Okna czasowe $[e_i, l_i]$.
    double a;                                       ///< Parametr liniowy kosztu paliwa.
    double b;                                       ///< Parametr kwadratowy kosztu paliwa.
    double M;                                       ///< Stała (np. do funkcji kary / big-M).
};

/**
 * @brief Rozwiązanie problemu.
 */
struct Solution
{
    std::vector<int> route; ///< Kolejność odwiedzanych miast (zwykle z powrotem do 0 na końcu).
    double total_cost;      ///< Wartość funkcji celu.
    bool is_valid;          ///< Czy rozwiązanie spełnia ograniczenia.
};

/**
 * @brief Kandydat na kolejny węzeł (dla listy RCL).
 */
struct Candidate
{
    int city_index; ///< Indeks miasta.
    double cost;    ///< Koszt/ocena kandydata (np. odległość + paliwo + kara/czas).
};

#endif