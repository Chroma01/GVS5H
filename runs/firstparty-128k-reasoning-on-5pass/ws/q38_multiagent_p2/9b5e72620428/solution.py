import sys
from collections import Counter


def main():
    out = sys.stdout.write
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]
    b = data[1 + n:1 + 2 * n]
    del data

    fixed_a = [x for x in a if x != -1]
    fixed_b = [x for x in b if x != -1]
    del a, b

    f = len(fixed_a)
    fb = len(fixed_b)
    ub = n - fb
    k = f - ub

    if k <= 1:
        out("Yes\n")
        return

    if not fixed_a or not fixed_b:
        out("No\n")
        return

    ca = Counter(fixed_a)
    cb = Counter(fixed_b)
    L = max(max(fixed_a, default=0), max(fixed_b, default=0))
    del fixed_a, fixed_b

    max_t = min(max(ca.values()), max(cb.values()), k)
    items_a = sorted(ca.items())
    items_b = sorted(cb.items())

    layers_a = [[] for _ in range(max_t + 1)]
    layers_b = [[] for _ in range(max_t + 1)]

    for v, c in items_a:
        lim = c if c < max_t else max_t
        for t in range(1, lim + 1):
            layers_a[t].append(v)

    for v, c in items_b:
        lim = c if c < max_t else max_t
        for t in range(1, lim + 1):
            layers_b[t].append(v)

    del items_a, items_b, ca, cb

    sums = []
    extend = sums.extend
    L_local = L

    for t in range(1, max_t + 1):
        A_t = layers_a[t]
        B_t = layers_b[t]
        if not A_t or not B_t:
            continue

        if len(A_t) <= len(B_t):
            outer = A_t
            inner = B_t
        else:
            outer = B_t
            inner = A_t

        st = len(inner)
        len_inner = len(inner)

        for x in outer:
            th = L_local - x
            while st > 0 and inner[st - 1] >= th:
                st -= 1

            if st == 0:
                extend([x + y for y in inner])
            elif st < len_inner:
                extend([x + y for y in inner[st:]])

    del layers_a, layers_b

    if len(sums) < k:
        out("No\n")
        return

    sums.sort()
    it = iter(sums)
    prev = next(it)
    run = 1

    for v in it:
        if v == prev:
            run += 1
            if run >= k:
                out("Yes\n")
                return
        else:
            prev = v
            run = 1

    out("No\n")


if __name__ == "__main__":
    main()