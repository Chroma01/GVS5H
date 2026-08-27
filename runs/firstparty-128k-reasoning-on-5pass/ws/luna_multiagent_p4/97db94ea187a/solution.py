import sys
from math import comb

def solve():
    N, P = map(int, sys.stdin.readline().split())
    D = N * (N - 1) // 2
    half = N // 2

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % P

    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], P - 2, P)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % P

    # transitions[(a, b)] consists of (degree shift, coefficient)
    # for y^C(b,2) * (y^a - 1)^b * invfact[b].
    transitions = {}
    for a in range(1, N):
        for b in range(1, N - a + 1):
            base = b * (b - 1) // 2
            ib = invfact[b]
            cur = []
            for j in range(b + 1):
                c = comb(b, j)
                if (b - j) & 1:
                    c = -c
                c %= P
                c = c * ib % P
                shift = base + a * j
                if shift <= D and c:
                    cur.append((shift, c))
            transitions[(a, b)] = cur

    # levels[t] maps (even_vertex_count, last_layer_size, layer_index_parity)
    # to [polynomial in y, current maximum degree].
    levels = [None] * (N + 1)
    initial = [0] * (D + 1)
    initial[0] = 1
    levels[1] = {(1, 1, 0): [initial, 0]}

    for t in range(1, N):
        states = levels[t]
        if not states:
            continue

        # All incoming transitions to this level are complete now, so reduce
        # coefficients before using them as sources.
        for arr, md in states.values():
            for i in range(md + 1):
                arr[i] %= P

        for (q, a, phase), (src, src_md) in states.items():
            max_b = N - t
            for b in range(1, max_b + 1):
                nt = t + b
                nq = q + (b if phase else 0)
                if nq > half or nt - nq > half:
                    continue

                key = (nq, b, phase ^ 1)
                target_level = levels[nt]
                if target_level is None:
                    target_level = {}
                    levels[nt] = target_level

                item = target_level.get(key)
                if item is None:
                    dst = [0] * (D + 1)
                    dst_md = -1
                    item = [dst, dst_md]
                    target_level[key] = item
                else:
                    dst, dst_md = item

                for shift, coef in transitions[(a, b)]:
                    if shift > D:
                        continue
                    upper = min(src_md, D - shift)
                    if upper < 0:
                        continue
                    # Deliberately defer modular reduction until this level
                    # is used as a source; this greatly reduces % operations.
                    for i in range(upper + 1):
                        dst[i + shift] += src[i] * coef
                    nd = upper + shift
                    if nd > item[1]:
                        item[1] = nd

        levels[t] = None

    final_level = levels[N]
    total_y = [0] * (D + 1)
    if final_level:
        for (q, a, phase), (arr, md) in final_level.items():
            if q != half:
                continue
            for i in range(md + 1):
                total_y[i] = (total_y[i] + arr[i]) % P

    # Convert from the y-basis to the x-basis using y = 1 + x:
    # [x^m] y^e = C(e, m).
    answer = [0] * (D + 1)
    for e, value in enumerate(total_y):
        if value:
            for m in range(e + 1):
                answer[m] = (answer[m] + value * comb(e, m)) % P

    multiplier = fact[N - 1]
    result = [(answer[m] * multiplier) % P for m in range(N - 1, D + 1)]
    print(*result)

if __name__ == "__main__":
    solve()