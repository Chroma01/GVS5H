import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))

    # prev[i]: previous index with same value (0 if none)
    prev = [0] * (n + 1)
    last = {}
    for i in range(1, n + 1):
        v = A[i - 1]
        prev[i] = last.get(v, 0)
        last[v] = i

    # Part 1: sum over subarrays of distinct value count.
    # Occurrence i is the FIRST occurrence of its value in [L,R]
    # iff prev[i] < L <= i and R >= i (no upper constraint from nxt).
    # Contribution: (i - prev[i]) choices of L times (n - i + 1) choices of R.
    distinct_sum = 0
    for i in range(1, n + 1):
        distinct_sum += (i - prev[i]) * (n - i + 1)

    # Part 2: sum over subarrays of e(S) = number of adjacent value pairs
    # {v, v+1} both present in the subarray.
    # For fixed R, with lastR[w] = last occurrence of w in A[1..R] (0 if none):
    #   both v and v+1 present in [L,R] iff L <= min(lastR[v], lastR[v+1]).
    # So pair_sum = sum_R S_R where S_R = sum_v min(lastR[v], lastR[v+1]).
    # Sweep R; when lastR[x] updates p -> R, only edges (x-1,x) and (x,x+1)
    # change their min; update S in O(1) and accumulate.
    lastR = [0] * (n + 2)  # index by value; values in [1..N]
    S = 0
    pair_sum = 0
    for R in range(1, n + 1):
        x = A[R - 1]
        p = lastR[x]
        # edge (x-1, x)
        if x - 1 >= 1:
            q = lastR[x - 1]
            S -= min(p, q)
            S += min(R, q)
        # edge (x, x+1)
        if x + 1 <= n:
            q = lastR[x + 1]
            S -= min(p, q)
            S += min(R, q)
        lastR[x] = R
        pair_sum += S

    print(distinct_sum - pair_sum)

solve()