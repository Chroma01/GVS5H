import sys
from math import comb

def solve():
    N, P = map(int, sys.stdin.readline().split())
    H = N // 2
    K = N * (N - 1) // 2

    # binomial coefficients modulo P, for changing from t-basis to x-basis:
    # t^d = (1+x)^d.
    C = [[0] * (K + 1) for _ in range(K + 1)]
    C[0][0] = 1
    for n in range(1, K + 1):
        C[n][0] = 1
        C[n][n] = 1
        row = C[n]
        prev = C[n - 1]
        for r in range(1, n):
            row[r] = (prev[r - 1] + prev[r]) % P

    # buckets[used_vertices][(current_layer_parity, even_count, current_layer_size)]
    # stores coefficients in the basis (1+x)^d.
    buckets = [None] * (N + 1)
    buckets[1] = {(0, 1, 1): [1]}

    final_t = [0] * (K + 1)

    for used in range(1, N):
        current = buckets[used]
        if not current:
            continue

        remaining_labels = N - used

        for (parity, even_count, previous_size), poly in current.items():
            odd_count = used - even_count
            next_parity = parity ^ 1

            if next_parity == 0:
                max_b = H - even_count
            else:
                max_b = H - odd_count

            if max_b <= 0:
                continue

            plen = len(poly)

            for b in range(1, max_b + 1):
                new_used = used + b
                new_even = even_count + b if next_parity == 0 else even_count

                # Choose labels of the new BFS layer.
                label_factor = comb(remaining_labels, b) % P

                # The new layer contributes:
                # (1+x)^(b choose 2) * ((1+x)^previous_size - 1)^b.
                # In t = 1+x basis, expand the latter by binomial theorem.
                intra_shift = b * (b - 1) // 2
                max_shift = intra_shift + previous_size * b
                needed = plen + max_shift

                if new_used == N:
                    out = final_t
                    for j in range(b + 1):
                        factor = label_factor * comb(b, j) % P
                        if (b - j) & 1:
                            factor = (-factor) % P
                        shift = intra_shift + previous_size * j
                        for i, value in enumerate(poly):
                            out[i + shift] = (out[i + shift] + value * factor) % P
                else:
                    if buckets[new_used] is None:
                        buckets[new_used] = {}

                    key = (next_parity, new_even, b)
                    target = buckets[new_used].get(key)
                    if target is None:
                        target = [0] * needed
                        buckets[new_used][key] = target
                    elif len(target) < needed:
                        target.extend([0] * (needed - len(target)))

                    for j in range(b + 1):
                        factor = label_factor * comb(b, j) % P
                        if (b - j) & 1:
                            factor = (-factor) % P
                        shift = intra_shift + previous_size * j
                        for i, value in enumerate(poly):
                            target[i + shift] = (target[i + shift] + value * factor) % P

        buckets[used] = None

    # Convert sum_d final_t[d] * (1+x)^d into ordinary x coefficients.
    answer = [0] * (K + 1)
    for d, value in enumerate(final_t):
        if value:
            row = C[d]
            for m in range(d + 1):
                answer[m] = (answer[m] + value * row[m]) % P

    print(*answer[N - 1:])

if __name__ == "__main__":
    solve()