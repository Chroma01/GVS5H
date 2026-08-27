import sys

MOD = 998244353


def solve():
    input = sys.stdin.buffer.readline

    H, W = map(int, input().split())
    A = []
    for _ in range(H):
        A.extend(map(int, input().split()))

    Q, sh, sw = map(int, input().split())
    r = sh - 1
    c = sw - 1

    qr = [0] * Q
    qc = [0] * Q
    qv = [0] * Q

    for i in range(Q):
        d, x = input().split()
        if d == b'L':
            c -= 1
        elif d == b'R':
            c += 1
        elif d == b'U':
            r -= 1
        else:
            r += 1
        qr[i] = r
        qc[i] = c
        qv[i] = int(x)

    n = H * W

    # Temporal block lengths for a four-level hierarchy.
    sizes = [
        max(1, int(n ** (15.0 / 31.0))),
        max(1, int(n ** (14.0 / 31.0))),
        max(1, int(n ** (12.0 / 31.0))),
        max(1, int(n ** (8.0 / 31.0))),
        1,
    ]
    for i in range(1, len(sizes)):
        if sizes[i] > sizes[i - 1]:
            sizes[i] = sizes[i - 1]
    sizes[-1] = 1

    fwd = [0] * n
    bwd = [0] * n
    output = []

    def bbox(left, right):
        r1 = r2 = qr[left]
        c1 = c2 = qc[left]
        for i in range(left + 1, right):
            x = qr[i]
            y = qc[i]
            if x < r1:
                r1 = x
            elif x > r2:
                r2 = x
            if y < c1:
                c1 = y
            elif y > c2:
                c2 = y
        return r1, r2, c1, c2

    def rebuild(r1, r2, c1, c2):
        # Recompute ordinary source-to-cell and cell-to-sink DPs in this
        # rectangle. Values just outside it remain valid.
        for rr in range(r1, r2 + 1):
            base = rr * W
            for cc in range(c1, c2 + 1):
                p = base + cc
                if rr == 0 and cc == 0:
                    fwd[p] = A[p]
                else:
                    v = 0
                    if rr:
                        v += fwd[p - W]
                    if cc:
                        v += fwd[p - 1]
                    if v >= MOD:
                        v -= MOD
                    fwd[p] = v * A[p] % MOD

        for rr in range(r2, r1 - 1, -1):
            base = rr * W
            for cc in range(c2, c1 - 1, -1):
                p = base + cc
                if rr == H - 1 and cc == W - 1:
                    bwd[p] = A[p]
                else:
                    v = 0
                    if rr + 1 < H:
                        v += bwd[p + W]
                    if cc + 1 < W:
                        v += bwd[p + 1]
                    if v >= MOD:
                        v -= MOD
                    bwd[p] = v * A[p] % MOD

    def point_contribution(rr, cc):
        # Total weight of all paths passing through (rr, cc), evaluated from
        # its neighboring fwd/bwd values, so division is never needed.
        p = rr * W + cc

        if rr == 0 and cc == 0:
            before = 1
        else:
            before = 0
            if rr:
                before += fwd[p - W]
            if cc:
                before += fwd[p - 1]
            if before >= MOD:
                before -= MOD

        if rr == H - 1 and cc == W - 1:
            after = 1
        else:
            after = 0
            if rr + 1 < H:
                after += bwd[p + W]
            if cc + 1 < W:
                after += bwd[p + 1]
            if after >= MOD:
                after -= MOD

        return before * A[p] % MOD * after % MOD

    def process(left, right, level, current_answer):
        if right - left == 1:
            rr = qr[left]
            cc = qc[left]
            p = rr * W + cc

            old = point_contribution(rr, cc)
            A[p] = qv[left]
            new = point_contribution(rr, cc)

            value = current_answer - old + new
            value %= MOD
            output.append(str(value))
            return value

        r1, r2, c1, c2 = bbox(left, right)

        step = sizes[level] if level < len(sizes) else 1
        length = right - left
        if step >= length:
            step = max(1, (length + 1) // 2)

        cur = current_answer
        pos = left
        first = True

        while pos < right:
            end = min(right, pos + step)

            # On entry to the first child, its DP values were already built
            # by the parent. Afterwards the preceding child changed cells in
            # this rectangle, requiring a fresh local rebuild.
            if not first:
                rebuild(r1, r2, c1, c2)
            first = False

            cur = process(pos, end, level + 1, cur)
            pos = end

        return cur

    rebuild(0, H - 1, 0, W - 1)
    current = fwd[-1]

    root_step = sizes[0]
    pos = 0
    first_root = True

    while pos < Q:
        end = min(Q, pos + root_step)

        if not first_root:
            rebuild(0, H - 1, 0, W - 1)
        first_root = False

        current = process(pos, end, 1, current)
        pos = end

    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    solve()