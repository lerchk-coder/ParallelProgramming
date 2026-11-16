cmake_minimum_required(VERSION 3.10)
project(Lab2_MatrixMultiply)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(OpenMP REQUIRED)

add_executable(matrix_app "C:/Users/user/Desktop/ParallelProgramming/labs/lab2/src/main.cpp")

target_link_libraries(matrix_app PRIVATE OpenMP::OpenMP_CXX)