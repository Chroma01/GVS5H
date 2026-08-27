import sys

MOD = 998244353


def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    H = int(next(it))
    W = int(next(it))
    N = H * W

    a = [int(next(it)) for _ in range(N)]

    Q = int(next(it))
    r = int(next(it)) - 1
    c = int(next(it)) - 1

    updates = []
    for _ in range(Q):
        d = next(it)
        value = int(next(it))

        if d == b"L":
            c -= 1
        elif d == b"R":
            c += 1
        elif d == b"U":
            r -= 1
        else:
            r += 1

        updates.append((r, c, value))

    def rebuild():
        f = [0] * N
        for i in range(H):
            base = i * W
            for j in range(W):
                p = base + j
                if i == 0 and j == 0:
                    f[p] = a[p]
                else:
                    s = 0
                    if i:
                        s += f[p - W]
                    if j:
                        s += f[p - 1]
                    f[p] = a[p] * s % MOD

        g = [0] * N
        for i in range(H - 1, -1, -1):
            base = i * W
            for j in range(W - 1, -1, -1):
                p = base + j
                if i == H - 1 and j == W - 1:
                    g[p] = a[p]
                else:
                    s = 0
                    if i + 1 < H:
                        s += g[p + W]
                    if j + 1 < W:
                        s += g[p + 1]
                    g[p] = a[p] * s % MOD

        return f, g

    candidates = [16, 24, 32, 48, 64, 80, 96, 128, 160, 224, 320, 448]
    candidates = [b for b in candidates if b <= Q]
    if not candidates:
        candidates = [Q]

    best_b = candidates[0]
    best_cost = None

    for B in candidates:
        cost = 0

        for start in range(0, Q, B):
            end = min(Q, start + B)

            min_r = H
            max_r = -1
            min_c = W
            max_c = -1

            for k in range(start, end):
                x, y, _ = updates[k]
                min_r = min(min_r, x)
                max_r = max(max_r, x)
                min_c = min(min_c, y)
                max_c = max(max_c, y)

            rh = max_r - min_r + 1
            rw = max_c - min_c + 1

            cost += N + rh * rw + (end - start) * (rh + rw)

            for k in range(start, end):
                x, y, _ = updates[k]
                cost += (max_r - x + 1) * (max_c - y + 1)

        if best_cost is None or cost < best_cost:
            best_cost = cost
            best_b = B

    B = best_b
    f, g = rebuild()
    answer = f[N - 1]
    out = []

    for block_start in range(0, Q, B):
        block_end = min(Q, block_start + B)

        min_r = H
        max_r = -1
        min_c = W
        max_c = -1

        for k in range(block_start, block_end):
            x, y, _ = updates[k]
            min_r = min(min_r, x)
            max_r = max(max_r, x)
            min_c = min(min_c, y)
            max_c = max(max_c, y)

        rh = max_r - min_r + 1
        rw = max_c - min_c + 1
        area = rh * rw

        local = [0] * area
        for x in range(rh):
            src = (min_r + x) * W + min_c
            dst = x * rw
            local[dst:dst + rw] = f[src:src + rw]

        def rectangle_contribution():
            if max_r == H - 1 and max_c == W - 1:
                return local[(rh - 1) * rw + rw - 1]

            res = 0

            if max_r + 1 < H:
                lp = (rh - 1) * rw
                gp = (max_r + 1) * W + min_c
                for y in range(rw):
                    res += local[lp + y] * g[gp + y]

            if max_c + 1 < W:
                for x in range(rh):
                    res += local[x * rw + rw - 1] * g[
                        (min_r + x) * W + max_c + 1
                    ]

            return res % MOD

        frozen_total = answer
        frozen_rectangle = rectangle_contribution()

        for k in range(block_start, block_end):
            gr, gc, value = updates[k]
            x0 = gr - min_r
            y0 = gc - min_c
            target = x0 * rw + y0
            gp = gr * W + gc

            old_local_value = local[target]

            pred = 0
            if x0:
                pred += local[target - rw]
            elif gr:
                pred += f[gp - W]

            if y0:
                pred += local[target - 1]
            elif gc:
                pred += f[gp - 1]

            a[gp] = value
            new_local_value = value * pred % MOD
            delta = (new_local_value - old_local_value) % MOD
            local[target] = new_local_value

            dh = rh - x0
            dw = rw - y0
            diff = [0] * (dh * dw)
            diff[0] = delta

            base_global = gr * W + gc

            for yy in range(1, dw):
                lp = x0 * rw + y0 + yy
                d = a[base_global + yy] * diff[yy - 1] % MOD
                diff[yy] = d
                local[lp] = (local[lp] + d) % MOD

            for xx in range(1, dh):
                local_row = (x0 + xx) * rw + y0
                global_row = (gr + xx) * W + gc
                diff_row = xx * dw
                prev_diff_row = (xx - 1) * dw

                d = a[global_row] * diff[prev_diff_row] % MOD
                diff[diff_row] = d
                local[local_row] = (local[local_row] + d) % MOD

                for yy in range(1, dw):
                    d = a[global_row + yy] * (
                        diff[prev_diff_row + yy] + diff[diff_row + yy - 1]
                    ) % MOD
                    diff[diff_row + yy] = d
                    p = local_row + yy
                    local[p] = (local[p] + d) % MOD

            current_rectangle = rectangle_contribution()
            out.append(str(
                (frozen_total - frozen_rectangle + current_rectangle) % MOD
            ))

        if block_end < Q:
            f, g = rebuild()
            answer = f[N - 1]

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()