
cmake_minimum_required(VERSION 3.10)
project(arquiteia_backend)

set(CMAKE_CXX_STANDARD 17)

include(FetchContent)

# Try to find an installed pybind11 first; if not found, fetch it via FetchContent
find_package(pybind11 CONFIG QUIET)
if(NOT pybind11_FOUND)
    message(STATUS "pybind11 not found - fetching pybind11 via FetchContent")
    FetchContent_Declare(
        pybind11
        GIT_REPOSITORY https://github.com/pybind/pybind11.git
        # Use an older pybind11 tag compatible with older MSVC toolchains as a temporary workaround
        GIT_TAG v2.9.2
    )
    FetchContent_MakeAvailable(pybind11)
endif()

pybind11_add_module(arquiteia
        src/cache_simulator.cpp
        src/matmul_tiling.cpp
        src/arquiteia_bindings.cpp
)

target_include_directories(arquiteia PUBLIC include)
