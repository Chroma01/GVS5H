import sys
import heapq
import random
from bisect import bisect_right


# ---------------------------------------------------------------------------
# Fast O(N log N) solution
# ---------------------------------------------------------------------------
def solve(N, A, B, C):
    R = []          # A=1, B=0 -> must flip down once
    S = []          # A=0, B=1 -> must flip up once
    P = []          # A=1, B=1 -> optional "excursion": down then up
    for i in range(N):
        a = A[i]; b = B[i]; c = C[i]
        if a == 1 and b == 0:
            R.append(c)
        elif a == 0 and b == 1:
            S.append(c)
        elif a == 1 and b == 1:
            P.append(c)

    R.sort()
    S.sort()
    nR = len(R); nS = len(S)

    preR = [0] * (nR + 1)
    for i in range(nR):
        preR[i + 1] = preR[i] + R[i]
    preS = [0] * (nS + 1)
    for i in range(nS):
        preS[i + 1] = preS[i] + S[i]

    # pairwise sum of minimums inside a sorted (ascending) list
    PR = sum(R[i] * (nR - 1 - i) for i in range(nR))
    PS = sum(S[i] * (nS - 1 - i) for i in range(nS))

    WS = preS[nS]
    WP = sum(P)

    Const = PR + PS + WS + (nR + nS) * WP
    nm1 = nR + nS + 1

    P.sort(reverse=True)

    best = Const                       # k = 0 : choose no excursion
    a_pre = 0
    s_pre = 0
    t_pre = 0
    for i, c in enumerate(P, start=1):
        jr = bisect_right(R, c)
        g = preR[jr] + c * (nR - jr)
        js = bisect_right(S, c)
        g += preS[js] + c * (nS - js)
        a_pre += g - nm1 * c + 2 * WP
        s_pre += c
        t_pre += i * c
        tot = Const + a_pre - 2 * (i * s_pre - t_pre)
        if tot < best:
            best = tot
    return best


# ---------------------------------------------------------------------------
# Brute force: Dijkstra over all 2^N states
# edge u -> (u xor 1<<i), cost = weighted popcount of the destination
# ---------------------------------------------------------------------------
def brute(N, A, B, C):
    size = 1 << N
    start = 0
    target = 0
    for i in range(N):
        if A[i]:
            start |= 1 << i
        if B[i]:
            target |= 1 << i

    cost = [0] * size
    for s in range(1, size):
        lb = s & (-s)
        cost[s] = cost[s ^ lb] + C[lb.bit_length() - 1]

    INF = float('inf')
    dist = [INF] * size
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == target:
            return d
        for i in range(N):
            v = u ^ (1 << i)
            nd = d + cost[v]
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist[target]


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------
def validate():
    ok = True

    samples = [
        (4, [0, 1, 1, 1], [1, 0, 1, 0], [4, 6, 2, 9], 16),
        (5, [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], 0),
        (20,
         [1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0],
         [0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
         [52, 73, 97, 72, 54, 15, 79, 67, 13, 55, 65, 22, 36, 90, 84, 46, 1, 2, 27, 8],
         2867),
    ]
    for idx, (N, A, B, C, exp) in enumerate(samples, 1):
        got = solve(N, A, B, C)
        st = "OK" if got == exp else "FAIL"
        if got != exp:
            ok = False
        print("sample %d: got=%d expected=%d [%s]" % (idx, got, exp, st))

    # exhaustive small: N <= 4, all A,B, all C in {1,2,3}
    mism = 0
    for N in range(1, 5):
        for am in range(1 << N):
            A = [(am >> i) & 1 for i in range(N)]
            for bm in range(1 << N):
                B = [(bm >> i) & 1 for i in range(N)]
                for cm in range(3 ** N):
                    x = cm
                    C = []
                    for _ in range(N):
                        C.append(x % 3 + 1)
                        x //= 3
                    f = solve(N, A, B, C)
                    b = brute(N, A, B, C)
                    if f != b:
                        mism += 1
                        ok = False
                        if mism <= 5:
                            print("MISMATCH", N, A, B, C, "fast=", f, "brute=", b)
    print("exhaustive N<=4 done, mismatches =", mism)

    # random small cases (ties, all-equal C, empty classes, big values)
    rnd = 0
    random.seed(20240607)
    for t in range(3000):
        N = random.randint(1, 10)
        A = [random.randint(0, 1) for _ in range(N)]
        B = [random.randint(0, 1) for _ in range(N)]
        mode = t % 3
        if mode == 0:
            C = [random.randint(1, 4) for _ in range(N)]
        elif mode == 1:
            C = [random.randint(1, 10 ** 6) for _ in range(N)]
        else:
            C = [random.choice([1, 2, 3, 10 ** 6]) for _ in range(N)]
        f = solve(N, A, B, C)
        b = brute(N, A, B, C)
        if f != b:
            rnd += 1
            ok = False
            if rnd <= 5:
                print("MISMATCH", N, A, B, C, "fast=", f, "brute=", b)
    print("random tests done, mismatches =", rnd)
    print("ALL TESTS PASSED" if ok else "FAILURES DETECTED")


# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--validate":
        validate()
        return
    data = sys.stdin.buffer.read().split()
    if not data:          # no input -> run the self-validation suite
        validate()
        return
    pos = 0
    N = int(data[pos]); pos += 1
    A = [int(x) for x in data[pos:pos + N]]; pos += N
    B = [int(x) for x in data[pos:pos + N]]; pos += N
    C = [int(x) for x in data[pos:pos + N]]
    sys.stdout.write(str(solve(N, A, B, C)) + "\n")


main()