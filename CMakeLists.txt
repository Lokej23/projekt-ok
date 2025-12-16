cmake_minimum_required(VERSION 3.10)
project(TSP_Fuel_Time)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Znajdowanie pakietu OpenMP
find_package(OpenMP REQUIRED)

# Katalog z nagłówkami
include_directories(include)

# Pliki źródłowe
set(SOURCES 
    src/main.cpp 
    src/tsp_utils.cpp 
    src/tsp_greedy_solver.cpp
)

add_executable(tsp_solver ${SOURCES})

# Linkowanie OpenMP
if(OpenMP_CXX_FOUND)
    target_link_libraries(tsp_solver PUBLIC OpenMP::OpenMP_CXX)
endif()