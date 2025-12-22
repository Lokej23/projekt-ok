cmake_minimum_required(VERSION 3.10)
project(TSP_Fuel_Time)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Znajdowanie pakietu OpenMP
find_package(OpenMP REQUIRED)

# doxygen
find_package(Doxygen)

if (DOXYGEN_FOUND)
    add_custom_target(doc
        COMMAND ${DOXYGEN_EXECUTABLE} ${CMAKE_SOURCE_DIR}/Doxyfile
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        COMMENT "Generating API documentation with Doxygen"
        VERBATIM)
else()
    message("Doxygen not found, unable to generate documentation")
endif()

# Katalog z nagłówkami
include_directories(include)

# Pliki źródłowe
set(SOURCES 
    src/main.cpp 
    src/tsp_utils.cpp 
    src/tsp_greedy_solver.cpp
    src/tsp_sa_solver.cpp
)

add_executable(tsp_solver ${SOURCES})

# Linkowanie OpenMP
if(OpenMP_CXX_FOUND)
    target_link_libraries(tsp_solver PUBLIC OpenMP::OpenMP_CXX)
endif()