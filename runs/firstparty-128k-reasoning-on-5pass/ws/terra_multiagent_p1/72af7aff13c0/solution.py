import sys

MOD = 998244353


def solve_small_width(H, W, A, updates):
    # Use columns when H is the small dimension; otherwise transpose conceptually
    if H <= W:
        K = H
        L = W

        def make_matrix(line):
            m = [[0] * K for _ in range(K)]
            prod = 1
            for j in range(K):
                prod = 1
                for i in range(j, K):
                    prod = prod * A[i * W + line] % MOD
                    m[i][j] = prod
            return m

        def line_of(r, c):
            return c
    else:
        K = W
        L = H

        def make_matrix(line):
            m = [[0] * K for _ in range(K)]
            for j in range(K):
                prod = 1
                for i in range(j, K):
                    prod = prod * A[line * W + i] % MOD
                    m[i][j] = prod
            return m

        def line_of(r, c):
            return r

    def multiply(a, b):
        # Returns a*b. Every matrix is lower triangular.
        res = [[0] * K for _ in range(K)]
        for i in range(K):
            ri = res[i]
            ai = a[i]
            for t in range(i + 1):
                x = ai[t]
                if x:
                    bt = b[t]
                    for j in range(t + 1):
                        ri[j] = (ri[j] + x * bt[j]) % MOD
        return res

    size = 1
    while size < L:
        size <<= 1

    ident = [[0] * K for _ in range(K)]
    for i in range(K):
        ident[i][i] = 1

    seg = [None] * (2 * size)
    for i in range(size):
        seg[size + i] = make_matrix(i) if i < L else ident

    for i in range(size - 1, 0, -1):
        # Applying left segment then right segment: right * left
        seg[i] = multiply(seg[i << 1 | 1], seg[i << 1])

    out = []
    for r, c, value in updates:
        A[r * W + c] = value
        p = size + line_of(r, c)
        seg[p] = make_matrix(line_of(r, c))
        p >>= 1
        while p:
            seg[p] = multiply(seg[p << 1 | 1], seg[p << 1])
            p >>= 1
        out.append(str(seg[1][K - 1][0]))

    sys.stdout.write("\n".join(out))


def solve_fallback(H, W, A, updates):
    n = H * W

    def build_forward():
        dp = [0] * n
        for i in range(H):
            base = i * W
            left = 0
            if i == 0:
                for j in range(W):
                    p = base + j
                    if j == 0:
                        left = A[p]
                    else:
                        left = left * A[p] % MOD
                    dp[p] = left
            else:
                above = base - W
                for j in range(W):
                    p = base + j
                    left = A[p] * (left + dp[above + j]) % MOD
                    dp[p] = left
        return dp

    def build_backward():
        dp = [0] * n
        for i in range(H - 1, -1, -1):
            base = i * W
            right = 0
            if i == H - 1:
                for j in range(W - 1, -1, -1):
                    p = base + j
                    if j == W - 1:
                        right = A[p]
                    else:
                        right = right * A[p] % MOD
                    dp[p] = right
            else:
                below = base + W
                for j in range(W - 1, -1, -1):
                    p = base + j
                    right = A[p] * (right + dp[below + j]) % MOD
                    dp[p] = right
        return dp

    q = len(updates)
    batches = []
    i = 0
    while i < q:
        r0 = r1 = updates[i][0]
        c0 = c1 = updates[i][1]
        j = i + 1

        while j < q:
            rr, cc, _ = updates[j]
            nr0 = min(r0, rr)
            nr1 = max(r1, rr)
            nc0 = min(c0, cc)
            nc1 = max(c1, cc)
            length = j - i + 1
            area = (nr1 - nr0 + 1) * (nc1 - nc0 + 1)

            if length * area > n and j > i + 1:
                break

            r0, r1, c0, c1 = nr0, nr1, nc0, nc1
            j += 1

        batches.append((i, j, r0, r1, c0, c1))
        i = j

    ans = []

    for lo, hi, r0, r1, c0, c1 in batches:
        forward = build_forward()
        backward = build_backward()
        initial_total = forward[-1]

        bh = r1 - r0 + 1
        bw = c1 - c0 + 1

        def rectangle_contribution():
            prev = [0] * bw
            right_exit = [0] * bh

            for ii in range(bh):
                rr = r0 + ii
                row_base = rr * W
                cur = [0] * bw
                left = 0

                for jj in range(bw):
                    cc = c0 + jj
                    pos = row_base + cc
                    incoming = 0

                    if rr == 0 and cc == 0:
                        incoming = 1
                    else:
                        if ii:
                            incoming += prev[jj]
                        elif rr:
                            incoming += forward[pos - W]

                        if jj:
                            incoming += left
                        elif cc:
                            incoming += forward[pos - 1]

                    left = A[pos] * (incoming % MOD) % MOD
                    cur[jj] = left

                right_exit[ii] = cur[-1]
                prev = cur

            if r0 <= H - 1 <= r1 and c0 <= W - 1 <= c1:
                return prev[W - 1 - c0]

            total = 0

            if r1 + 1 < H:
                below = (r1 + 1) * W
                for j in range(bw):
                    total += prev[j] * backward[below + c0 + j]

            if c1 + 1 < W:
                for i in range(bh):
                    total += right_exit[i] * backward[(r0 + i) * W + c1 + 1]

            return total % MOD

        fixed = (initial_total - rectangle_contribution()) % MOD

        for k in range(lo, hi):
            rr, cc, value = updates[k]
            A[rr * W + cc] = value
            ans.append(str((fixed + rectangle_contribution()) % MOD))

    sys.stdout.write("\n".join(ans))


def solve():
    input = sys.stdin.buffer.readline

    H, W = map(int, input().split())
    A = []
    for _ in range(H):
        A.extend(map(int, input().split()))

    Q, sh, sw = map(int, input().split())
    r = sh - 1
    c = sw - 1

    updates = []
    for _ in range(Q):
        d, x = input().split()
        if d == b"L":
            c -= 1
        elif d == b"R":
            c += 1
        elif d == b"U":
            r -= 1
        else:
            r += 1
        updates.append((r, c, int(x)))

    if min(H, W) <= 6:
        solve_small_width(H, W, A, updates)
    else:
        solve_fallback(H, W, A, updates)


if __name__ == "__main__":
    solve()