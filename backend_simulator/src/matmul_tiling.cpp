#include "../include/arquiteia.hpp"

using namespace arquiteia;

size_t arquiteia::compute_gemm_flops(size_t N) {
    // 2 * N^3 for matrix multiply
    return (size_t)2 * N * N * N;
}
