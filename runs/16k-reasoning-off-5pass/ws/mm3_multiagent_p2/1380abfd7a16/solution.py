import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    P = [0] * (N + 1)  # 1-indexed
    for i in range(1, N + 1):
        P[i] = int(next(it))

    # Fenwick tree over free positions, all 1's initially.
    size = N
    bit = [0] * (size + 1)
    for i in range(1, size + 1):
        bit[i] += 1
        j = i + (i & -i)
        if j <= size:
            bit[j] += bit[i]

    ans = [0] * N

    def find_kth(k):
        """Return smallest index idx (1-indexed) such that prefix sum >= k.
        Assumes 1 <= k <= total sum."""
        pos = 0
        bit_mask = 1 << (size.bit_length() - 1)
        while bit_mask:
            nxt = pos + bit_mask
            if nxt <= size and bit[nxt] < k:
                k -= bit[nxt]
                pos = nxt
            bit_mask >>= 1
        return pos + 1  # 1-indexed position

    for i in range(N, 0, -1):
        pos = find_kth(P[i])  # 1-indexed position in final array
        ans[pos - 1] = i
        # Mark this position as occupied: subtract 1 at pos.
        p = pos
        while p <= size:
            bit[p] -= 1
            p += p & -p

    sys.stdout.write(' '.join(map(str, ans)))

if __name__ == "__main__":
    main()