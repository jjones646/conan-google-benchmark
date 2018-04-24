cmake_minimum_required(VERSION 3.0)

project(ConanGoogleBenchmark)
include(conanbuildinfo.cmake)

conan_basic_setup(TARGETS)

if(BENCHMARK_ENABLE_TESTING)
    enable_testing()
endif()

add_subdirectory(benchmark)
