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

    std::cerr << "--- TSP z ograniczeniem czasu i paliwa ---" << std::endl;

    if (!LoadData(filename, data))
    {
        std::cerr << "Nie udalo sie wczytac pliku " << filename << std::endl;
        return 1;
    }

    std::cerr << "Wczytano " << data.n << " miast." << std::endl;
    std::cerr << "Liczba watkow: " << omp_get_max_threads() << std::endl;

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

    std::cerr << "Liczba iteracji: " << iterations << ", k najlepszych: " << k_best << std::endl;
    std::cerr << "Rozpoczynanie obliczen..." << std::endl;

    double start_time = omp_get_wtime();

    Solution best = RunParallelGreedySolver(data, iterations, k_best);

    double end_time = omp_get_wtime();

    std::cerr << "----------------------------------------" << std::endl;
    std::cerr << "Czas obliczen: " << (end_time - start_time) << " s" << std::endl;
    std::cerr << "Najlepszy znaleziony koszt Z: " << best.total_cost << std::endl;
    std::cerr << "Trasa: ";
    for (size_t i = 0; i < best.route.size(); ++i)
    {
        std::cerr << best.route[i];
        if (i < best.route.size() - 1)
            std::cerr << " -> ";
    }
    std::cerr << std::endl;

    std::string output_filename = filename;
    size_t lastindex = output_filename.find_last_of("."); 
    if (lastindex != std::string::npos) {
        output_filename = output_filename.substr(0, lastindex); 
    }
    output_filename += "_results.json";
    
    SaveResults(output_filename, best, end_time - start_time);
    std::cerr << "Wyniki zapisano do: " << output_filename << std::endl;

    return 0;
}