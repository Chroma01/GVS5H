import sys

def solve():
    input_data = sys.stdin.read().split()
    it = iter(input_data)
    N = int(next(it))
    X = int(next(it))
    foods = [[], [], []]  # index 0,1,2 for vitamin 1,2,3
    maxA = 0
    for _ in range(N):
        v = int(next(it)) - 1
        a = int(next(it))
        c = int(next(it))
        foods[v].append((a, c))
        if a > maxA:
            maxA = a
    # DP for each vitamin: best[v][c] = max vitamin amount achievable with exactly c calories
    # We'll use -1 for impossible states.
    best = [[-1] * (X + 1) for _ in range(3)]
    for v in range(3):
        dp = [-1] * (X + 1)
        dp[0] = 0
        for a, c in foods[v]:
            # 0/1 knapsack: iterate c from X down to c
            for cur_c in range(X, c - 1, -1):
                if dp[cur_c - c] != -1:
                    val = dp[cur_c - c] + a
                    if val > dp[cur_c]:
                        dp[cur_c] = val
        best[v] = dp
        # make prefix max over calories: for each c, best[v][c] = max_{c' <= c} best[v][c']
        cur_max = -1
        for c in range(X + 1):
            if dp[c] > cur_max:
                cur_max = dp[c]
            best[v][c] = cur_max
    # Binary search on answer M
    lo = 0
    hi = maxA * N + 1  # upper bound exclusive
    # Actually we can bound hi by sum of all A_i, but maxA*N is safe.
    while lo < hi:
        mid = (lo + hi) // 2
        # Check if we can achieve at least mid for each vitamin with total calories <= X
        # For each vitamin, find minimal calories needed to get >= mid
        needed = [0, 0, 0]
        possible = True
        for v in range(3):
            # find smallest c such that best[v][c] >= mid
            found = False
            # linear scan is O(X) per vitamin, total O(3X) per check, fine.
            for c in range(X + 1):
                if best[v][c] >= mid:
                    needed[v] = c
                    found = True
                    break
            if not found:
                possible = False
                break
        if possible and needed[0] + needed[1] + needed[2] <= X:
            lo = mid + 1
        else:
            hi = mid
    # lo is the first value that is NOT achievable, so answer is lo-1
    print(lo - 1)

if __name__ == "__main__":
    solve()