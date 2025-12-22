#include <iostream>
#include <omp.h>
#include <string>
#include "args.hxx"
#include "tsp_types.hpp"
#include "tsp_utils.hpp"
#include "tsp_greedy_solver.hpp"
#include "tsp_sa_solver.hpp"

/**
 * @file main.cpp
 * @brief Główny plik programu rozwiązującego problem TSP z ograniczeniami.
 * 
 * Program obsługuje argumenty wiersza poleceń, wczytuje dane,
 * uruchamia wybrany algorytm (Greedy lub Simulated Annealing)
 * i zapisuje wyniki.
 */

/**
 * @brief Główna funkcja programu.
 * 
 * @param argc Liczba argumentów wywołania.
 * @param argv Tablica argumentów wywołania.
 * @return int Kod wyjścia (0 - sukces, 1 - błąd).
 */
int main(int argc, char *argv[])
{
    args::ArgumentParser parser("TSP z ograniczeniem czasu i paliwa", "Program rozwiazujacy problem komiwojazera (TSP) wykorzystujący algorytm symulowanego wyżarzania oraz zachłanny ulosowiony.");
    args::HelpFlag help(parser, "help", "Wyswietl to menu pomocy", {'h', "help"});

    // Ścieżki plików
    args::ValueFlag<std::string> arg_input(parser, "input_path", "Sciezka do pliku wejsciowego", {'d', "data"});
    args::ValueFlag<std::string> arg_output(parser, "output_path", "Sciezka do pliku wynikowego", {'o', "output"});

    // Algorytm
    args::Group group(parser, "Algorytmy (wybierz jeden):", args::Group::Validators::AtMostOne);
    args::Flag arg_greedy(group, "greedy", "Uzyj algorytmu zachlannego (domyslnie)", {'g', "greedy"});
    args::Flag arg_sa(group, "sa", "Uzyj algorytmu symulowanego wyzarzania", {'s', "sa"});


    // parametry algorytmów
    args::ValueFlag<int> arg_iterations(parser, "iterations", "Liczba iteracji (domyslnie 1000)", {'i', "iterations"});
    args::ValueFlag<int> arg_k(parser, "k", "Liczba k najlepszych (domyslnie 4)", {'k'});
    args::ValueFlag<double> arg_T(parser, "T", "Temperatura początkowa (domyslnie 5000)", {'T'});
    args::ValueFlag<double> arg_cooling_rate(parser, "cooling_rate", "Współczynnik chłodzenia (domyslnie 0.99)", {'c'});
    args::ValueFlag<double> arg_t(parser, "t", "Minimalna temperatura (domyslnie 0.1)", {'t'});

    try
    {
        parser.ParseCLI(argc, argv);
    }
    catch (const args::Help &)
    {
        std::cerr << parser;
        return 0;
    }
    catch (const args::ParseError &e)
    {
        std::cerr << e.what() << std::endl;
        std::cerr << parser;
        return 1;
    }
    catch (const args::ValidationError &e)
    {
        std::cerr << e.what() << std::endl;
        std::cerr << parser;
        return 1;
    }

    if (!arg_input)
    {
        std::cerr << "Blad: Nie podano pliku wejsciowego." << std::endl;
        std::cerr << parser;
        return 1;
    }

    std::string filename = args::get(arg_input);

    int iterations = arg_iterations ? args::get(arg_iterations) : 1000;
    int k_best = arg_k ? args::get(arg_k) : 4;
    std::string algorithm = "greedy";
    if (arg_sa) {
        algorithm = "sa";
    }
    
    // Parametry SA
    double initial_temp = arg_T ? args::get(arg_T) : 5000.0;
    double cooling_rate = arg_cooling_rate ? args::get(arg_cooling_rate) : 0.99;
    double min_temp = arg_t ? args::get(arg_t) : 0.1;

    std::cerr << "--- TSP z ograniczeniem czasu i paliwa ---" << std::endl;

    ProblemData data;
    if (!LoadData(filename, data))
    {
        std::cerr << "Nie udalo sie wczytac pliku " << filename << std::endl;
        return 1;
    }

    std::cerr << "Wczytano " << data.n << " miast." << std::endl;
    std::cerr << "Liczba watkow: " << omp_get_max_threads() << std::endl;
    std::cerr << "Algorytm: " << algorithm << std::endl;
    
    if (algorithm == "greedy") {
        std::cerr << "Liczba iteracji: " << iterations << ", k najlepszych: " << k_best << std::endl;
    } else if (algorithm == "sa") {
        std::cerr << "SA Params: T=" << initial_temp << ", cooling=" << cooling_rate 
                  << ", min_T=" << min_temp << ", iter_per_temp=" << iterations 
                  << ", k_greedy=" << k_best << std::endl;
    }

    Solution best;
    double start_time = omp_get_wtime();

    if (algorithm == "greedy")
    {
        best = RunParallelGreedySolver(data, iterations, k_best);
    }
    else if (algorithm == "sa")
    {
        SAParams params;
        params.initial_temp = initial_temp;
        params.cooling_rate = cooling_rate;
        params.min_temp = min_temp;
        params.iterations_per_temp = iterations;
        params.k_best_greedy = k_best;
        
        best = RunParallelSASolver(data, params);
    }
    else
    {
        std::cerr << "Nieznany algorytm: " << algorithm << std::endl;
        return 1;
    }

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

    std::string output_filename;
    if (arg_output)
    {
        output_filename = args::get(arg_output);
    }
    else
    {
        output_filename = filename;
        size_t lastindex = output_filename.find_last_of(".");
        if (lastindex != std::string::npos)
        {
            output_filename = output_filename.substr(0, lastindex);
        }
        output_filename += "_result.json";
    }

    SaveResults(output_filename, best, end_time - start_time);
    std::cerr << "Wyniki zapisano do: " << output_filename << std::endl;

    return 0;
}