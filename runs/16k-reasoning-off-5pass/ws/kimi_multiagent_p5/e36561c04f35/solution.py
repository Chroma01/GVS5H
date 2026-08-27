import sys
from collections import defaultdict

def fast(A):
    N = len(A)
    dp = [0] * (N + 1)
    cv = defaultdict(int)      # cv[v] = count of value v in processed prefix
    Hv = defaultdict(int)      # Hv[v] = # pairs p<q in prefix with A[p]!=v, A[q]==v
    hull = defaultdict(list)   # per-value lower envelope of lines (m, b)
    ptr = defaultdict(int)     # per-value query pointer

    def add_line(v, m, b):
        h = hull[v]
        # same slope: keep only the smallest intercept (min queries)
        while h and h[-1][0] == m:
            if h[-1][1] <= b:
                return
            h.pop()
        while len(h) >= 2:
            m1, b1 = h[-2]
            m2, b2 = h[-1]
            # slopes strictly decreasing: m1 > m2 > m
            # middle line useless iff (b2-b1)/(m1-m2) >= (b-b2)/(m2-m)
            if (b2 - b1) * (m2 - m) >= (b - b2) * (m1 - m2):
                h.pop()
            else:
                break
        h.append((m, b))

    def query(v, x):
        h = hull[v]
        p = ptr[v]
        while p + 1 < len(h) and h[p][0] * x + h[p][1] >= h[p + 1][0] * x + h[p + 1][1]:
            p += 1
        ptr[v] = p
        return h[p][0] * x + h[p][1]

    for i in range(1, N + 1):
        v = A[i - 1]
        # add line for j = i-1 using state of prefix A[:i-1]
        j = i - 1
        nv_j = j - cv[v]
        add_line(v, -nv_j, dp[j] - Hv[v] + nv_j * cv[v])
        # incorporate A[i-1] = v into counters
        Hv[v] += (i - 1) - cv[v]
        cv[v] += 1
        # transitions
        best = dp[i - 1] + 1
        c = query(v, cv[v]) + Hv[v] + 1
        if c < best:
            best = c
        dp[i] = best
    return dp[N]

def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    T = int(data[idx]); idx += 1
    out = []
    for _ in range(T):
        N = int(data[idx]); idx += 1
        A = [int(x) for x in data[idx:idx + N]]; idx += N
        out.append(str(fast(A)))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    solve()