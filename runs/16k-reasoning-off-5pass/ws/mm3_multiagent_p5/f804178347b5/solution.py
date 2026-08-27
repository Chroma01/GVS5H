import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    # The rest are bits; they may be given as a single string or separated.
    bits = []
    for token in data[1:]:
        bits.extend(list(token))
    # Ensure we have exactly 3^N bits
    A = bits[:3**N]
    # Recursive DP
    sys.setrecursionlimit(1000000)
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dp(l, size):
        # Returns (cost0, cost1) for the subtree covering A[l:l+size]
        if size == 1:
            val = int(A[l])
            cost0 = 0 if val == 0 else 1
            cost1 = 0 if val == 1 else 1
            return (cost0, cost1)
        third = size // 3
        c1 = dp(l, third)
        c2 = dp(l + third, third)
        c3 = dp(l + 2 * third, third)
        # Combine for parent = 0
        # Configs: (0,0,0), (0,0,1), (0,1,0), (1,0,0)
        cost0 = min(
            c1[0] + c2[0] + c3[0],
            c1[0] + c2[0] + c3[1],
            c1[0] + c2[1] + c3[0],
            c1[1] + c2[0] + c3[0]
        )
        # Combine for parent = 1
        # Configs: (1,1,1), (1,1,0), (1,0,1), (0,1,1)
        cost1 = min(
            c1[1] + c2[1] + c3[1],
            c1[1] + c2[1] + c3[0],
            c1[1] + c2[0] + c3[1],
            c1[0] + c2[1] + c3[1]
        )
        return (cost0, cost1)

    total_size = 3 ** N
    cost0, cost1 = dp(0, total_size)
    print(min(cost0, cost1))

if __name__ == "__main__":
    solve()