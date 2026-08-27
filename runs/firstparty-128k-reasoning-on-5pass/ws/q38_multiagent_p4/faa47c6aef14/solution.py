import sys
from bisect import bisect_left


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(map(int, data))
    N = next(it)
    X = next(it) - 1

    A = [0] * N
    total_a = 0
    for i in range(N):
        v = next(it)
        A[i] = v
        total_a += v

    B = [0] * N
    total_b = 0
    for i in range(N):
        v = next(it)
        B[i] = v
        total_b += v

    inv_p = [0] * N
    for i in range(N):
        inv_p[next(it) - 1] = i

    inv_q = [0] * N
    for i in range(N):
        inv_q[next(it) - 1] = i

    data = None
    it = None

    def build_chain(inv, balls, total):
        nodes = []
        cur = X
        cycle_balls = balls[X]
        max_d = 0

        for d in range(1, N):
            cur = inv[cur]
            if cur == X:
                break
            nodes.append(cur)
            if balls[cur]:
                cycle_balls += balls[cur]
                max_d = d

        if total != cycle_balls:
            return None

        return nodes[:max_d][::-1]

    red = build_chain(inv_p, A, total_a)
    if red is None:
        print(-1)
        return

    blue = build_chain(inv_q, B, total_b)
    if blue is None:
        print(-1)
        return

    if not red or not blue:
        lcs = 0
    else:
        pos = [-1] * N
        for i, v in enumerate(red):
            pos[v] = i

        tails = []
        for v in blue:
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