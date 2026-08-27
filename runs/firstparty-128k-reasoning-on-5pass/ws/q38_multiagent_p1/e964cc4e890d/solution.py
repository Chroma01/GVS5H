import sys
import gc

MOD = 998244353
G = 3


def main():
    gc.disable()
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    S = data[1]

    # Necessary conditions for cuts 1 and 2N-1.
    if S[0] != 66 or S[-1] != 87:  # 'B', 'W'
        print(0)
        return

    # c[w] = number of black vertices before the w-th white vertex.
    c = [0] * (N + 1)
    b = 0
    w = 0
    for ch in S:
        if ch == 66:  # B
            b += 1
        else:         # W
            w += 1
            c[w] = b

    fact = [1] * (N + 1)
    mod = MOD
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % mod

    A = [0] * (N + 1)
    add = [0] * (N + 1)

    # NTT roots.  The largest convolution length is below 2N, but 3N is a safe bound.
    max_k = (3 * N + 10).bit_length()
    root_pw = [0] * (max_k + 1)
    inv_root_pw = [0] * (max_k + 1)
    inv_len = [1] * (max_k + 1)
    inv2 = (mod + 1) // 2
    for k in range(1, max_k + 1):
        root_pw[k] = pow(G, (mod - 1) >> k, mod)
        inv_root_pw[k] = pow(root_pw[k], mod - 2, mod)
        inv_len[k] = inv_len[k - 1] * inv2 % mod

    # Lazy twiddle tables.  This removes the per-butterfly twiddle update multiplication.
    fwd_tw = [None] * (max_k + 1)
    inv_tw = [None] * (max_k + 1)

    def get_fwd_tw(k):
        tw = fwd_tw[k]
        if tw is None:
            half = 1 << (k - 1)
            tw = [1] * half
            wlen = root_pw[k]
            for i in range(1, half):
                tw[i] = tw[i - 1] * wlen % mod
            fwd_tw[k] = tw
        return tw

    def get_inv_tw(k):
        tw = inv_tw[k]
        if tw is None:
            half = 1 << (k - 1)
            tw = [1] * half
            wlen = inv_root_pw[k]
            for i in range(1, half):
                tw[i] = tw[i - 1] * wlen % mod
            inv_tw[k] = tw
        return tw

    # DIF forward NTT.  Output is in bit-reversed order.
    def ntt(a, k):
        n = 1 << k
        length = n
        while length > 1:
            half = length >> 1
            tw = get_fwd_tw(k)
            for i in range(0, n, length):
                for t in range(half):
                    j = i + t
                    u = a[j]
                    v = a[j + half]
                    x = u + v
                    if x >= mod:
                        x -= mod
                    y = u - v
                    if y < 0:
                        y += mod
                    a[j] = x
                    a[j + half] = (y * tw[t]) % mod
            length = half
            k -= 1

    # DIT inverse NTT.  Input is in bit-reversed order, output is natural order.
    def intt(a, k):
        n = 1 << k
        length = 2
        kk = 1
        while length <= n:
            half = length >> 1
            tw = get_inv_tw(kk)
            for i in range(0, n, length):
                for t in range(half):
                    j = i + t
                    u = a[j]
                    v = (a[j + half] * tw[t]) % mod
                    x = u + v
                    if x >= mod:
                        x -= mod
                    y = u - v
                    if y < 0:
                        y += mod
                    a[j] = x
                    a[j + half] = y
            length <<= 1
            kk += 1
        inv_n = inv_len[k]
        for i in range(n):
            a[i] = (a[i] * inv_n) % mod

    def apply_grouped(l, mid, r):
        """Add contributions from [l, mid] to [mid+1, r] by grouping equal c[j]."""
        base = mid + 1
        r1 = r + 1
        j = l
        while j <= mid:
            d = c[j]
            coeff = 0
            while j <= mid and c[j] == d:
                aj = A[j]
                if aj:
                    coeff += aj
                    if coeff >= mod:
                        coeff -= mod
                j += 1
            if coeff:
                start = base if base > d else d
                if start <= r:
                    if coeff == 1:
                        for i in range(start, r1):
                            x = add[i] + fact[i - d]
                            if x >= mod:
                                x -= mod
                            add[i] = x
                    else:
                        for i in range(start, r1):
                            add[i] = (add[i] + coeff * fact[i - d]) % mod

    def scan_grouped_cost(l, mid, r, limit):
        """Upper-bounded cost of grouped direct application."""
        base = mid + 1
        cost = 0
        j = l
        while j <= mid and cost <= limit:
            d = c[j]
            coeff = 0
            while j <= mid and c[j] == d:
                aj = A[j]
                if aj:
                    coeff += aj
                    if coeff >= mod:
                        coeff -= mod
                j += 1
            if coeff:
                start = base if base > d else d
                if start <= r:
                    cost += r - start + 1
        return cost

    def apply_ntt(l, mid, r, d0, L, k_min, K, n):
        """Add contributions from [l, mid] to [mid+1, r] using one NTT convolution."""
        T = [0] * L
        nonzero = False
        j = l
        while j <= mid:
            d = c[j]
            coeff = 0
            while j <= mid and c[j] == d:
                aj = A[j]
                if aj:
                    coeff += aj
                    if coeff >= mod:
                        coeff -= mod
                j += 1
            if coeff and d <= r:
                T[d - d0] = coeff
                nonzero = True

        if not nonzero:
            return

        F = fact[k_min:k_min + K]
        k = n.bit_length() - 1

        T.extend([0] * (n - L))
        F.extend([0] * (n - K))

        ntt(T, k)
        ntt(F, k)

        for i in range(n):
            T[i] = (T[i] * F[i]) % mod
        del F

        intt(T, k)

        off = d0 + k_min
        start_i = mid + 1
        if start_i < off:
            start_i = off
        r1 = r + 1
        for i in range(start_i, r1):
            x = add[i] + T[i - off]
            if x >= mod:
                x -= mod
            add[i] = x

    SMALL_ROUGH = 4096
    MIN_NTT = 128
    NAIVE_FACTOR = 2

    def apply(l, mid, r):
        d0 = c[l]
        if d0 > r:
            return

        left_len = mid - l + 1
        right_len = r - mid
        rough = left_len * right_len

        if rough <= SMALL_ROUGH:
            apply_grouped(l, mid, r)
            return

        d1 = c[mid]
        if d1 > r:
            d1 = r
        L = d1 - d0 + 1
        if L <= 0:
            return

        base = mid + 1
        k_min = base - d0 - (L - 1)
        if k_min < 0:
            k_min = 0
        k_max = r - d0
        if k_min > k_max:
            return

        K = k_max - k_min + 1
        conv_len = L + K - 1
        n = 1 << (conv_len - 1).bit_length()

        if n < MIN_NTT:
            apply_grouped(l, mid, r)
            return

        limit = NAIVE_FACTOR * n * (n.bit_length() - 1)
        grouped_cost = scan_grouped_cost(l, mid, r, limit)
        if grouped_cost == 0:
            return

        if grouped_cost <= limit:
            apply_grouped(l, mid, r)
        else:
            apply_ntt(l, mid, r, d0, L, k_min, K, n)

    sys.setrecursionlimit(1_000_000)
    BLOCK = 32

    def solve(l, r):
        if r - l + 1 <= BLOCK:
            r1 = r + 1
            for i in range(l, r1):
                if c[i] <= i:
                    val = fact[i] - add[i]
                    if val < 0:
                        val += mod
                    A[i] = val
                else:
                    A[i] = 0

                aj = A[i]
                if aj:
                    d = c[i]
                    start = i + 1
                    if d > start:
                        start = d
                    if start <= r:
                        if aj == 1:
                            for k in range(start, r1):
                                x = add[k] + fact[k - d]
                                if x >= mod:
                                    x -= mod
                                add[k] = x
                        else:
                            for k in range(start, r1):
                                add[k] = (add[k] + aj * fact[k - d]) % mod
            return

        mid = (l + r) >> 1
        solve(l, mid)
        apply(l, mid, r)
        solve(mid + 1, r)

    solve(1, N)
    print(A[N] % mod)


if __name__ == "__main__":
    main()