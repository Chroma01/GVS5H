import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    q_idx = 1 + 2 * n
    q = data[q_idx]
    q_start = q_idx + 1
    queries = data[q_start:q_start + q]

    if q == 0:
        return

    m = max(queries)
    top = 1 << (m.bit_length() - 1)

    # Fenwick tree for d[x] = F(x) - F(x-1), initially all ones.
    bit = [0] + [i & -i for i in range(1, m + 1)]
    total = m  # F(m)

    def lb(t, bit=bit, m=m, top=top):
        """Smallest index i with prefix sum >= t, or m+1 if none."""
        idx = 0
        step = top
        while step:
            nxt = idx + step
            if nxt <= m and bit[nxt] < t:
                idx = nxt
                t -= bit[nxt]
            step >>= 1
        return idx + 1

    p = 1
    for _ in range(n):
        L = data[p]
        R = data[p + 1]
        p += 2

        if L > total:
            continue

        a = lb(L)
        rp = R + 1

        if rp > total:
            # Affected range is [a, m].
            i = a
            while i <= m:
                bit[i] += 1
                i += i & -i
            total += 1
        else:
            c = lb(rp)
            if c > a:
                # Affected range is [a, c-1].
                i = a
                while i <= m:
                    bit[i] += 1
                    i += i & -i

                i = c
                while i <= m:
                    bit[i] -= 1
                    i += i & -i

    del data

    # Convert Fenwick tree in-place to prefix sums: bit[x] becomes F(x).
    for i in range(1, m + 1):
        bit[i] += bit[i - (i & -i)]

    out = [str(bit[x]) for x in queries]
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()