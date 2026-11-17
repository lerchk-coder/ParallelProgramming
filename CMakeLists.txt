cmake_minimum_required(VERSION 3.18)

set(CUDAToolkit_ROOT "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v13.5")
set(CMAKE_CUDA_COMPILER "${CUDAToolkit_ROOT}/bin/nvcc.exe")

project(ParallelProgramming_Labs LANGUAGES CXX CUDA)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CUDA_STANDARD 14)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

if(MSVC)
    add_compile_options(/utf-8)
    set(CMAKE_CXX_FLAGS_RELEASE "/O2 /DNDEBUG")
    set(CMAKE_CUDA_FLAGS_RELEASE "-O3")
else()
    set(CMAKE_CXX_FLAGS_RELEASE "-O3")
    set(CMAKE_CUDA_FLAGS_RELEASE "-O3")
endif()

find_package(OpenMP REQUIRED)
find_package(CUDAToolkit REQUIRED)

if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/lab1/CMakeLists.txt")
    add_subdirectory(lab1)
endif()

if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/lab2/CMakeLists.txt")
    add_subdirectory(lab2)
endif()

if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/lab4/CMakeLists.txt")
    add_subdirectory(lab4)
endif()