#ifndef TSP_TYPES_HPP
#define TSP_TYPES_HPP

#include <vector>
#include <string>

struct ProblemData
{
    int n;                                          // miasta
    std::vector<std::vector<double>> c_matrix;      // c_ij
    std::vector<std::vector<double>> t_matrix;      // t_ij
    std::vector<std::pair<double, double>> windows; // [e_i, l_i]
    double a;                                       // poliwo liniowy
    double b;                                       // paliwo kwadratowy
    double M;                                       // stała
};

struct Solution
{
    std::vector<int> route; // kolejność miast
    double total_cost;
    bool is_valid;
};

struct Candidate
{
    int city_index;
    double heuristic_cost; // odległość + kara + czas
};

#endif