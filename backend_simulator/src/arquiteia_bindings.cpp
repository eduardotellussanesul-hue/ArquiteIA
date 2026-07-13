#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../include/arquiteia.hpp"

namespace py = pybind11;

PYBIND11_MODULE(arquiteia, m) {
    m.doc() = "ArquiteIA C++ backend bindings";

    py::class_<arquiteia::CacheResult>(m, "CacheResult")
        .def_readonly("cache_misses", &arquiteia::CacheResult::cache_misses)
        .def_readonly("accesses", &arquiteia::CacheResult::accesses);

    m.def("estimate_gemm_cache", &arquiteia::estimate_gemm_cache, "Estimate cache behavior for GEMM",
          py::arg("N"), py::arg("tile"));

    m.def("compute_gemm_flops", &arquiteia::compute_gemm_flops, "Compute FLOPs for GEMM", py::arg("N"));
}
