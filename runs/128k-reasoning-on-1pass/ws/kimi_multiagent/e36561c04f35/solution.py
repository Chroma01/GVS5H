import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    T = int(data[pos]); pos += 1
    out = []
    INF = 1 << 30
    for _ in range(T):
        N = int(data[pos]); pos += 1
        A = [int(x) for x in data[pos:pos + N]]; pos += N

        # DP over disjoint adjacent-swap sets.
        # d_j = 1 iff we swap pair (j, j+1) (0-indexed), with d_j + d_{j+1} <= 1.
        # State while processing position i: (d_{i-2}, d_{i-1}), only three
        # feasible values: (0,0), (1,0), (0,1).
        # Cost = (#swaps so far) + (#runs of the resulting sequence so far).
        # Final value at position i:
        #   A[i+1] if d_i=1, else A[i-1] if d_{i-1}=1, else A[i].
        dp00, dp10, dp01 = 0, INF, INF
        for i in range(N):
            ai = A[i]
            n00 = INF; n10 = INF; n01 = INF
            last = (i + 1 == N)

            # from state (d_{i-2}, d_{i-1}) = (0,0): position i-1 holds A[i-1]
            if dp00 < INF:
                if i:
                    vp = A[i-1]
                    c = dp00 + (1 if ai != vp else 0)
                else:
                    vp = 0
                    c = dp00 + 1                      # first element opens a run
                if c < n00: n00 = c                   # d_i = 0 -> state (0,0)
                if not last:                          # d_i = 1 -> state (0,1)
                    v = A[i+1]
                    c = dp00 + 1 + ((1 if v != vp else 0) if i else 1)
                    if c < n01: n01 = c

            # from state (1,0): pair (i-2,i-1) swapped, position i-1 holds A[i-2]
            if dp10 < INF:
                vp = A[i-2]
                c = dp10 + (1 if ai != vp else 0)
                if c < n00: n00 = c                   # d_i = 0 -> state (0,0)
                if not last:
                    v = A[i+1]
                    c = dp10 + 1 + (1 if v != vp else 0)
                    if c < n01: n01 = c               # d_i = 1 -> state (0,1)

            # from state (0,1): pair (i-1,i) swapped, position i-1 holds A[i];
            # d_i forced 0 (disjointness), position i holds A[i-1]
            if dp01 < INF:
                v = A[i-1]
                c = dp01 + (1 if v != ai else 0)
                if c < n10: n10 = c                   # -> state (1,0)

            dp00, dp10, dp01 = n00, n10, n01

        out.append(str(min(dp00, dp10, dp01)))
    sys.stdout.write('\n'.join(out) + '\n')

main()