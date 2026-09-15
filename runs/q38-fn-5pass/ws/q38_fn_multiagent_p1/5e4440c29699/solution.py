import sys

MOD = 998244353


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    W, H, L, R, D, U = data
    mod = MOD

    # We need binomials up to about W+H+4.
    N = W + H + 5

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % mod

    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], mod - 2, mod)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % mod

    def C(n, k):
        if k < 0 or k > n:
            return 0
        return fact[n] * invfact[k] % mod * invfact[n - k] % mod

    # Number of monotone paths in full rectangle [0..w] x [0..h]
    # with arbitrary start and end.
    # Also equals prefix sum of paths_to(a,b) over 0<=a<=w, 0<=b<=h.
    def total_paths(w, h):
        if w < 0 or h < 0:
            return 0
        return (C(w + h + 4, w + 2) - w - h - 4 - (w + 1) * (h + 1)) % mod

    # Sum of paths_to(a,b) over rectangle a1..a2, b1..b2,
    # where paths_to(a,b) = number of paths ending at fixed point
    # (a,b) from arbitrary start in [0..a] x [0..b].
    def sum_paths_to(a1, a2, b1, b2):
        if a1 > a2 or b1 > b2:
            return 0
        return (
            total_paths(a2, b2)
            - total_paths(a1 - 1, b2)
            - total_paths(a2, b1 - 1)
            + total_paths(a1 - 1, b1 - 1)
        ) % mod

    # Count paths in the full grid whose start and end are both allowed.
    # Inclusion-exclusion over start/end being inside the forbidden rectangle.
    start_bad = sum_paths_to(W - R, W - L, H - U, H - D)
    end_bad = sum_paths_to(L, R, D, U)
    both_bad = total_paths(R - L, U - D)
    allowed = (total_paths(W, H) - start_bad - end_bad + both_bad) % mod

    # Subtract paths that visit the forbidden rectangle.
    # Split by unique first forbidden point: left side or bottom side.
    invalid = 0

    left_init = None
    bottom_init = None

    if L > 0:
        y = D
        left_init = (
            C(L + y + 1, L),
            C(W - L + H - y + 2, W - L + 1),
            C(R - L + U - y + 2, R - L + 1),
        )

    if D > 0:
        x = L
        bottom_init = (
            C(x + D + 1, x + 1),
            C(W - x + H - D + 2, W - x + 1),
            C(R - x + U - D + 2, R - x + 1),
        )

    if left_init is not None or bottom_init is not None:
        # If at least one boundary sum has length > 1, we need modular inverses
        # to update binomial coefficients in O(1) per step.
        need_inv = (left_init is not None and U > D) or (bottom_init is not None and R > L)

        if need_inv:
            # Convert fact in-place into a shifted inverse table:
            # inv[i-1] = modular inverse of i.
            for i in range(N, 0, -1):
                fact[i - 1] = fact[i - 1] * invfact[i] % mod
            del invfact

        inv = fact

        # First entry from the left side: (L-1,y) -> (L,y), D <= y <= U.
        if left_init is not None:
            c1, c2, c3 = left_init
            inv_local = inv
            LL = L
            WWL = W - L
            RRL = R - L
            HH = H
            UU = U
            DD = D
            s = 0

            for y in range(DD, UU):
                diff = c2 - c3
                if diff < 0:
                    diff += mod
                term = (c1 - 1) * diff % mod
                s += term
                if s >= mod:
                    s -= mod

                # c1 = C(L+y+1, L) -> C(L+y+2, L)
                c1 = c1 * (LL + y + 2) % mod * inv_local[y + 1] % mod
                # c2 = C(W-L+H-y+2, W-L+1) -> top decreases by 1
                c2 = c2 * (HH - y + 1) % mod * inv_local[WWL + HH - y + 1] % mod
                # c3 = C(R-L+U-y+2, R-L+1) -> top decreases by 1
                c3 = c3 * (UU - y + 1) % mod * inv_local[RRL + UU - y + 1] % mod

            diff = c2 - c3
            if diff < 0:
                diff += mod
            term = (c1 - 1) * diff % mod
            s += term
            if s >= mod:
                s -= mod

            invalid += s
            if invalid >= mod:
                invalid -= mod

        # First entry from the bottom side: (x,D-1) -> (x,D), L <= x <= R.
        if bottom_init is not None:
            b1, b2, b3 = bottom_init
            inv_local = inv
            LL = L
            RR = R
            DD = D
            UU = U
            WW = W
            HH = H
            s = 0

            for x in range(LL, RR):
                diff = b2 - b3
                if diff < 0:
                    diff += mod
                term = (b1 - 1) * diff % mod
                s += term
                if s >= mod:
                    s -= mod

                # b1 = C(x+D+1, x+1) -> C(x+D+2, x+2)
                b1 = b1 * (x + DD + 2) % mod * inv_local[x + 1] % mod
                # b2 = C(W-x+H-D+2, W-x+1) -> both top and bottom decrease by 1
                b2 = b2 * (WW - x + 1) % mod * inv_local[WW - x + HH - DD + 1] % mod
                # b3 = C(R-x+U-D+2, R-x+1) -> both top and bottom decrease by 1
                b3 = b3 * (RR - x + 1) % mod * inv_local[RR - x + UU - DD + 1] % mod

            diff = b2 - b3
            if diff < 0:
                diff += mod
            term = (b1 - 1) * diff % mod
            s += term
            if s >= mod:
                s -= mod

            invalid += s
            if invalid >= mod:
                invalid -= mod

    print((allowed - invalid) % mod)


if __name__ == "__main__":
    solve()