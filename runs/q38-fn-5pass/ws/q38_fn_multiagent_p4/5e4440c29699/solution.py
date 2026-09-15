import sys
from array import array

MOD = 998244353


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    W, H, L, R, D, U = map(int, data)
    mod = MOD
    N = W + H + 4

    # factorials and inverse factorials modulo MOD
    fact = array('I', [0]) * (N + 1)
    fact[0] = 1
    val = 1
    for i in range(1, N + 1):
        val = (val * i) % mod
        fact[i] = val

    invfact = array('I', [0]) * (N + 1)
    val = pow(fact[N], mod - 2, mod)
    invfact[N] = val
    for i in range(N, 0, -1):
        val = (val * i) % mod
        invfact[i - 1] = val

    def comb(n, k, fact=fact, invfact=invfact, mod=mod):
        if k < 0 or k > n:
            return 0
        return (fact[n] * invfact[k] % mod) * invfact[n - k] % mod

    # Sum_{0<=x<=X, 0<=y<=Y} C(x+y+2, x+1)
    def pref_end(x, y):
        if x < 0 or y < 0:
            return 0
        return (comb(x + y + 4, y + 2) - x - y - 4) % mod

    # Total monotone paths in a full (w+1) x (h+1) grid, arbitrary start/end.
    def total_paths(w, h):
        if w < 0 or h < 0:
            return 0
        return (pref_end(w, h) - (w + 1) * (h + 1)) % mod

    # Sum of C(x+y+2, x+1) over a rectangle.
    def rect_sum(x1, x2, y1, y2):
        if x1 > x2 or y1 > y2:
            return 0
        return (
            pref_end(x2, y2)
            - pref_end(x1 - 1, y2)
            - pref_end(x2, y1 - 1)
            + pref_end(x1 - 1, y1 - 1)
        ) % mod

    area = ((R - L + 1) * (U - D + 1)) % mod

    # Full-grid paths whose start and end are both outside the forbidden rectangle.
    a_all = total_paths(W, H)
    a_end = (rect_sum(L, R, D, U) - area) % mod
    a_start = (rect_sum(W - R, W - L, H - U, H - D) - area) % mod
    a_both = total_paths(R - L, U - D)
    full_out = (a_all - a_start - a_end + a_both) % mod

    invalid = 0

    # If the forbidden rectangle contains the origin, no outside path can enter it.
    # If it touches both top and right borders, no path that enters it can end outside.
    no_invalid = (L == 0 and D == 0) or (R == W and U == H)

    if not no_invalid:
        need_bottom = D > 0
        need_left = L > 0
        bottom_updates = need_bottom and (L < R)
        left_updates = need_left and (D < U)

        inv_local = []
        if bottom_updates or left_updates:
            max_den = 2
            if bottom_updates:
                max_den = max(
                    max_den,
                    R + 1,
                    W - L + H - D + 2,
                    R - L + U - D + 2,
                )
            if left_updates:
                max_den = max(
                    max_den,
                    U + 1,
                    W - L + H - D + 2,
                    R - L + U - D + 2,
                )

            inv = [0] * (max_den + 1)
            inv[1] = 1
            for i in range(2, max_den + 1):
                inv[i] = (mod - mod // i) * inv[mod % i] % mod
            inv_local = inv

        # First entry through the bottom edge: (x, D), previous point (x, D-1).
        if need_bottom:
            A = comb(L + D + 1, D)
            Q = comb(W - L + H - D + 2, H - D + 1)
            Inside = comb(R - L + U - D + 2, U - D + 1)

            cnt = R - L
            if cnt:
                a_num = L + D + 2
                a_den = L + 2
                q_num = W - L + 1
                q_den = W - L + H - D + 2
                i_num = R - L + 1
                i_den = R - L + U - D + 2

                for _ in range(cnt):
                    invalid += (A - 1) * (Q - Inside)

                    A = (A * a_num * inv_local[a_den]) % mod
                    Q = (Q * q_num * inv_local[q_den]) % mod
                    Inside = (Inside * i_num * inv_local[i_den]) % mod

                    a_num += 1
                    a_den += 1
                    q_num -= 1
                    q_den -= 1
                    i_num -= 1
                    i_den -= 1

            invalid += (A - 1) * (Q - Inside)

        # First entry through the left edge: (L, y), previous point (L-1, y).
        if need_left:
            A = comb(L + D + 1, L)
            Q = comb(W - L + H - D + 2, W - L + 1)
            Inside = comb(R - L + U - D + 2, R - L + 1)

            cnt = U - D
            if cnt:
                a_num = L + D + 2
                a_den = D + 2
                q_num = H - D + 1
                q_den = W - L + H - D + 2
                i_num = U - D + 1
                i_den = R - L + U - D + 2

                for _ in range(cnt):
                    invalid += (A - 1) * (Q - Inside)

                    A = (A * a_num * inv_local[a_den]) % mod
                    Q = (Q * q_num * inv_local[q_den]) % mod
                    Inside = (Inside * i_num * inv_local[i_den]) % mod

                    a_num += 1
                    a_den += 1
                    q_num -= 1
                    q_den -= 1
                    i_num -= 1
                    i_den -= 1

            invalid += (A - 1) * (Q - Inside)

    ans = (full_out - invalid) % mod
    print(ans)


if __name__ == "__main__":
    solve()