import sys


def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    P = int(data[1])

    E = N // 2
    Cmax = N * (N - 1) // 2
    D = Cmax - 3 * E + 2

    # Modular inverses of 1..max(D+1, N)
    max_inv = max(D + 1, N) + 1
    inv = [0] * (max_inv + 1)
    inv[1] = 1
    for i in range(2, max_inv + 1):
        inv[i] = (P - (P // i) * inv[P % i] % P) % P

    # Binomial coefficients modulo P
    comb = [[0] * (N + 1) for _ in range(N + 1)]
    for i in range(N + 1):
        comb[i][0] = 1
        comb[i][i] = 1
        for j in range(1, i):
            comb[i][j] = (comb[i - 1][j - 1] + comb[i - 1][j]) % P

    # Packed polynomial base.  2^45 is safely larger than any stored limb:
    # a DP state receives at most N contributions, and the final sum is < 2N^2 P.
    SHIFT = 45
    MASK = (1 << SHIFT) - 1
    FULL_MASK = (1 << (SHIFT * (E + 1))) - 1
    shift_bits = [SHIFT * i for i in range(E + 1)]

    # low_mask[t] keeps even-counts e with t - e <= E (odd count not already too large)
    low_mask = [FULL_MASK] * (N + 1)
    for t in range(N + 1):
        min_e = t - E
        if min_e > 0:
            low_mask[t] = FULL_MASK ^ ((1 << (SHIFT * min_e)) - 1)

    # Reusable range objects for small limb loops
    ranges = [range(i) for i in range(E + 2)]

    # Flattened DP indices: index = t * stride + a * 2 + parity
    stride = 2 * (N + 1)
    size = (N + 1) * stride
    start_idx = stride + 2
    start_val = 1 << shift_bits[1]

    idx_odd = [[0] * (N + 1) for _ in range(N + 1)]
    idx_even = [[0] * (N + 1) for _ in range(N + 1)]
    for t in range(1, N):
        for b in range(1, N - t + 1):
            idx_odd[t][b] = (t + b) * stride + b * 2 + 1
            idx_even[t][b] = (t + b) * stride + b * 2

    max_a_list = [0] * (N + 1)
    for t in range(1, N):
        max_a_list[t] = 1 if t == 1 else t - 1

    def eval_x(xval):
        mod = P
        N_local = N
        E_local = E
        shift = SHIFT
        mask = MASK
        shbits = shift_bits
        stride_local = stride
        size_local = size
        start_idx_local = start_idx
        start_val_local = start_val
        inv_local = inv
        comb_local = comb
        low_masks = low_mask
        ranges_local = ranges
        idx_odd_local = idx_odd
        idx_even_local = idx_even
        max_a_list_local = max_a_list

        y = (xval + 1) % mod
        invx = inv_local[xval]

        pow_y = [1] * (N_local + 1)
        for i in range(1, N_local + 1):
            pow_y[i] = (pow_y[i - 1] * y) % mod

        q = [0] * (N_local + 1)
        for a in range(1, N_local + 1):
            q[a] = ((pow_y[a] - 1) * invx) % mod

        qpow = [[1] * (N_local + 1) for _ in range(N_local + 1)]
        for a in range(1, N_local + 1):
            qa = q[a]
            row = qpow[a]
            v = 1
            for b in range(1, N_local + 1):
                v = (v * qa) % mod
                row[b] = v

        internal = [1] * (N_local + 1)
        for b in range(2, N_local + 1):
            internal[b] = (internal[b - 1] * pow_y[b - 1]) % mod

        base = [[0] * (N_local + 1) for _ in range(N_local + 1)]
        for rem in range(1, N_local):
            brow = base[rem]
            crow = comb_local[rem]
            for b in range(1, rem + 1):
                brow[b] = (crow[b] * internal[b]) % mod

        dp = [0] * size_local
        dp[start_idx_local] = start_val_local

        for t in range(1, N_local):
            rem = N_local - t
            base_rem = base[rem]
            base_t = t * stride_local
            max_a = max_a_list_local[t]
            idx_odd_t = idx_odd_local[t]
            idx_even_t = idx_even_local[t]

            for a in range(1, max_a + 1):
                idx0 = base_t + a * 2

                if t <= E_local:
                    p0 = dp[idx0]
                    p1 = dp[idx0 + 1]
                else:
                    low_t = low_masks[t]
                    p0 = dp[idx0] & low_t
                    p1 = dp[idx0 + 1] & low_t

                if not p0 and not p1:
                    continue

                qrow = qpow[a]
                if qrow[1] == 0:
                    continue

                # Current layer parity 0 (even), next layer is odd.
                if p0:
                    min_e = ((p0 & -p0).bit_length() - 1) // shift
                    max_e = (p0.bit_length() - 1) // shift

                    max_b = rem
                    v = max_e - t + E_local
                    if v < max_b:
                        max_b = v

                    if max_b > 0:
                        off = min_e
                        p_tmp = p0 >> shbits[off] if off else p0
                        width = max_e - off + 1
                        rng = ranges_local[width]

                        coeffs = [0] * width
                        for i in rng:
                            coeffs[i] = p_tmp & mask
                            p_tmp >>= shift

                        start_sh = shbits[off]
                        for b in range(1, max_b + 1):
                            w = (base_rem[b] * qrow[b]) % mod
                            if not w:
                                continue
                            res = 0
                            sh = start_sh
                            for i in rng:
                                c = coeffs[i]
                                if c:
                                    res |= ((c * w) % mod) << sh
                                sh += shift
                            dp[idx_odd_t[b]] += res

                # Current layer parity 1 (odd), next layer is even.
                if p1:
                    min_e = ((p1 & -p1).bit_length() - 1) // shift
                    max_e = (p1.bit_length() - 1) // shift

                    max_b = rem
                    v = E_local - min_e
                    if v < max_b:
                        max_b = v

                    if max_b > 0:
                        off = min_e
                        p_tmp = p1 >> shbits[off] if off else p1
                        width_full = max_e - off + 1
                        rng_full = ranges_local[width_full]

                        coeffs = [0] * width_full
                        for i in rng_full:
                            coeffs[i] = p_tmp & mask
                            p_tmp >>= shift

                        for b in range(1, max_b + 1):
                            lim = E_local - b - off + 1
                            if lim > width_full:
                                lim = width_full
                            if lim <= 0:
                                continue

                            w = (base_rem[b] * qrow[b]) % mod
                            if not w:
                                continue

                            res = 0
                            sh = shbits[off + b]
                            for i in ranges_local[lim]:
                                c = coeffs[i]
                                if c:
                                    res |= ((c * w) % mod) << sh
                                sh += shift
                            dp[idx_even_t[b]] += res

        ans = 0
        base_N = N_local * stride_local
        shE = shbits[E_local]
        for a in range(1, N_local):
            idx = base_N + a * 2
            ans += (dp[idx] >> shE) & mask
            ans += (dp[idx + 1] >> shE) & mask
        return ans % mod

    vals = [0] * (D + 1)
    for i in range(1, D + 2):
        vals[i - 1] = eval_x(i)

    # Newton forward differences: G(x) = sum_k newton[k] * C(x-1, k)
    diff = vals[:]
    newton = [0] * (D + 1)
    for k in range(D + 1):
        newton[k] = diff[0]
        for i in range(D - k):
            v = diff[i + 1] - diff[i]
            if v < 0:
                v += P
            diff[i] = v

    # Convert basis C(x-1, k) to power basis.
    res = [0] * (D + 1)
    poly = [1]
    for k in range(D + 1):
        ck = newton[k]
        if ck:
            for i, c in enumerate(poly):
                res[i] = (res[i] + ck * c) % P

        if k < D:
            r = k + 1
            factor = inv[r]
            old = poly
            new = [0] * (k + 2)
            new[0] = (-r * old[0]) * factor % P
            for j in range(1, k + 1):
                new[j] = (old[j - 1] - r * old[j]) * factor % P
            new[k + 1] = old[k] * factor % P
            poly = new

    total_out = Cmax - N + 2
    if len(res) > total_out:
        res = res[:total_out]
    elif len(res) < total_out:
        res += [0] * (total_out - len(res))

    sys.stdout.write(" ".join(map(str, res)) + "\n")


if __name__ == "__main__":
    solve()