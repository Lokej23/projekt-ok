#include <iostream>
#include <omp.h>
#include "tsp_types.hpp"
#include "tsp_utils.hpp"
#include "tsp_greedy_solver.hpp"

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        std::cerr << "Uzycie: " << argv[0] << " path/file.json iterations k" << std::endl;
        return 1;
    }
    std::string filename = argv[1];
    ProblemData data;

    std::cout << "--- TSP z ograniczeniem czasu i paliwa ---" << std::endl;

    if (!LoadData(filename, data))
    {
        std::cerr << "Nie udalo sie wczytac pliku " << filename << std::endl;
        return 1;
    }

    std::cout << "Wczytano " << data.n << " miast." << std::endl;
    std::cout << "Liczba watkow: " << omp_get_max_threads() << std::endl;

    int iterations;
    int k_best;
    if (argc < 4)
    {
        iterations = 1000;
        k_best = 4;
    }
    else
    {
        iterations = std::stoi(argv[2]);
        k_best = std::stoi(argv[3]);
    };

    std::cout << "Liczba iteracji: " << iterations << ", k najlepszych: " << k_best << std::endl;
    std::cout << "Rozpoczynanie obliczen..." << std::endl;

    double start_time = omp_get_wtime();

    Solution best = RunParallelGreedySolver(data, iterations, k_best);

    double end_time = omp_get_wtime();

    std::cout << "----------------------------------------" << std::endl;
    std::cout << "Czas obliczen: " << (end_time - start_time) << " s" << std::endl;
    std::cout << "Najlepszy znaleziony koszt Z: " << best.total_cost << std::endl;
    std::cout << "Trasa: ";
    for (size_t i = 0; i < best.route.size(); ++i)
    {
        std::cout << best.route[i];
        if (i < best.route.size() - 1)
            std::cout << " -> ";
    }
    std::cout << std::endl;

    return 0;
}