#ifndef TSP_GREEDY_SOLVER_HPP
#define TSP_GREEDY_SOLVER_HPP

#include "tsp_types.hpp"
#include <random>

/**
 * @file tsp_greedy_solver.hpp
 * @brief Deklaracje algorytmu zachłannego dla TSP z oknami czasowymi i paliwem.
 */

/**
 * @brief Uruchamia wielokrotnie algorytm zachłanny i zwraca najlepsze znalezione rozwiązanie.
 *
 * Funkcja uruchamia wiele iteracji na wielu wątkach i wybiera najlepszy wynik.
 *
 * @param data Dane problemu.
 * @param iterations Liczba iteracji konstrukcji rozwiązania.
 * @param k_best Liczba najlepszych kandydatów w (RCL).
 * @return Najlepsze znalezione rozwiązanie.
 */
Solution RunParallelGreedySolver(const ProblemData &data, int iterations, int k_best);

#endif