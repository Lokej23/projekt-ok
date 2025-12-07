#ifndef TSP_GREEDY_SOLVER_HPP
#define TSP_GREEDY_SOLVER_HPP

#include "tsp_types.hpp"
#include <random>

Solution RunParallelGreedySolver(const ProblemData &data, int iterations, int k_best);

#endif