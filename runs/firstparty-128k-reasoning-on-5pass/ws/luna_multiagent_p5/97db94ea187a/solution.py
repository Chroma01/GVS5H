import sys
from math import comb


def solve():
    n, mod = map(int, sys.stdin.buffer.readline().split())
    half = n // 2
    max_edges = n * (n - 1) // 2
    need_edges = n - 1

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % mod

    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], mod - 2, mod)
    for i in range(n, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % mod

    # In q = 1 + x, a layer of size s following a layer of size p has
    # polynomial q^C(s,2) * (q^p - 1)^s.
    # Each item is (q-degree shift, coefficient).
    layer_terms = [[None] * (n + 1) for _ in range(n + 1)]
    for p in range(1, n + 1):
        for s in range(1, n + 1):
            inside = s * (s - 1) // 2
            terms = []
            for k in range(s + 1):
                degree = inside + p * k
                if degree > max_edges:
                    continue
                coefficient = comb(s, k)
                if (s - k) & 1:
                    coefficient = -coefficient
                coefficient %= mod
                if coefficient:
                    terms.append((degree, coefficient))
            layer_terms[p][s] = terms

    # levels[used] maps (previous layer size, even vertices, layer parity)
    # to a dense polynomial in q.
    levels = [dict() for _ in range(n + 1)]
    levels[1][(1, 1, 0)] = [1]

    for used in range(1, n):
        current = levels[used]
        for (previous, even_count, parity), poly in current.items():
            remaining = n - used
            for size in range(1, remaining + 1):
                new_used = used + size
                added_even = size if parity else 0
                new_even = even_count + added_even
                new_odd = new_used - new_even

                if new_even > half or new_odd > half:
                    continue

                new_parity = parity ^ 1
                key = (size, new_even, new_parity)
                terms = layer_terms[previous][size]

                max_shift = terms[-1][0]
                target_len = min(max_edges, len(poly) - 1 + max_shift) + 1

                target = levels[new_used].get(key)
                if target is None:
                    target = [0] * target_len
                    levels[new_used][key] = target
                elif len(target) < target_len:
                    target.extend([0] * (target_len - len(target)))

                scale = inv_fact[size]

                # Shift-add by q^degree terms.  Iterating by shift avoids
                # repeatedly recomputing the scaled coefficient for every
                # source polynomial entry.
                for shift, coefficient in terms:
                    factor = coefficient * scale % mod
                    limit = min(len(poly), len(target) - shift)
                    for i in range(limit):
                        value = poly[i]
                        if value:
                            j = i + shift
                            target[j] = (
                                target[j] + value * factor
                            ) % mod

    qpoly = [0] * (max_edges + 1)
    for (previous, even_count, parity), poly in levels[n].items():
        if even_count != half:
            continue
        upto = min(len(poly), max_edges + 1)
        for degree in range(upto):
            qpoly[degree] = (qpoly[degree] + poly[degree]) % mod

    label_factor = fact[n - 1]
    for degree in range(max_edges + 1):
        qpoly[degree] = qpoly[degree] * label_factor % mod

    answers = []
    for m in range(need_edges, max_edges + 1):
        value = 0
        for degree in range(m, max_edges + 1):
            coefficient = qpoly[degree]
            if coefficient:
                value = (value + coefficient * comb(degree, m)) % mod
        answers.append(str(value))

    sys.stdout.write(" ".join(answers))


if __name__ == "__main__":
    solve()