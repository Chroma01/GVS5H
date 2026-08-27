import sys
from bisect import bisect_left

SELF_TEST = False


def _build(arr):
    arr.sort()
    n = len(arr)
    pref = [0] * (n + 1)
    pm = 0
    for i, v in enumerate(arr):
        pref[i + 1] = pref[i] + v
        pm += v * (n - 1 - i)
    return arr, pref, pm


def solve_parts(D, U, P):
    D_arr, D_pref, pmD = _build(D)
    U_arr, U_pref, pmU = _build(U)
    P.sort(reverse=True)

    Psum = sum(P)
    sumU = sum(U)
    m = len(D) + len(U)

    ans = m * Psum + sumU + pmD + pmU
    sumS = 0
    d_len = len(D_arr)
    u_len = len(U_arr)

    for k, x in enumerate(P, 1):
        idx = bisect_left(D_arr, x)
        pmD += D_pref[idx] + x * (d_len - idx) + x * (k - 1)

        idx = bisect_left(U_arr, x)
        pmU += U_pref[idx] + x * (u_len - idx) + x * (k - 1)

        sumS += x
        val = (m + 2 * k) * (Psum - sumS) + sumU + sumS + pmD + pmU
        if val < ans:
            ans = val

    return ans


def solve_case(A, B, C):
    D = []
    U = []
    P = []
    for a, b, c in zip(A, B, C):
        if a == 1 and b == 0:
            D.append(c)
        elif a == 0 and b == 1:
            U.append(c)
        elif a == 1 and b == 1:
            P.append(c)
    return solve_parts(D, U, P)


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    D = []
    U = []
    P = []

    a0 = 1
    b0 = 1 + N
    c0 = 1 + 2 * N

    for i in range(N):
        a = data[a0 + i]
        b = data[b0 + i]
        c = data[c0 + i]

        if a == 1 and b == 0:
            D.append(c)
        elif a == 0 and b == 1:
            U.append(c)
        elif a == 1 and b == 1:
            P.append(c)

    del data
    print(solve_parts(D, U, P))


def brute_force(A, B, C):
    N = len(A)
    start = tuple(A)
    target = tuple(B)

    import heapq

    INF = 10**30
    dist = {start: 0}
    heap = [(0, start)]

    while heap:
        d, s = heapq.heappop(heap)
        if d != dist.get(s):
            continue
        if s == target:
            return d

        for i in range(N):
            ns = list(s)
            ns[i] ^= 1
            ns = tuple(ns)

            cost = 0
            for j in range(N):
                if ns[j]:
                    cost += C[j]

            nd = d + cost
            if nd < dist.get(ns, INF):
                dist[ns] = nd
                heapq.heappush(heap, (nd, ns))

    return dist.get(target, INF)


def _self_test():
    import random

    random.seed(12345)
    for _ in range(300):
        N = random.randint(1, 5)
        A = [random.randint(0, 1) for _ in range(N)]
        B = [random.randint(0, 1) for _ in range(N)]
        C = [random.randint(1, 10) for _ in range(N)]

        expected = brute_force(A, B, C)
        got = solve_case(A, B, C)

        if expected != got:
            raise AssertionError((A, B, C, expected, got))


if __name__ == "__main__":
    if SELF_TEST:
        _self_test()
    else:
        main()