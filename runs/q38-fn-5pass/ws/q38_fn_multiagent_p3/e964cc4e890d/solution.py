import sys
import gc

MOD = 998244353


def main():
    gc.disable()
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    S = data[1]

    # Necessary boundary conditions.
    if S[0] != 66 or S[-1] != 87:  # 'B', 'W'
        print(0)
        return

    # Compressed bad events (I, H), strictly increasing in both coordinates.
    I = []
    H = []
    last_h = -1
    black = 0
    white = 0

    for c in S:
        if c == 66:  # 'B'
            if 1 <= black <= N - 1:
                h = white
                if h >= black and h > last_h:
                    I.append(black)
                    H.append(h)
                    last_h = h
            black += 1
        else:
            white += 1

    m = len(I)

    mod = MOD
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % mod

    if m == 0:
        print(fact[N])
        return

    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], mod - 2, mod)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % mod

    f = [0] * m
    contrib = [0] * m  # exact integer sums; reduced only when computing f[a]

    DIRECT_BLOCK = 64
    SMALL_M = 2000

    def direct_block(l, r):
        """Quadratic computation inside one small CDQ block."""
        prev_I = []
        prev_F = []
        fact_l = fact
        invfact_l = invfact
        I_l = I
        H_l = H
        contrib_l = contrib
        f_l = f
        mod_l = mod

        for a in range(l, r):
            ha = H_l[a]
            s = contrib_l[a]

            pI = prev_I
            pF = prev_F
            for j in range(len(pF)):
                s += pF[j] * fact_l[ha - pI[j]]

            fa = (-(fact_l[ha] + s) % mod_l) * invfact_l[ha - I_l[a]] % mod_l
            f_l[a] = fa

            if fa:
                pI.append(I_l[a])
                pF.append(fa)

    if m <= SMALL_M:
        direct_block(0, m)
    else:
        # Pack factorial values as 128-bit little-endian digits.
        # Base 2^128 is safe: every convolution coefficient is < N * MOD^2 < 2^128.
        fact_ba = bytearray(16 * (N + 1))
        mv = memoryview(fact_ba).cast("Q")
        for i, val in enumerate(fact):
            mv[2 * i] = val
        del mv
        fact_bytes = bytes(fact_ba)
        fact_mv = memoryview(fact_bytes)

        DIRECT_OPS = 15000

        def direct_add(mid, r, left_I, left_F):
            """Directly add contributions from a nonzero left list to right events."""
            ln = len(left_F)
            fact_l = fact
            contrib_l = contrib
            H_l = H

            if ln == 1:
                fb = left_F[0]
                ib = left_I[0]
                for a in range(mid, r):
                    contrib_l[a] += fb * fact_l[H_l[a] - ib]
                return

            for a in range(mid, r):
                ha = H_l[a]
                s = 0
                for j in range(ln):
                    s += left_F[j] * fact_l[ha - left_I[j]]
                if s:
                    contrib_l[a] += s

        def add_contrib(l, mid, r):
            """Add sum_{b in [l,mid)} f[b] * fact[H[a]-I[b]] to a in [mid,r)."""
            left_I = []
            left_F = []
            minI = N + 1
            maxI = -1

            I_l = I
            f_l = f
            for b in range(l, mid):
                fb = f_l[b]
                if fb:
                    ib = I_l[b]
                    left_I.append(ib)
                    left_F.append(fb)
                    if ib < minI:
                        minI = ib
                    if ib > maxI:
                        maxI = ib

            if not left_I:
                return

            right_count = r - mid
            ops = len(left_I) * right_count

            H_mid = H[mid]
            V = H[r - 1] - H_mid
            U = maxI - minI
            span = U + V + 1

            # Hybrid: direct for small work or very sparse value spans.
            if ops <= DIRECT_OPS or ops <= span * 2:
                direct_add(mid, r, left_I, left_F)
                return

            # Should not happen for valid compressed events, but keep a safe fallback.
            if H_mid < maxI:
                direct_add(mid, r, left_I, left_F)
                return

            # Build A[u] = f[b] at u = I[b] - minI.
            lenA = U + 1
            ba = bytearray(16 * lenA)
            mv = memoryview(ba).cast("Q")
            for j in range(len(left_I)):
                mv[2 * (left_I[j] - minI)] = left_F[j]
            A = int.from_bytes(ba, "little")
            del mv, ba

            if A == 0:
                return

            # B[s] = fact[min_idx + s], where min_idx = H_mid - maxI.
            min_idx = H_mid - maxI
            max_idx = H[r - 1] - minI
            B = int.from_bytes(
                fact_mv[min_idx * 16:(max_idx + 1) * 16],
                "little"
            )

            prod = A * B
            full_len = 2 * U + V + 1
            pb = prod.to_bytes(16 * full_len, "little")
            mv2 = memoryview(pb).cast("Q")

            contrib_l = contrib
            H_l = H
            for a in range(mid, r):
                pos = (U + H_l[a] - H_mid) << 1
                contrib_l[a] += mv2[pos] + (mv2[pos + 1] << 64)

        sys.setrecursionlimit(1_000_000)

        def cdq(l, r):
            if r - l <= DIRECT_BLOCK:
                direct_block(l, r)
                return
            mid = (l + r) >> 1
            cdq(l, mid)
            add_contrib(l, mid, r)
            cdq(mid, r)

        cdq(0, m)

    ans = fact[N]
    for a in range(m):
        ans = (ans + f[a] * fact[N - I[a]]) % mod

    print(ans)


if __name__ == "__main__":
    main()