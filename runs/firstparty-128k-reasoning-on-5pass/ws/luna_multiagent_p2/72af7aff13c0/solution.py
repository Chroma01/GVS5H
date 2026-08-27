import sys

MOD = 998244353
BLOCK = 46


def solve():
    input = sys.stdin.buffer.readline

    H, W = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(H)]

    Q, sh, sw = map(int, input().split())
    h, w = sh - 1, sw - 1

    ops = []
    positions = []

    for _ in range(Q):
        d, x = input().split()
        x = int(x)

        if d == b"L":
            w -= 1
        elif d == b"R":
            w += 1
        elif d == b"U":
            h -= 1
        else:
            h += 1

        ops.append((h, w, x))
        positions.append((h, w))

    answers = []

    for left in range(0, Q, BLOCK):
        right = min(Q, left + BLOCK)

        r0, c0 = H, W
        r1, c1 = -1, -1

        for i in range(left, right):
            r, c = positions[i]
            if r < r0:
                r0 = r
            if r > r1:
                r1 = r
            if c < c0:
                c0 = c
            if c > c1:
                c1 = c

        pre = [[0] * W for _ in range(H)]
        for r in range(H):
            ar = a[r]
            pr = pre[r]
            for c in range(W):
                if r == 0 and c == 0:
                    pr[c] = ar[c]
                else:
                    s = 0
                    if r:
                        s += pre[r - 1][c]
                    if c:
                        s += pr[c - 1]
                    pr[c] = ar[c] * s % MOD

        suf = [[0] * W for _ in range(H)]
        for r in range(H - 1, -1, -1):
            ar = a[r]
            sr = suf[r]
            for c in range(W - 1, -1, -1):
                if r == H - 1 and c == W - 1:
                    s = 1
                else:
                    s = 0
                    if r + 1 < H:
                        s += suf[r + 1][c]
                    if c + 1 < W:
                        s += sr[c + 1]
                sr[c] = ar[c] * s % MOD

        local = [
            pre[r][c0:c1 + 1]
            for r in range(r0, r1 + 1)
        ]
        local_h = r1 - r0 + 1
        local_w = c1 - c0 + 1

        def through_box():
            if r1 == H - 1 and c1 == W - 1:
                return local[-1][-1]

            total = 0

            if r1 < H - 1:
                suffix_row = suf[r1 + 1]
                last_local_row = local[-1]
                for c in range(c0, c1 + 1):
                    total += last_local_row[c - c0] * suffix_row[c]

            if c1 < W - 1:
                right_col = c1 + 1
                last_local_col = local_w - 1
                for r in range(r0, r1 + 1):
                    total += local[r - r0][last_local_col] * suf[r][right_col]

            return total % MOD

        unchanged = (pre[H - 1][W - 1] - through_box()) % MOD

        for i in range(left, right):
            r, c, value = ops[i]
            a[r][c] = value

            for rr in range(r, r1 + 1):
                lr = rr - r0
                row = local[lr]

                for cc in range(c, c1 + 1):
                    lc = cc - c0

                    if rr == 0 and cc == 0:
                        row[lc] = a[rr][cc]
                        continue

                    ways = 0

                    if rr:
                        if rr == r0:
                            ways += pre[rr - 1][cc]
                        else:
                            ways += local[lr - 1][lc]

                    if cc:
                        if cc == c0:
                            ways += pre[rr][cc - 1]
                        else:
                            ways += row[lc - 1]

                    row[lc] = a[rr][cc] * ways % MOD

            answers.append(str((unchanged + through_box()) % MOD))

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()