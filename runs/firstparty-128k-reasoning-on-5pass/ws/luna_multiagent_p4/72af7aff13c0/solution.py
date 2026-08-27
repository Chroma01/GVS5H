import sys
import math

MOD = 998244353


def solve():
    input = sys.stdin.buffer.readline

    H, W = map(int, input().split())
    N = H * W

    grid = []
    for _ in range(H):
        grid.extend(map(int, input().split()))

    Q, sh, sw = map(int, input().split())
    r, c = sh - 1, sw - 1

    queries = []
    for _ in range(Q):
        d, a = input().split()
        queries.append((d, int(a)))

    block_size = max(1, int(math.sqrt(N)))

    blocked = bytearray(N)
    forward = [0] * N
    backward = [0] * N
    answers = []

    for left in range(0, Q, block_size):
        right = min(Q, left + block_size)

        touched = []
        seen = {}

        tr, tc = r, c
        for qi in range(left, right):
            d, _ = queries[qi]
            if d == b"L":
                tc -= 1
            elif d == b"R":
                tc += 1
            elif d == b"U":
                tr -= 1
            else:
                tr += 1

            p = tr * W + tc
            if p not in seen:
                seen[p] = len(touched)
                touched.append(p)

        for p in touched:
            blocked[p] = 1

        for i in range(H):
            base = i * W
            for j in range(W):
                p = base + j

                if blocked[p]:
                    forward[p] = 0
                    continue

                if i == 0 and j == 0:
                    forward[p] = grid[p] % MOD
                    continue

                s = 0
                if i:
                    s += forward[p - W]
                if j:
                    s += forward[p - 1]

                forward[p] = (s % MOD) * grid[p] % MOD

        for i in range(H - 1, -1, -1):
            base = i * W
            for j in range(W - 1, -1, -1):
                p = base + j

                if blocked[p]:
                    backward[p] = 0
                    continue

                if i == H - 1 and j == W - 1:
                    backward[p] = grid[p] % MOD
                    continue

                s = 0
                if i + 1 < H:
                    s += backward[p + W]
                if j + 1 < W:
                    s += backward[p + 1]

                backward[p] = (s % MOD) * grid[p] % MOD

        baseline = forward[N - 1]

        touched.sort(key=lambda p: (p // W + p % W, p))
        k = len(touched)
        index = {p: i for i, p in enumerate(touched)}

        entry = [0] * k
        exit_weight = [0] * k

        for z, p in enumerate(touched):
            i, j = divmod(p, W)

            s = 0
            if i == 0 and j == 0:
                s = 1
            else:
                if i:
                    q = p - W
                    if not blocked[q]:
                        s += forward[q]
                if j:
                    q = p - 1
                    if not blocked[q]:
                        s += forward[q]

            entry[z] = s % MOD

            s = 0
            if i == H - 1 and j == W - 1:
                s = 1
            else:
                if i + 1 < H:
                    q = p + W
                    if not blocked[q]:
                        s += backward[q]
                if j + 1 < W:
                    q = p + 1
                    if not blocked[q]:
                        s += backward[q]

            exit_weight[z] = s % MOD

        max_row = max(p // W for p in touched)
        max_col = max(p % W for p in touched)

        transition = [[0] * k for _ in range(k)]

        for sid, source in enumerate(touched):
            sr, sc = divmod(source, W)
            dp = {}

            for i in range(sr, max_row + 1):
                base = i * W
                for j in range(sc, max_col + 1):
                    p = base + j

                    if p == source:
                        cur = 1
                    else:
                        cur = dp.get(p, 0)

                    if cur == 0:
                        continue

                    if i + 1 <= max_row:
                        q = p + W
                        if blocked[q]:
                            tid = index.get(q)
                            if tid is not None:
                                transition[sid][tid] += cur
                                if transition[sid][tid] >= MOD:
                                    transition[sid][tid] -= MOD
                        else:
                            dp[q] = (dp.get(q, 0) + cur * grid[q]) % MOD

                    if j + 1 <= max_col:
                        q = p + 1
                        if blocked[q]:
                            tid = index.get(q)
                            if tid is not None:
                                transition[sid][tid] += cur
                                if transition[sid][tid] >= MOD:
                                    transition[sid][tid] -= MOD
                        else:
                            dp[q] = (dp.get(q, 0) + cur * grid[q]) % MOD

        through = [0] * k

        for qi in range(left, right):
            d, value = queries[qi]

            if d == b"L":
                c -= 1
            elif d == b"R":
                c += 1
            elif d == b"U":
                r -= 1
            else:
                r += 1

            p = r * W + c
            grid[p] = value

            for v in range(k):
                total = entry[v]
                for u in range(k):
                    total += through[u] * transition[u][v]
                through[v] = grid[touched[v]] * (total % MOD) % MOD

            result = baseline
            for z in range(k):
                result += through[z] * exit_weight[z]

            answers.append(str(result % MOD))

        for p in touched:
            blocked[p] = 0

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()