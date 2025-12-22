#ifndef TSP_SA_SOLVER_HPP
#define TSP_SA_SOLVER_HPP

#include "tsp_types.hpp"

/**
 * @file tsp_sa_solver.hpp
 * @brief Deklaracje algorytmu Symulowanego Wyżarzania (Simulated Annealing) dla TSP.
 */

/**
 * @brief Parametry konfiguracyjne dla algorytmu Symulowanego Wyżarzania.
 */
struct SAParams
{
    double initial_temp;     ///< Temperatura początkowa.
    double cooling_rate;     ///< Współczynnik chłodzenia.
    double min_temp;         ///< Temperatura końcowa (warunek stopu).
    int iterations_per_temp; ///< Liczba prób zmiany sąsiedztwa dla jednej temperatury.
    int k_best_greedy;       ///< Parametr k dla generowania rozwiązania początkowego (z alg. zachłannego).
};

/**
 * @brief Uruchamia wielokrotnie algorytm Symulowanego Wyżarzania.
 *
 * Każdy wątek generuje własne rozwiązanie początkowe metodą zachłanną (używając GenGreedySolution),
 * a następnie przeprowadza proces wyżarzania, próbując ulepszyć to rozwiązanie.
 * Zwracane jest najlepsze rozwiązanie znalezione przez wszystkie wątki.
 *
 * @param data Dane problemu.
 * @param params Parametry algorytmu SA.
 * @return Najlepsze znalezione rozwiązanie.
 */
Solution RunParallelSASolver(const ProblemData &data, const SAParams &params);

#endif