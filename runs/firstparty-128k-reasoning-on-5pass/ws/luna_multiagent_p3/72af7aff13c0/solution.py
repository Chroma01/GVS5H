import sys

MOD = 998244353


def make_row(values, s):
    mat = [0] * (s * s)
    for k in range(s):
        cur = values[k]
        mat[k * s + k] = cur
        for j in range(k + 1, s):
            cur = cur * values[j] % MOD
            mat[j * s + k] = cur
    return mat


def mat_mul(a, b, s):
    c = [0] * (s * s)
    for i in range(s):
        ib = i * s
        for k in range(i + 1):
            x = a[ib + k]
            if x:
                kb = k * s
                for j in range(k + 1):
                    c[ib + j] = (c[ib + j] + x * b[kb + j]) % MOD
    return c


def solve_small(H, W, grid, queries):
    transposed = H < W
    if transposed:
        length, width = W, H
    else:
        length, width = H, W

    size = 1
    while size < length:
        size <<= 1

    identity = [0] * (width * width)
    for i in range(width):
        identity[i * width + i] = 1

    tree = [identity[:] for _ in range(2 * size)]

    for r in range(length):
        vals = [0] * width
        if transposed:
            for c in range(width):
                vals[c] = grid[c * W + r]
        else:
            base = r * W
            for c in range(width):
                vals[c] = grid[base + c]
        tree[size + r] = make_row(vals, width)

    for p in range(size - 1, 0, -1):
        tree[p] = mat_mul(tree[p << 1 | 1], tree[p << 1], width)

    answers = []

    for _, value, r, c in queries:
        grid[r * W + c] = value

        rr = c if transposed else r
        vals = [0] * width
        if transposed:
            for j in range(width):
                vals[j] = grid[j * W + rr]
        else:
            base = rr * W
            for j in range(width):
                vals[j] = grid[base + j]

        p = size + rr
        tree[p] = make_row(vals, width)
        p >>= 1
        while p:
            tree[p] = mat_mul(tree[p << 1 | 1], tree[p << 1], width)
            p >>= 1

        answers.append(str(tree[1][(width - 1) * width] % MOD))

    return answers


def solve_block(H, W, grid, queries):
    n = H * W
    q = len(queries)
    block_size = 320
    answers = []

    for block_start in range(0, q, block_size):
        block_end = min(q, block_start + block_size)

        r1, c1 = H, W
        r2, c2 = -1, -1
        for k in range(block_start, block_end):
            r, c, _ = queries[k]
            if r < r1:
                r1 = r
            if r > r2:
                r2 = r
            if c < c1:
                c1 = c
            if c > c2:
                c2 = c

        height = r2 - r1 + 1
        width = c2 - c1 + 1

        forward = [0] * W
        top = [0] * width
        left = [0] * height
        total = 0

        for r in range(H):
            base = r * W
            for c in range(W):
                if r == 0 and c == 0:
                    forward[c] = grid[0]
                else:
                    ways = 0
                    if r:
                        ways += forward[c]
                    if c:
                        ways += forward[c - 1]
                    forward[c] = grid[base + c] * ways % MOD

            if r == r1 - 1:
                for j in range(width):
                    top[j] = forward[c1 + j]
            if r1 <= r <= r2 and c1:
                left[r - r1] = forward[c1 - 1]

            if r == H - 1:
                total = forward[W - 1]

        bottom = [0] * width
        right = [0] * height
        backward = [0] * W

        for r in range(H - 1, -1, -1):
            base = r * W
            for c in range(W - 1, -1, -1):
                if r == H - 1 and c == W - 1:
                    backward[c] = grid[n - 1]
                else:
                    ways = 0
                    if r + 1 < H:
                        ways += backward[c]
                    if c + 1 < W:
                        ways += backward[c + 1]
                    backward[c] = grid[base + c] * ways % MOD

            if r == r2 + 1:
                for j in range(width):
                    bottom[j] = backward[c1 + j]
            if r1 <= r <= r2 and c2 + 1 < W:
                right[r - r1] = backward[c2 + 1]

        inside = [[0] * width for _ in range(height)]

        def rebuild(si, sj):
            for i in range(si, height):
                rr = r1 + i
                row = inside[i]
                base = rr * W

                for j in range(sj, width):
                    cc = c1 + j

                    if rr == 0 and cc == 0:
                        row[j] = grid[0]
                        continue

                    ways = 0
                    if i:
                        ways += inside[i - 1][j]
                    elif r1:
                        ways += top[j]

                    if j:
                        ways += row[j - 1]
                    elif c1:
                        ways += left[i]

                    row[j] = grid[base + cc] * ways % MOD

        rebuild(0, 0)

        def crossing():
            result = 0

            if r2 + 1 < H:
                last = inside[-1]
                for j in range(width):
                    result += last[j] * bottom[j]

            if c2 + 1 < W:
                j = width - 1
                for i in range(height):
                    result += inside[i][j] * right[i]

            if r2 == H - 1 and c2 == W - 1:
                result += inside[-1][-1]

            return result % MOD

        old_crossing = crossing()

        for k in range(block_start, block_end):
            r, c, value = queries[k]
            grid[r * W + c] = value

            rebuild(r - r1, c - c1)
            new_crossing = crossing()

            answers.append(str((total - old_crossing + new_crossing) % MOD))

    return answers


def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    H = int(next(it))
    W = int(next(it))
    grid = [int(next(it)) for _ in range(H * W)]

    Q = int(next(it))
    r = int(next(it)) - 1
    c = int(next(it)) - 1

    queries = []
    for _ in range(Q):
        direction = next(it)
        value = int(next(it))

        if direction == b"L":
            c -= 1
        elif direction == b"R":
            c += 1
        elif direction == b"U":
            r -= 1
        else:
            r += 1

        queries.append((r, c, value))

    if min(H, W) <= 6:
        answers = solve_small(H, W, grid, queries)
    else:
        answers = solve_block(H, W, grid, queries)

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()