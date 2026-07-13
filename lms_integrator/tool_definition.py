def suggest_tile(N):
    # naive suggestion: try common tile sizes
    candidates = [32,16,8,4]
    for t in candidates:
        if N % t == 0:
            return t
    return candidates[0]
