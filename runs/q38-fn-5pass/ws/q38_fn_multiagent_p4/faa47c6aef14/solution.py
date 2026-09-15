import sys
from bisect import bisect_left


def solve():
    it = iter(map(int, sys.stdin.buffer.read().split()))
    try:
        N = next(it)
    except StopIteration:
        return

    X = next(it) - 1

    A = [next(it) for _ in range(N)]
    B = [next(it) for _ in range(N)]

    invP = [0] * N
    for i in range(N):
        invP[next(it) - 1] = i

    invQ = [0] * N
    for i in range(N):
        invQ[next(it) - 1] = i

    def make_chain(inv, balls):
        # Mark the cycle containing X by walking backwards (inverse permutation).
        mark = bytearray(N)
        mark[X] = 1

        # back[k-1] is the vertex at distance k from X along the permutation.
        back = []
        cur = inv[X]
        while cur != X:
            mark[cur] = 1
            back.append(cur)
            cur = inv[cur]

        # Farthest occupied vertex distance.
        dmax = 0
        for k, v in enumerate(back, 1):
            if balls[v]:
                dmax = k

        # Any ball outside this cycle can never reach X.
        for i, b in enumerate(balls):
            if b and not mark[i]:
                return None

        if dmax == 0:
            return []

        # Required order: farthest -> ... -> closest to X, excluding X.
        return back[dmax - 1::-1]

    red = make_chain(invP, A)
    if red is None:
        print(-1)
        return

    blue = make_chain(invQ, B)
    if blue is None:
        print(-1)
        return

    # Original arrays are no longer needed.
    del A, B, invP, invQ

    if not red or not blue:
        print(len(red) + len(blue))
        return

    # LCS of two sequences with distinct elements:
    # map blue positions, then strict LIS over common positions in red order.
    pos = [-1] * N
    for i, v in enumerate(blue):
        pos[v] = i

    tails = []
    for v in red:
        p = pos[v]
        if p != -1:
            j = bisect_left(tails, p)
            if j == len(tails):
                tails.append(p)
            else:
                tails[j] = p

    lcs = len(tails)
    print(len(red) + len(blue) - lcs)


if __name__ == "__main__":
    solve()