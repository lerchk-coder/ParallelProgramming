cmake_minimum_required(VERSION 3.10)
project(Lab1_MatrixMultiply)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# OpenMP
find_package(OpenMP REQUIRED)

if(MSVC)
    add_compile_options(/utf-8)
    set(CMAKE_CXX_FLAGS_RELEASE "/O2 /DNDEBUG")
else()
    set(CMAKE_CXX_FLAGS_RELEASE "-O3")
endif()

add_executable(matrix_app src/main.cpp)

if(OpenMP_CXX_FOUND)
    target_link_libraries(matrix_app PRIVATE OpenMP::OpenMP_CXX)
endif()