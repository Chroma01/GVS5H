import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    L = [0] * M
    R = [0] * M
    for i in range(M):
        L[i] = int(next(it))
        R[i] = int(next(it))
    
    # Greedy set cover: cover [1, N] with min number of operations
    # Type 1: covers [L_i, R_i]
    # Type 2: covers complement of [L_i, R_i], i.e., [1, L_i-1] U [R_i+1, N]
    # Each used operation costs 1.
    
    # Sort operations by L ascending, then R descending
    sorted_idx = list(range(M))
    sorted_idx.sort(key=lambda i: (L[i], -R[i]))
    
    ans = [0] * M  # 0, 1, or 2
    pos = 0  # rightmost covered position so far
    total_cost = 0
    
    # Phase 1: extend coverage using type 1 operations
    # Classic greedy interval covering: always pick the interval with max R among those with L <= pos+1
    i = 0  # pointer in sorted_idx
    while pos < N:
        maxR = pos
        best_idx = -1
        # Scan all intervals with L <= pos+1 that are unused
        while i < M and L[sorted_idx[i]] <= pos + 1:
            idx = sorted_idx[i]
            if ans[idx] == 0 and R[idx] > maxR:
                maxR = R[idx]
                best_idx = idx
            i += 1
        if best_idx != -1:
            pos = maxR
            ans[best_idx] = 1
            total_cost += 1
        else:
            break
    
    # Phase 2: if not fully covered, try to finish with a type 2 operation
    if pos < N:
        # Need an unused operation with R <= pos (so that complement covers [pos+1, N])
        # Among those, pick the one with minimum L to also cover [1, L-1]
        min_L = float('inf')
        finish_idx = -1
        for idx in range(M):
            if ans[idx] == 0 and R[idx] <= pos:
                if L[idx] < min_L:
                    min_L = L[idx]
                    finish_idx = idx
        if finish_idx != -1:
            ans[finish_idx] = 2
            total_cost += 1
            pos = N
        else:
            print(-1)
            return
    
    # Output result
    out = [str(total_cost), ' '.join(str(x) for x in ans)]
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == "__main__":
    solve()