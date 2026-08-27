import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    c_start = 1
    c_end = 1 + 2 * N
    Q = data[c_end]
    queries = data[c_end + 1: c_end + 1 + Q]

    if not queries:
        return

    n = max(queries)

    # Fenwick tree over the difference array D.
    # Initially D[i] = 1, so Fenwick node i stores lowbit(i).
    bit = [0] + [i & -i for i in range(1, n + 1)]

    # Difference array D, where A[i] = prefix sum of D[1..i].
    D = [0] + [1] * n + [0]

    # Powers of two for Fenwick lower_bound.
    steps = [1 << k for k in range(n.bit_length() - 1, -1, -1)]

    def lower_bound(target, b=bit, nn=n, steps=steps):
        """Return the smallest idx such that prefix_sum(idx) >= target."""
        idx = 0
        for step in steps:
            nxt = idx + step
            if nxt <= nn:
                val = b[nxt]
                if val < target:
                    idx = nxt
                    target -= val
        return idx + 1

    minA = 1          # A[1]
    maxA = n          # A[n]
    lb = lower_bound
    bit_local = bit
    D_local = D
    nn = n

    for i in range(c_start, c_end, 2):
        L = data[i]
        R = data[i + 1]
        rp1 = R + 1

        # No rating can be in [L, R].
        if rp1 <= minA or L > maxA:
            continue

        if L <= minA:
            l = 1
        else:
            l = lb(L)

        if rp1 <= maxA:
            r = lb(rp1) - 1
        else:
            r = nn

        if l <= r:
            # Add 1 to A[l..r].
            D_local[l] += 1
            j = l
            while j <= nn:
                bit_local[j] += 1
                j += j & -j

            if r < nn:
                p = r + 1
                D_local[p] -= 1
                j = p
                while j <= nn:
                    bit_local[j] -= 1
                    j += j & -j
            else:
                maxA += 1

            if l == 1:
                minA += 1

    del data

    # Convert difference array D into final ratings A in-place.
    cur = 0
    for i in range(1, nn + 1):
        cur += D_local[i]
        D_local[i] = cur

    out = [str(D_local[x]) for x in queries]
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()