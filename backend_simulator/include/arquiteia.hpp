#pragma once

#include <cstddef>

namespace arquiteia {

struct CacheResult {
    size_t cache_misses;
    size_t accesses;
};

// Estimate cache misses for a GEMM with given matrix size and tile size
CacheResult estimate_gemm_cache(size_t N, size_t tile);

// Compute a simple FLOP count for a matrix multiply
size_t compute_gemm_flops(size_t N);

} // namespace arquiteia
