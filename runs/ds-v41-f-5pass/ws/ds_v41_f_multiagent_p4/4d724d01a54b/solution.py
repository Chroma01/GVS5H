import sys
import time
import heapq
import math
import itertools


def fast(n, perm):
    """O(N log N) greedy/Fenwick solution."""
    pos = [0] * (n + 1)
    for i, x in enumerate(perm):
        pos[x] = i + 1
    tree = [0] * (n + 1)
    ans = 0
    for v in range(1, n + 1):
        p = pos[v]
        s = 0
        j = p
        while j > 0:
            s += tree[j]
            j -= j & (-j)
        a = (v - 1) - s          # smaller values to the right of v
        ans += a * (2 * v - a - 1) // 2
        j = p
        while j <= n:
            tree[j] += 1
            j += j & (-j)
    return ans


def brute_all(n):
    """Single-source Dijkstra from identity over all n! permutations.
    Edges are symmetric (swap i,i+1 cost i both ways), so dist[P]
    equals the minimum cost to sort P."""
    start = tuple(range(1, n + 1))
    INF = 1 << 60
    dist = {start: 0}
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, INF):
            continue
        for i in range(n - 1):
            v = list(u)
            v[i], v[i + 1] = v[i + 1], v[i]
            v = tuple(v)
            nd = d + i + 1
            if nd < dist.get(v, INF):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


def verify():
    ok = True
    for n in range(2, 8):
        dist = brute_all(n)
        assert len(dist) == math.factorial(n), (n, len(dist))
        for perm in itertools.permutations(range(1, n + 1)):
            f = fast(n, list(perm))
            b = dist[perm]
            if f != b:
                print("MISMATCH n=%d perm=%s fast=%d brute=%d" % (n, perm, f, b))
                ok = False
                return ok
        print("n=%d: OK, %d permutations" % (n, len(dist)))

    # worst-case stress: reverse-sorted N = 2*10^5
    n = 200000
    perm = list(range(n, 0, -1))
    t = time.time()
    res = fast(n, perm)
    dt = time.time() - t
    exp = math.comb(n + 1, 3)
    print("worst-case reverse n=%d: ans=%d time=%.2fs expected C(n+1,3)=%d %s"
          % (n, res, dt, exp, "MATCH" if exp == res else "NO MATCH"))
    if exp != res:
        ok = False
    return ok


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        print("VERIFY:", "PASS" if verify() else "FAIL")
        return
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    P = list(map(int, data[1:1 + n]))
    print(fast(n, P))


main()