import sys

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    nxt = it.__next__
    int_ = int

    N = int_(nxt())
    M = 500000

    # Fenwick tree over the difference array D.
    # Initially D = [1] * M, so bit[i] = lowbit(i).
    bit = [0] + [i & -i for i in range(1, M + 1)]
    D = [1] * M

    total = M          # A[M-1], the maximum current rating
    min_val = 1        # A[0], the minimum current rating
    top = 1 << (M.bit_length() - 1)

    def lower_bound(target, bit=bit, M=M, top=top):
        """Return the first 0-based index i with prefix_sum(i) >= target."""
        idx = 0
        bitmask = top
        while bitmask:
            nxt_idx = idx + bitmask
            if nxt_idx <= M and bit[nxt_idx] < target:
                idx = nxt_idx
                target -= bit[nxt_idx]
            bitmask >>= 1
        return idx

    lb = lower_bound

    for _ in range(N):
        L = int_(nxt())
        R = int_(nxt())

        # No current rating can lie in [L, R].
        if L > total or R < min_val:
            continue

        if L <= min_val:
            a = 0
        else:
            a = lb(L)

        rp = R + 1
        if rp > total:
            c = M
        else:
            c = lb(rp)

        if a < c:
            # Add 1 to A[a:c] by updating the difference array.
            if a == 0:
                min_val += 1
                D[0] += 1
                i = 1
            else:
                D[a] += 1
                i = a + 1

            while i <= M:
                bit[i] += 1
                i += i & -i

            if c == M:
                total += 1
            else:
                D[c] -= 1
                i = c + 1
                while i <= M:
                    bit[i] -= 1
                    i += i & -i

    Q = int_(nxt())
    queries = [int_(nxt()) for _ in range(Q)]

    # Free large input/tree structures before producing output.
    del data, it, nxt, lb, lower_bound, bit

    # Reconstruct final ratings in-place: D becomes prefix sums of differences.
    s = 0
    for i in range(M):
        s += D[i]
        D[i] = s

    sys.stdout.write('\n'.join(str(D[x - 1]) for x in queries))

if __name__ == "__main__":
    main()