import sys
from collections import deque
import random


def formula_solve(N, A, B):
    # A and B are bytes.  Positions are 0-indexed.
    a = [i for i, c in enumerate(A) if c == 49]  # ord('1') == 49
    b = [i for i, c in enumerate(B) if c == 49]

    m = len(a)
    k = len(b)

    if m < k:
        return -1

    # D is the total required reduction of the span.
    D = (a[-1] - a[0]) - (b[-1] - b[0])
    if D < 0:
        return -1

    # Universal lower bound.
    E = max(abs(b[0] - a[0]), abs(b[-1] - a[-1]), (D + 1) // 2)

    # If there is only one target occupied square, there are no target gaps.
    if k == 1:
        return E

    mk = k - 1
    G = [a[i + 1] - a[i] for i in range(m - 1)]
    H = [b[i + 1] - b[i] for i in range(mk)]

    # 1) Try to match every target gap to a strictly larger initial gap.
    #    Then no exact gap exists, and the lower bound E is attainable.
    j = 0
    for g in G:
        if g > H[j]:
            j += 1
            if j == mk:
                return E

    # 2) Otherwise, all exact gaps must have the same displacement parity.
    #    For each parity p, greedily test whether H can be matched using:
    #      - strict matches g > h, or
    #      - exact matches g == h whose displacement parity is p.
    ans = -1
    for p in (0, 1):
        j = 0
        for i, g in enumerate(G):
            h = H[j]
            if g > h or (g == h and ((b[j] - a[i]) & 1) == p):
                j += 1
                if j == mk:
                    cand = E if (E & 1) == p else E + 1
                    if ans == -1 or cand < ans:
                        ans = cand
                    break

    return ans


# ----------------------------------------------------------------------
# Brute-force BFS oracle for tiny N, used only by the validation harness.
# ----------------------------------------------------------------------
def bfs_solve(N, A, B):
    init = tuple(1 if c == 49 else 0 for c in A)
    goal = tuple(1 if c == 49 else 0 for c in B)

    def occ(state):
        return tuple(1 if v > 0 else 0 for v in state)

    if occ(init) == goal:
        return 0

    q = deque([init])
    dist = {init: 0}

    while q:
        st = q.popleft()
        nd = dist[st] + 1

        for c in range(N):
            new = [0] * N
            for x, cnt in enumerate(st):
                if cnt:
                    if c > x:
                        nx = x + 1
                    elif c < x:
                        nx = x - 1
                    else:
                        nx = x
                    new[nx] += cnt

            ns = tuple(new)
            if ns not in dist:
                if occ(ns) == goal:
                    return nd
                dist[ns] = nd
                q.append(ns)

    return -1


def mask_to_bytes(mask, N):
    return bytes(49 if (mask >> i) & 1 else 48 for i in range(N))


def run_validation():
    mismatches = []

    # Exhaustive for N <= 5.
    for N in range(1, 6):
        strs = [mask_to_bytes(mask, N) for mask in range(1, 1 << N)]
        for A in strs:
            for B in strs:
                f = formula_solve(N, A, B)
                bfs = bfs_solve(N, A, B)
                if f != bfs:
                    mismatches.append((N, A.decode(), B.decode(), f, bfs))

    # Randomized for N <= 6.
    random.seed(12345)
    for _ in range(1000):
        N = random.randint(1, 6)
        A = mask_to_bytes(random.randrange(1, 1 << N), N)
        B = mask_to_bytes(random.randrange(1, 1 << N), N)
        f = formula_solve(N, A, B)
        bfs = bfs_solve(N, A, B)
        if f != bfs:
            mismatches.append((N, A.decode(), B.decode(), f, bfs))

    if mismatches:
        print("counterexamples found")
        for x in mismatches[:50]:
            print(x)
    else:
        print("no counterexamples found")


def solve_input(data):
    t = int(data[0])
    idx = 1
    out = []

    for _ in range(t):
        N = int(data[idx])
        A = data[idx + 1]
        B = data[idx + 2]
        idx += 3
        out.append(str(formula_solve(N, A, B)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    data = sys.stdin.buffer.read().split()
    if not data:
        run_validation()
    elif data[0] == b"VALIDATE":
        run_validation()
    else:
        solve_input(data)