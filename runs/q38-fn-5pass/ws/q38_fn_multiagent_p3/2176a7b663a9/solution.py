import sys
import heapq
import random

INF = 10**30


def build_lr_small(n, W, L, R):
    maxC = max(max(L), max(R), 1) + 5
    left = [INF] * (maxC + 2)
    right = [INF] * (maxC + 2)
    for i in range(n):
        if W[i] < left[R[i]]:
            left[R[i]] = W[i]
        if W[i] < right[L[i]]:
            right[L[i]] = W[i]
    for x in range(1, maxC + 2):
        if left[x - 1] < left[x]:
            left[x] = left[x - 1]
    for x in range(maxC, -1, -1):
        if right[x + 1] < right[x]:
            right[x] = right[x + 1]
    return left, right


def formula_small(n, W, L, R):
    left, right = build_lr_small(n, W, L, R)
    res = [[INF] * n for _ in range(n)]
    for i in range(n):
        res[i][i] = W[i]
        for j in range(n):
            if i == j:
                continue
            if R[i] < L[j] or R[j] < L[i]:
                res[i][j] = W[i] + W[j]
            else:
                mn = INF
                v = left[min(L[i], L[j]) - 1]
                if v < mn:
                    mn = v
                v = right[max(R[i], R[j]) + 1]
                if v < mn:
                    mn = v

                a = left[L[i] - 1]
                b = right[R[j] + 1]
                if a < INF and b < INF:
                    v = a + b
                    if v < mn:
                        mn = v

                a = right[R[i] + 1]
                b = left[L[j] - 1]
                if a < INF and b < INF:
                    v = a + b
                    if v < mn:
                        mn = v

                if mn < INF:
                    res[i][j] = W[i] + W[j] + mn
    return res


def exact_small(n, W, L, R):
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if R[i] < L[j] or R[j] < L[i]:
                adj[i].append(j)
                adj[j].append(i)

    res = []
    for s in range(n):
        dist = [INF] * n
        dist[s] = W[s]
        heap = [(W[s], s)]
        while heap:
            d, u = heapq.heappop(heap)
            if d != dist[u]:
                continue
            for v in adj[u]:
                nd = d + W[v]
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(heap, (nd, v))
        res.append(dist)
    return res


def check_case(n, W, L, R):
    ex = exact_small(n, W, L, R)
    fm = formula_small(n, W, L, R)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if ex[i][j] != fm[i][j]:
                return False, (n, W, L, R, i, j, ex[i][j], fm[i][j])
    return True, None


def run_validator():
    random.seed(12345)
    cases = []

    for _ in range(1000):
        n = random.randint(2, 8)
        W = [random.randint(1, 20) for _ in range(n)]
        L = []
        R = []
        for _ in range(n):
            l = random.randint(1, 2 * n)
            r = random.randint(l, 2 * n)
            L.append(l)
            R.append(r)
        cases.append((n, W, L, R))

    # Adversarial cases.
    cases.append((2, [1, 1], [1, 2], [2, 3]))
    cases.append((2, [1, 1], [1, 1], [2, 2]))
    cases.append((3, [1, 1, 1], [1, 2, 3], [6, 3, 5]))
    cases.append((4, [1, 1, 1, 1], [1, 5, 2, 4], [4, 8, 3, 5]))
    cases.append((4, [10, 1, 1, 10], [3, 1, 1, 4], [5, 3, 2, 5]))
    cases.append((5, [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [10, 10, 10, 10, 10]))
    cases.append((4, [1, 1, 1, 1], [1, 2, 3, 4], [2, 3, 4, 5]))
    cases.append((3, [1, 1, 1], [3, 1, 1], [5, 3, 2]))
    cases.append((3, [1, 1, 1], [1, 1, 1], [2, 2, 2]))
    cases.append((3, [1, 1, 1], [1, 2, 3], [1, 2, 3]))

    for idx, case in enumerate(cases):
        ok, info = check_case(*case)
        if not ok:
            print("FAIL", idx, info)
            return
    print("PASS")


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        run_validator()
        return

    it = iter(data)
    N = int(next(it))
    W = [0] + [int(next(it)) for _ in range(N)]

    L = [0] * (N + 1)
    R = [0] * (N + 1)

    maxC = 2 * N + 5
    left = [INF] * (maxC + 2)
    right = [INF] * (maxC + 2)

    for i in range(1, N + 1):
        l = int(next(it))
        r = int(next(it))
        L[i] = l
        R[i] = r
        if W[i] < left[r]:
            left[r] = W[i]
        if W[i] < right[l]:
            right[l] = W[i]

    # left[x] = minimum weight among intervals with R <= x
    for x in range(1, maxC + 2):
        if left[x - 1] < left[x]:
            left[x] = left[x - 1]

    # right[x] = minimum weight among intervals with L >= x
    for x in range(maxC, -1, -1):
        if right[x + 1] < right[x]:
            right[x] = right[x + 1]

    Q = int(next(it))
    out = []

    for _ in range(Q):
        s = int(next(it))
        t = int(next(it))

        ls = L[s]
        rs = R[s]
        lt = L[t]
        rt = R[t]
        base = W[s] + W[t]

        if rs < lt or rt < ls:
            out.append(str(base))
            continue

        mn = INF

        # Common neighbor strictly left of both.
        v = left[(ls if ls < lt else lt) - 1]
        if v < mn:
            mn = v

        # Common neighbor strictly right of both.
        v = right[(rs if rs > rt else rt) + 1]
        if v < mn:
            mn = v

        # Three-edge path: left of s, then right of t.
        a = left[ls - 1]
        b = right[rt + 1]
        if a < INF and b < INF:
            v = a + b
            if v < mn:
                mn = v

        # Three-edge path: right of s, then left of t.
        a = right[rs + 1]
        b = left[lt - 1]
        if a < INF and b < INF:
            v = a + b
            if v < mn:
                mn = v

        if mn == INF:
            out.append("-1")
        else:
            out.append(str(base + mn))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()