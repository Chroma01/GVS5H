import sys
from math import isqrt

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    P = [int(x) for x in data[2:2 + N]]
    P.sort()
    p_min = P[0]

    # Safe upper bound for the threshold V.
    # For any feasible V, S(V) >= p_min * c^2 with c = (V//p_min + 1)//2.
    # This implies V < 2*sqrt(M*p_min) + 2*p_min + 2.
    upper = min(M, 2 * isqrt(M * p_min) + 2 * p_min + 2)

    def total_cost(V):
        s = 0
        for p in P:
            if p > V:
                break
            c = (V // p + 1) // 2
            s += p * c * c
            if s > M:
                return s
        return s

    lo, hi = 0, upper
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if total_cost(mid) <= M:
            lo = mid
        else:
            hi = mid - 1
    V = lo

    total = 0
    count = 0
    w = 10**30
    cnt_w = 0
    for p in P:
        if p > V:
            c = 0
        else:
            c = (V // p + 1) // 2
        count += c
        total += p * c * c
        nxt = p * (2 * c + 1)
        if nxt < w:
            w = nxt
            cnt_w = 1
        elif nxt == w:
            cnt_w += 1

    R = M - total
    ans = count + min(cnt_w, R // w)
    print(ans)

if __name__ == "__main__":
    solve()