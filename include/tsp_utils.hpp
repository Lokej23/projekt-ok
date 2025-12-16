#ifndef TSP_UTILS_HPP
#define TSP_UTILS_HPP

#include "tsp_types.hpp"
#include <string>

bool LoadData(const std::string &filename, ProblemData &data);
double CalcFuelCost(double distance, double a, double b);
double EvaluateSolution(const ProblemData &data, const std::vector<int> &route);

#endif