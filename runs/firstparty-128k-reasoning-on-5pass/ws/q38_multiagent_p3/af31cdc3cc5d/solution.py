import sys
import heapq


def prefix_f(seq, n):
    low = []
    high = []
    sl = 0
    sh = 0
    ll = 0
    hh = 0
    F = [0] * (n // 2 + 1)

    heappush = heapq.heappush
    heappop = heapq.heappop

    it = iter(seq)
    nxt = it.__next__
    idx = 0

    for i in range(1, n + 1):
        x = nxt()

        if ll == 0 or x <= -low[0]:
            heappush(low, -x)
            sl += x
            ll += 1
        else:
            heappush(high, x)
            sh += x
            hh += 1

        if ll > hh + 1:
            v = -heappop(low)
            sl -= v
            ll -= 1
            heappush(high, v)
            sh += v
            hh += 1
        elif hh > ll:
            v = heappop(high)
            sh -= v
            hh -= 1
            heappush(low, -v)
            sl += v
            ll += 1

        if (i & 1) == 0:
            idx += 1
            F[idx] = sh - sl

    return F


def solve_array(a):
    n = len(a)
    F = prefix_f(a, n)

    if n % 2 == 0:
        return F[n // 2]

    R = prefix_f(reversed(a), n)
    best = 0

    # F[k] pairs with R[M-k], where M = n // 2.
    for fk, rk in zip(F, reversed(R)):
        v = fk + rk
        if v > best:
            best = v

    return best


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    del data
    print(solve_array(a))


def brute_force(a):
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dfs(t):
        l = len(t)
        if l <= 1:
            return 0
        best = 0
        for i in range(l - 1):
            cand = abs(t[i] - t[i + 1]) + dfs(t[:i] + t[i + 2:])
            if cand > best:
                best = cand
        return best

    return dfs(tuple(a))


def run_selftest():
    import random

    assert solve_array([1, 2, 5, 3]) == 5
    assert solve_array([3, 1, 4, 1, 5, 9, 2]) == 14
    assert solve_array([1, 1, 1, 1, 1]) == 0

    base = [1, 2, 3, 4, 5, 6, 7, 8]
    for n in range(2, 9):
        patterns = [
            base[:n],
            base[::-1][:n],
            [1, 1, 2, 2, 3, 3, 4, 4][:n],
            [1, 2, 1, 2, 1, 2, 1, 2][:n],
            [5] * n,
        ]
        for a in patterns:
            if len(a) == n:
                expected = brute_force(a)
                got = solve_array(a)
                if expected != got:
                    print("FAIL", n, a, expected, got)
                    return

    random.seed(12345)
    for _ in range(500):
        n = random.randint(2, 8)
        r = random.random()
        if r < 0.2:
            a = [1] * n
        elif r < 0.5:
            a = [random.randint(1, 3) for _ in range(n)]
        else:
            a = [random.randint(1, 10) for _ in range(n)]

        expected = brute_force(a)
        got = solve_array(a)
        if expected != got:
            print("FAIL", n, a, expected, got)
            return

    print("selftest ok")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        run_selftest()
    else:
        solve()