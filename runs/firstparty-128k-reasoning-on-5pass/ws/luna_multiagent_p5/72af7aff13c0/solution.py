import sys
import math

MOD = 998244353


def solve():
    input = sys.stdin.buffer.readline

    h0, w0 = map(int, input().split())
    original = [list(map(int, input().split())) for _ in range(h0)]

    q, sh0, sw0 = map(int, input().split())
    sh0 -= 1
    sw0 -= 1

    if w0 <= h0:
        H, W = h0, w0
        grid = original
        sh, sw = sh0, sw0
        moves = {
            b"L": (0, -1),
            b"R": (0, 1),
            b"U": (-1, 0),
            b"D": (1, 0),
        }
    else:
        H, W = w0, h0
        grid = [list(row) for row in zip(*original)]
        sh, sw = sw0, sh0
        moves = {
            b"L": (-1, 0),
            b"R": (1, 0),
            b"U": (0, -1),
            b"D": (0, 1),
        }

    n = H * W

    candidates = set()
    x = max(1, int((n / 2) ** (1.0 / 3.0)))
    y = max(1, int(math.sqrt(2.0 * n / H)))
    for center in (x, y, 1):
        for d in range(-3, 4):
            candidates.add(max(1, center + d))
    candidates.add(q)

    def estimated_cost(b):
        rebuild = 2.0 * n / b
        local = min(H, b) * min(W, b)
        return rebuild + local

    block_size = min(q, min(candidates, key=estimated_cost))

    def make_dp(a):
        dp = [[0] * W for _ in range(H)]
        dp[0][0] = a[0][0]

        first = dp[0]
        source = a[0]
        for c in range(1, W):
            first[c] = first[c - 1] * source[c] % MOD

        for r in range(1, H):
            prev = dp[r - 1]
            cur = dp[r]
            ar = a[r]
            cur[0] = prev[0] * ar[0] % MOD
            left = cur[0]
            for c in range(1, W):
                left = (prev[c] + left) * ar[c] % MOD
                cur[c] = left

        return dp

    def make_suffix(a):
        suf = [[0] * W for _ in range(H)]
        last = H - 1
        cur = suf[last]
        ar = a[last]
        cur[W - 1] = ar[W - 1]
        right = cur[W - 1]
        for c in range(W - 2, -1, -1):
            right = ar[c] * right % MOD
            cur[c] = right

        for r in range(H - 2, -1, -1):
            cur = suf[r]
            nxt = suf[r + 1]
            ar = a[r]
            cur[W - 1] = ar[W - 1] * nxt[W - 1] % MOD
            right = cur[W - 1]
            for c in range(W - 2, -1, -1):
                right = ar[c] * (nxt[c] + right) % MOD
                cur[c] = right

        return suf

    def rectangle_exit(dp, suf, r1, r2, c1, c2):
        result = 0

        if r2 + 1 < H:
            row = dp[r2]
            after = suf[r2 + 1]
            for c in range(c1, c2 + 1):
                result += row[c] * after[c]

        if c2 + 1 < W:
            right_col = c2 + 1
            for r in range(r1, r2 + 1):
                result += dp[r][c2] * suf[r][right_col]

        if r2 == H - 1 and c2 == W - 1:
            result += dp[r2][c2]

        return result % MOD

    def local_answer(base_dp, base_suf, base_grid, changes,
                     r1, r2, c1, c2):
        height = r2 - r1 + 1
        width = c2 - c1 + 1
        local = [[0] * width for _ in range(height)]

        for i, r in enumerate(range(r1, r2 + 1)):
            row = local[i]
            base_row = base_grid[r]

            for j, c in enumerate(range(c1, c2 + 1)):
                if r == 0 and c == 0:
                    incoming = 1
                else:
                    incoming = 0

                    if r > 0:
                        if r > r1:
                            incoming += local[i - 1][j]
                        else:
                            incoming += base_dp[r - 1][c]

                    if c > 0:
                        if c > c1:
                            incoming += row[j - 1]
                        else:
                            incoming += base_dp[r][c - 1]

                idx = r * W + c
                value = changes.get(idx, base_row[c])
                row[j] = incoming % MOD * value % MOD

        modified = 0

        if r2 + 1 < H:
            row = local[r2 - r1]
            after = base_suf[r2 + 1]
            for c in range(c1, c2 + 1):
                modified += row[c - c1] * after[c]

        if c2 + 1 < W:
            right = width - 1
            right_col = c2 + 1
            for r in range(r1, r2 + 1):
                modified += local[r - r1][right] * base_suf[r][right_col]

        if r2 == H - 1 and c2 == W - 1:
            modified += local[H - 1 - r1][W - 1 - c1]

        modified %= MOD

        baseline = rectangle_exit(base_dp, base_suf, r1, r2, c1, c2)
        total = base_dp[H - 1][W - 1]
        return (total + modified - baseline) % MOD

    answers = []
    pos = 0

    while pos < q:
        end = min(q, pos + block_size)

        base_grid = grid
        base_dp = make_dp(base_grid)
        base_suf = make_suffix(base_grid)
        base_answer = base_dp[H - 1][W - 1]

        changes = {}
        min_r = H
        max_r = -1
        min_c = W
        max_c = -1

        for _ in range(pos, end):
            direction, value_bytes = input().split()
            value = int(value_bytes)

            dr, dc = moves[direction]
            sh += dr
            sw += dc

            idx = sh * W + sw
            changes[idx] = value

            if value != base_grid[sh][sw]:
                if sh < min_r:
                    min_r = sh
                if sh > max_r:
                    max_r = sh
                if sw < min_c:
                    min_c = sw
                if sw > max_c:
                    max_c = sw

            if max_r == -1:
                answers.append(str(base_answer))
            else:
                answers.append(str(local_answer(
                    base_dp, base_suf, base_grid, changes,
                    min_r, max_r, min_c, max_c
                )))

            grid[sh][sw] = value

        pos = end

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()