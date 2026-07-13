#include "../include/arquiteia.hpp"

using namespace arquiteia;

// Very simple cache miss estimator (not cycle-accurate)
CacheResult arquiteia::estimate_gemm_cache(size_t N, size_t tile) {
    CacheResult r{};
    if (tile == 0) tile = 1;
    // naive model: number of tile loads per matrix
    size_t tiles_per_row = (N + tile - 1) / tile;
    size_t total_tiles = tiles_per_row * tiles_per_row;
    // assume each tile brings tile*tile elements
    r.accesses = N * N * 2; // read A and B
    // simplistic: misses proportional to number of tiles
    r.cache_misses = total_tiles * tile * tile;
    return r;
}
