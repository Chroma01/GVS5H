import sys
sys.setrecursionlimit(1 << 25)

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    
    # Edge cases
    if K == 0:
        print(0)
        return
    if K == 1:
        print(max(A))
        return
    if K == N:
        result = 0
        for x in A:
            result ^= x
        print(result)
        return
    
    max_xor_val = [0]
    A_list = A
    N_val = N
    K_val = K
    
    def dfs(start, count, current_xor):
        if count == K_val:
            if current_xor > max_xor_val[0]:
                max_xor_val[0] = current_xor
            return
        # Pruning: not enough elements left to reach K
        if N_val - start < K_val - count:
            return
        # We need to pick (K_val - count) more elements starting from index i
        # So i can go up to N_val - (K_val - count)
        limit = N_val - (K_val - count)
        for i in range(start, limit + 1):
            dfs(i + 1, count + 1, current_xor ^ A_list[i])
    
    dfs(0, 0, 0)
    print(max_xor_val[0])

solve()