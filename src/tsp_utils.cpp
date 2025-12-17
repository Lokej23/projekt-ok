#include "tsp_utils.hpp"
#include <fstream>
#include <iostream>
#include <cmath>
#include <algorithm>
#include "json.hpp"

using json = nlohmann::json;

/**
 * @brief Wczytuje dane problemu z pliku JSON.
 * Wymaga biblioteki nlohmann/json.hpp.
 */
bool LoadData(const std::string &filename, ProblemData &data)
{
    std::ifstream f(filename);
    if (!f.is_open())
        return false;

    json j;
    try
    {
        f >> j;
        data.n = j["n"];
        data.a = j["a"];
        data.b = j["b"];
        data.M = j["M"];

        data.c_matrix = j["c_matrix"].get<std::vector<std::vector<double>>>();
        data.t_matrix = j["t_matrix"].get<std::vector<std::vector<double>>>();

        data.windows.clear();
        for (auto &win : j["t_windows"])
        {
            data.windows.push_back({win[0], win[1]});
        }
    }
    catch (const std::exception &e)
    {
        std::cerr << "Blad parsowania JSON: " << e.what() << std::endl;
        return false;
    }
    return true;
}

/**
 * @brief Oblicza koszt paliwa: $f = a \cdot d + b \cdot d^2$.
 */
double CalcFuelCost(double distance, double a, double b)
{
    return a * distance + b * std::pow(distance, 2);
}

/**
 * @brief Wylicza koszt trasy (odległość + paliwo + kara za spóźnienie).
 */
double EvaluateSolution(const ProblemData &data, const std::vector<int> &route)
{
    double total_cost = 0.0;
    double current_time = 0.0;
    double penalty_sum = 0.0;

    for (size_t i = 0; i < route.size() - 1; ++i)
    {
        int u = route[i];
        int v = route[i + 1];

        double dist = data.c_matrix[u][v];
        double travel_time = data.t_matrix[u][v];

        double fuel = CalcFuelCost(dist, data.a, data.b);
        total_cost += (dist + fuel);

        double arrival = current_time + travel_time;
        double start_window = data.windows[v].first;
        double end_window = data.windows[v].second;

        if (arrival < start_window)
        {
            arrival = start_window;
        }
        current_time = arrival;

        if (current_time > end_window)
        {
            penalty_sum += (current_time - end_window);
        }
    }

    return total_cost + penalty_sum;
}