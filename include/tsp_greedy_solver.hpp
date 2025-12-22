#ifndef TSP_GREEDY_SOLVER_HPP
#define TSP_GREEDY_SOLVER_HPP

#include "tsp_types.hpp"
#include <random>

/**
 * @file tsp_greedy_solver.hpp
 * @brief Deklaracje algorytmu zachłannego dla TSP z oknami czasowymi i paliwem.
 */

/**
 * @brief Generuje pojedyncze rozwiązanie metodą zachłanną z RCL.
 *
 * @param data Dane problemu.
 * @param k_best Rozmiar listy RCL.
 * @param rng Generator losowy.
 * @return Wygenerowane rozwiązanie.
 */
Solution GenGreedySolution(const ProblemData &data, int k_best, std::mt19937 &rng);

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