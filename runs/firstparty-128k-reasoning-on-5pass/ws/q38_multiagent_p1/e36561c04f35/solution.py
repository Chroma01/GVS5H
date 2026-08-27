import sys


def max_reward(vals, isS):
    """
    vals: run values, 0-indexed
    isS:  1 if the run is a singleton, 0 if heavy

    Returns the maximum number of P-savings achievable by a chain of
    P-moves and zero-cost Z-moves in this direction.
    """
    m = len(vals)
    if m <= 1:
        return 0

    NEG = -10**9
    best = [NEG] * (m + 1)
    z = [NEG] * (m + 1)
    p = [NEG] * (m + 1)
    best[0] = 0

    v = vals
    s = isS

    for i in range(m + 1):
        # Finalize best[i]: carry an inactive prefix forward, or stop an
        # active chain ending at i.
        if i:
            b = best[i - 1]
            if b > best[i]:
                best[i] = b
        if z[i] > best[i]:
            best[i] = z[i]
        if p[i] > best[i]:
            best[i] = p[i]

        if i == m:
            break
        if i + 1 >= m:
            continue
        if not (s[i] and s[i + 1]):
            continue

        # If the active value matches vals[i+1] and the two middle runs are
        # singletons:
        #   P is possible when vals[i+2] == vals[i]
        #   otherwise Z is possible.
        can_p = (i + 2 < m and v[i + 2] == v[i])

        # Active value vals[i-1]: start a new chain at run i-1.
        if i >= 1:
            val = best[i - 1]
            if val >= 0 and v[i - 1] == v[i + 1]:
                if can_p:
                    t = i + 3
                    nv = val + 1
                    if nv > p[t]:
                        p[t] = nv
                else:
                    t = i + 2
                    if val > z[t]:
                        z[t] = val

        # Active value vals[i-2]: last move was Z.
        if i >= 2:
            val = z[i]
            if val >= 0 and v[i - 2] == v[i + 1]:
                if can_p:
                    t = i + 3
                    nv = val + 1
                    if nv > p[t]:
                        p[t] = nv
                else:
                    t = i + 2
                    if val > z[t]:
                        z[t] = val

        # Active value vals[i-3]: last move was P.
        if i >= 3:
            val = p[i]
            if val >= 0 and v[i - 3] == v[i + 1]:
                if can_p:
                    t = i + 3
                    nv = val + 1
                    if nv > p[t]:
                        p[t] = nv
                else:
                    t = i + 2
                    if val > z[t]:
                        z[t] = val

    return best[m]


def answer_from_runs(vals, isS):
    m = len(vals)
    if m <= 1:
        return m

    r1 = max_reward(vals, isS)
    r2 = max_reward(vals[::-1], isS[::-1])
    return m - (r1 if r1 > r2 else r2)


def solve_case(A):
    vals = []
    isS = []
    for x in A:
        if vals and vals[-1] == x:
            if isS[-1]:
                isS[-1] = 0
        else:
            vals.append(x)
            isS.append(1)
    return answer_from_runs(vals, isS)


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    idx = 0
    T = data[idx]
    idx += 1
    out = []

    for _ in range(T):
        N = data[idx]
        idx += 1

        vals = []
        isS = []
        for _ in range(N):
            x = data[idx]
            idx += 1
            if vals and vals[-1] == x:
                if isS[-1]:
                    isS[-1] = 0
            else:
                vals.append(x)
                isS.append(1)

        out.append(str(answer_from_runs(vals, isS)))

    sys.stdout.write("\n".join(out))


def self_test():
    import itertools
    import random
    import heapq

    class ExactSmall:
        """
        Exact solver for all sequences of length <= maxN over alphabet 1..K.

        For each length n, deletion costs to shorter lengths are known.
        Then we run Dijkstra on the adjacent-swap graph of length-n states,
        with initial distances equal to "delete now" costs.
        """
        def __init__(self, K, maxN):
            self.K = K
            self.maxN = maxN
            self.dist = {(): 0}
            INF = 10**9

            for n in range(1, maxN + 1):
                states = list(itertools.product(range(1, K + 1), repeat=n))
                init = {}

                for st in states:
                    k = 1
                    while k < n and st[k] == st[0]:
                        k += 1

                    best = INF
                    for i in range(1, k + 1):
                        d = self.dist[st[i:]] + 1
                        if d < best:
                            best = d
                    init[st] = best

                dist = {}
                heap = []
                for st, d in init.items():
                    dist[st] = d
                    heap.append((d, st))
                heapq.heapify(heap)

                while heap:
                    d, st = heapq.heappop(heap)
                    if d != dist[st]:
                        continue

                    lst = list(st)
                    for i in range(n - 1):
                        if lst[i] != lst[i + 1]:
                            lst[i], lst[i + 1] = lst[i + 1], lst[i]
                            ns = tuple(lst)
                            nd = d + 1
                            old = dist.get(ns)
                            if old is None or nd < old:
                                dist[ns] = nd
                                heapq.heappush(heap, (nd, ns))
                            lst[i], lst[i + 1] = lst[i + 1], lst[i]

                self.dist.update(dist)

        def get(self, A):
            if len(A) > self.maxN:
                return None
            if A and max(A) > self.K:
                return None
            return self.dist.get(tuple(A))

    exact_cache = {}

    def get_exact(K, maxN):
        key = (K, maxN)
        if key not in exact_cache:
            exact_cache[key] = ExactSmall(K, maxN)
        return exact_cache[key]

    exact_by_K = {
        2: get_exact(2, 11),
        3: get_exact(3, 7),
        4: get_exact(4, 7),
    }

    def check(A, exact):
        e = exact.get(A)
        if e is None:
            K = max(2, max(A)) if A else 2
            exact = get_exact(K, len(A))
            e = exact.get(A)
        g = solve_case(A)
        if e != g:
            print("MISMATCH", A, "exact", e, "got", g)
            return False
        return True

    # Exhaustive small cases.
    for K, maxN in ((2, 11), (3, 7), (4, 7)):
        exact = exact_by_K[K]
        for n in range(2, maxN + 1):
            for tup in itertools.product(range(1, K + 1), repeat=n):
                if not check(list(tup), exact):
                    return

    # Regression cases and samples.
    regs = [
        [1, 2, 1, 3, 2, 3],
        [1, 2, 1, 3, 1, 3],
        [1, 2, 2, 2, 1, 2, 2, 1],
        [1, 1, 2, 1, 2],
        [4, 2, 1, 3],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
        [1, 2, 1, 2, 1, 2],
    ]
    for A in regs:
        K = max(2, max(A))
        exact = exact_by_K.get(K)
        if exact is None or len(A) > exact.maxN:
            exact = get_exact(K, len(A))
        if not check(A, exact):
            return

    # Random fuzz.
    rng = random.Random(12345)
    for _ in range(1000):
        n = rng.randint(2, 7)
        k = rng.randint(2, 4)
        A = [rng.randint(1, k) for _ in range(n)]
        K = max(2, k)
        if not check(A, exact_by_K[K]):
            return

    for _ in range(300):
        n = rng.randint(2, 11)
        A = [rng.randint(1, 2) for _ in range(n)]
        if not check(A, exact_by_K[2]):
            return

    print("self-test OK")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        self_test()
    else:
        solve()