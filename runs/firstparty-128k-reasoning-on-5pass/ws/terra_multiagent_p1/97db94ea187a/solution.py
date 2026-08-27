import sys

def solve():
    N, MOD = map(int, sys.stdin.readline().split())
    H = N // 2
    EMAX = N * (N - 1) // 2

    # Binomial coefficients modulo MOD, for values at most N or EMAX.
    comb_n = [[0] * (N + 1) for _ in range(N + 1)]
    comb_n[0][0] = 1
    for i in range(1, N + 1):
        comb_n[i][0] = comb_n[i][i] = 1
        for j in range(1, i):
            comb_n[i][j] = (comb_n[i - 1][j - 1] + comb_n[i - 1][j]) % MOD

    # Binomial coefficients for converting the (1+x)^q basis to x^m.
    comb_e = [[0] * (EMAX + 1) for _ in range(EMAX + 1)]
    comb_e[0][0] = 1
    for i in range(1, EMAX + 1):
        comb_e[i][0] = comb_e[i][i] = 1
        prev = comb_e[i - 1]
        row = comb_e[i]
        for j in range(1, i):
            row[j] = (prev[j - 1] + prev[j]) % MOD

    # terms[a][b] represents
    # ((1+x)^a - 1)^b * (1+x)^(b*(b-1)/2)
    # as a linear combination of powers of t = 1+x:
    # sum (shift, coefficient) * t^shift.
    terms = [[None] * (N + 1) for _ in range(N + 1)]
    for a in range(1, N + 1):
        for b in range(1, N + 1):
            base = b * (b - 1) // 2
            cur = []
            for j in range(b + 1):
                c = comb_n[b][j]
                if (b - j) & 1:
                    c = (-c) % MOD
                cur.append((base + a * j, c))
            terms[a][b] = cur

    # levels[u][(parity_of_last_layer, even_vertices_so_far, last_layer_size)]
    # is a polynomial in t=1+x, represented by coefficient list.
    levels = [None] * (N + 1)
    levels[1] = {(0, 1, 1): [1]}  # L_0 = {1}

    for used in range(1, N):
        cur_level = levels[used]
        if not cur_level:
            continue

        remaining = N - used

        for (parity, even_count, last_size), src in cur_level.items():
            src_len = len(src)
            next_parity = parity ^ 1

            for b in range(1, remaining + 1):
                next_used = used + b
                next_even = even_count + (b if next_parity == 0 else 0)
                next_odd = next_used - next_even

                if next_even > H or next_odd > H:
                    continue

                # Select which currently unused labels become the next layer.
                label_factor = comb_n[remaining][b]
                key = (next_parity, next_even, b)

                if levels[next_used] is None:
                    levels[next_used] = {}
                target_level = levels[next_used]

                max_shift = last_size * b + b * (b - 1) // 2
                needed_len = src_len + max_shift

                dst = target_level.get(key)
                if dst is None:
                    dst = [0] * needed_len
                    target_level[key] = dst
                elif len(dst) < needed_len:
                    dst.extend([0] * (needed_len - len(dst)))

                # Multiply src by the sparse t-basis representation of the
                # transition polynomial.
                for shift, coef0 in terms[last_size][b]:
                    coef = (coef0 * label_factor) % MOD
                    if coef == 0:
                        continue
                    end = src_len
                    for i in range(end):
                        v = src[i]
                        if v:
                            dst[i + shift] = (dst[i + shift] + v * coef) % MOD

        levels[used] = None

    total_t = [0] * (EMAX + 1)
    final_level = levels[N]
    if final_level:
        for (parity, even_count, last_size), poly in final_level.items():
            if even_count != H:
                continue
            for q, v in enumerate(poly):
                if v:
                    total_t[q] = (total_t[q] + v) % MOD

    # If F(x) = sum_q total_t[q] * (1+x)^q,
    # then [x^m] F = sum_{q>=m} total_t[q] * C(q,m).
    ans = [0] * (EMAX + 1)
    for q, v in enumerate(total_t):
        if v == 0:
            continue
        row = comb_e[q]
        for m in range(q + 1):
            ans[m] = (ans[m] + v * row[m]) % MOD

    print(" ".join(map(str, ans[N - 1:])))

if __name__ == "__main__":
    solve()