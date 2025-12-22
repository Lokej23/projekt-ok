#include "tsp_sa_solver.hpp"
#include "tsp_utils.hpp"
#include "tsp_greedy_solver.hpp"
#include <vector>
#include <cmath>
#include <algorithm>
#include <random>
#include <limits>
#include <omp.h>

/**
 * @file tsp_sa_solver.cpp
 * @brief Implementacja algorytmu Symulowanego Wyżarzania.
 */

/**
 * @brief Generuje sąsiada poprzez operację odwrócenia fragmentu trasy (2-opt).
 * Funkcja losuje dwa indeksy i odwraca kolejność miast pomiędzy nimi.
 * Modyfikuje wektor 'route' w miejscu. Nie rusza miasta startowego/końcowego (0).
 * @param route Trasa do zmodyfikowania.
 * @param n Liczba miast (indeksy w wektorze to 0..n).
 * @param rng Generator liczb losowych.
 */
static void MutateInvert(std::vector<int> &route, int n, std::mt19937 &rng)
{
    /// Można zmieniać indeksy od 1 do n-1, ponieważ trasa zaczyna i kończy się w mieście 0.
    if (n < 3) return;

    std::uniform_int_distribution<> distr(1, n - 1);
    
    int i = distr(rng);
    int j = distr(rng);

    /// Sprawdzenie czy i != j, jeśli tak to ponownie losujemy j
    if (i == j) 
    {
        j = distr(rng);
        if (i == j) return; ///< Brak zmiany
    }

    if (i > j) std::swap(i, j);

    /// Odwracamy fragment wektora
    std::reverse(route.begin() + i, route.begin() + j + 1);
}

/**
 * @brief Wykonuje pojedynczy przebieg Symulowanego Wyżarzania na jednym wątku.
 * @param data Dane problemu.
 * @param params Parametry SA.
 * @param rng Generator liczb losowych wątku.
 * @return Najlepsze rozwiązanie znalezione w tym przebiegu.
 */
static Solution GenSASolution(const ProblemData &data, const SAParams &params, std::mt19937 &rng)
{
    /// Generowanie rozwiązania bazowego metodą Greedy
    Solution current_sol = GenGreedySolution(data, params.k_best_greedy, rng);

    /// Dodatkowe przeliczenie kosztu
    /// current_sol.total_cost = EvaluateSolution(data, current_sol.route);
    
    Solution best_sol = current_sol;
    double temp = params.initial_temp;
    
    /// Rozkład dla prawdopodobieństwa akceptacji
    std::uniform_real_distribution<> prob_dist(0.0, 1.0);

    while (temp > params.min_temp)
    {
        for (int k = 0; k < params.iterations_per_temp; ++k)
        {
            /// Kandydat na sąsiada (kopia trasy)
            std::vector<int> neighbor_route = current_sol.route;
            
            /// Mutacja (2-opt)
            MutateInvert(neighbor_route, data.n, rng);

            /// Ocena sąsiada
            double neighbor_cost = EvaluateSolution(data, neighbor_route);
            
            /// Obliczenie różnicy kosztów
            double delta = neighbor_cost - current_sol.total_cost;

            /// Kryterium akceptacji Metropolis-Hastings
            if (delta < 0.0)
            {
                /// Bezwarunkowa akceptacja lepszego rozwiązania
                current_sol.route = neighbor_route;
                current_sol.total_cost = neighbor_cost;
                current_sol.is_valid = true;

                /// Aktualizacja najlepszego rozwiązania
                if (current_sol.total_cost < best_sol.total_cost)
                {
                    best_sol = current_sol;
                }
            }
            else
            {
                /// Gorsze rozwiązanie - akceptujemy z prawdopodobieństwem exp(-delta / T)
                double acceptance_prob = std::exp(-delta / temp); ///< e^{-\delta/T}
                if (prob_dist(rng) < acceptance_prob) ///< Losowa akceptacja
                {
                    current_sol.route = neighbor_route;
                    current_sol.total_cost = neighbor_cost;
                    current_sol.is_valid = true;
                }
            }
        }

        /// Chłodzenie
        temp *= params.cooling_rate;
    }

    return best_sol;
}

Solution RunParallelSASolver(const ProblemData &data, const SAParams &params)
{
    Solution global_best;
    global_best.total_cost = std::numeric_limits<double>::max(); ///< Inicjalizacja: największa wartość.
    global_best.is_valid = false;

    #pragma omp parallel
    {
        /// Inny seed dla każdego wątku.
        std::random_device rd;
        std::mt19937 thread_rng(rd() + omp_get_thread_num());

        Solution thread_best = GenSASolution(data, params, thread_rng);

        /// Tylko jeden wątek na raz aktualizuje najlepsze rozwiązanie.
        #pragma omp critical
        {
            if (thread_best.total_cost < global_best.total_cost)
            {
                global_best = thread_best;
            }
        }
    }

    return global_best;
}