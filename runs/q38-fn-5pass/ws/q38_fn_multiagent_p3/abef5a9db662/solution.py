import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    M = 500000
    N = data[0]

    # diff[i] = A[i] - A[i-1], with A[0] = 0.
    # Initially A[i] = i, so all differences are 1.
    diff = [0] + [1] * M + [0]

    # Fenwick tree over diff.  Initially diff is all ones, so bit[i] = lowbit(i).
    bit = [0] + [i & -i for i in range(1, M + 1)] + [0]

    highest = 1 << (M.bit_length() - 1)

    def lower_bound(target, b=bit, n=M, step0=highest):
        """Smallest idx such that prefix_sum(idx) >= target.
        Returns n+1 if total sum < target.
        """
        idx = 0
        step = step0
        while step:
            nxt = idx + step
            if nxt <= n and b[nxt] < target:
                idx = nxt
                target -= b[nxt]
            step >>= 1
        return idx + 1

    lb = lower_bound
    p = 1

    for _ in range(N):
        L = data[p]
        R = data[p + 1]
        p += 2

        # First initial rating whose current rating is at least L.
        l = lb(L)

        # First initial rating whose current rating is at least R+1.
        # Therefore the last one with current rating <= R is pos-1.
        pos = lb(R + 1)
        r = pos - 1

        if l <= r:
            # Add 1 to A[l..r] by updating the difference array.
            diff[l] += 1
            i = l
            while i <= M:
                bit[i] += 1
                i += i & -i

            if r < M:
                rp = r + 1
                diff[rp] -= 1
                i = rp
                while i <= M:
                    bit[i] -= 1
                    i += i & -i

    # Materialize final A[x] as prefix sums of diff.
    cur = 0
    for i in range(1, M + 1):
        cur += diff[i]
        diff[i] = cur

    # The Fenwick tree is no longer needed.
    del lower_bound
    del bit

    Q = data[p]
    p += 1

    out = [None] * Q
    for i in range(Q):
        out[i] = str(diff[data[p + i]])

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()