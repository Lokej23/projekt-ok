#include "tsp_greedy_solver.hpp"
#include "tsp_utils.hpp"
#include <vector>
#include <algorithm>
#include <random>
#include <limits>
#include <omp.h>

/**
 * @file tsp_greedy_solver.cpp
 * @brief Implementacja algorytmu zachłannego z losowaniem z RCL z wykorzystaniem biblioteki OpenMP.
 */

/**
 * @brief Generuje pojedyncze rozwiązanie metodą zachłanną z RCL.
 * @param data Dane problemu.
 * @param k_best Rozmiar listy RCL.
 * @param rng Generator losowy.
 * @return Wygenerowane rozwiązanie.
 */
static Solution GenGreedySolution(const ProblemData &data, int k_best, std::mt19937 &rng)
{
    int n = data.n;
    std::vector<int> route;
    route.reserve(n + 1);
    std::vector<bool> visited(n, false);

    /// Start w mieście 0.
    int current_node = 0;
    route.push_back(current_node);
    visited[current_node] = true;

    double current_time = 0.0; ///< Aktualny czas (start: 0).

    /// Konstrukcja trasy: kolejne wybory miasta.
    for (int step = 1; step < n; ++step)
    {
        std::vector<Candidate> candidates;
        candidates.reserve(n - step);

        /// Budowa listy kandydatów.
        for (int next_node = 0; next_node < n; ++next_node)
        {
            if (visited[next_node])
                continue;

            double dist = data.c_matrix[current_node][next_node];
            double drive_time = data.t_matrix[current_node][next_node];

            /// Czas przyjazdu, ewentualne oczekiwanie i kara.
            double arrival = current_time + drive_time;
            double wait_time = 0.0;
            double penalty = 0.0;

            /// Okna czasowe.
            double e_i = data.windows[next_node].first;
            double l_i = data.windows[next_node].second;

            if (arrival < e_i)
            {
                wait_time = e_i - arrival;
                arrival = e_i; ///< Jeśli przyjechano za wcześnie.
            }
            if (arrival > l_i)
            {
                penalty = arrival - l_i; ///< Kara za spóźnienie.
            }

            double fuel_cost = CalcFuelCost(dist, data.a, data.b); ///< Koszt paliwa.

            /// Heurystyka: kara jest gorsza od czasu oczekiwania.
            double score = (dist + fuel_cost) + (penalty * 2.0) + (wait_time * 0.5);

            candidates.push_back({next_node, score});
        }

        /// Sortowanie częściowe, aby dostać k_best dla RCL.
        int k = std::min((int)candidates.size(), k_best);
        std::partial_sort(candidates.begin(), candidates.begin() + k, candidates.end(),
                          [](const Candidate &a, const Candidate &b)
                          {
                              return a.cost < b.cost;
                          });

        /// Losowanie miasta z RCL.
        std::uniform_int_distribution<> distr(0, k - 1);
        int chosen_idx = distr(rng);
        Candidate chosen = candidates[chosen_idx];

        int next_city = chosen.city_index;

        /// Aktualizacja czasu dla wybranego miasta.
        double final_drive_time = data.t_matrix[current_node][next_city];
        double final_arrival = current_time + final_drive_time;
        if (final_arrival < data.windows[next_city].first)
        {
            final_arrival = data.windows[next_city].first;
        }

        /// Aktualizacja stanu.
        current_time = final_arrival;
        current_node = next_city;
        route.push_back(current_node);
        visited[current_node] = true;
    }

    /// Powrót do bazy.
    route.push_back(0);

    /// Złożenie końcowego rozwiązania.
    Solution sol;
    sol.route = route;
    /// Wyliczanie kosztu funkcją weryfikującą.
    sol.total_cost = EvaluateSolution(data, route);
    sol.is_valid = true;

    return sol;
}

Solution RunParallelGreedySolver(const ProblemData &data, int iterations, int k_best)
{
    Solution global_best;
    global_best.total_cost = std::numeric_limits<double>::max(); ///< Inicjalizacja: największa wartość.
    global_best.is_valid = false;

#pragma omp parallel
    {
        /// Inny seed dla każdego wątku.
        std::random_device rd;
        std::mt19937 thread_rng(rd() + omp_get_thread_num());

        Solution thread_best;
        thread_best.total_cost = std::numeric_limits<double>::max();

        /// Podział pętli na wątki.
#pragma omp for
        for (int i = 0; i < iterations; ++i)
        {
            Solution current_sol = GenGreedySolution(data, k_best, thread_rng);

            if (current_sol.total_cost < thread_best.total_cost)
            {
                thread_best = current_sol;
            }
        }

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