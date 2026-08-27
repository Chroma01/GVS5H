import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    P = [0] * (N + 1)
    for i in range(1, N + 1):
        P[i] = int(next(it))

    # Fenwick tree (Binary Indexed Tree) storing 1 for each empty slot
    bit = [0] * (N + 1)
    for i in range(1, N + 1):
        bit[i] = 1
        j = i + (i & -i)
        if j <= N:
            bit[j] += bit[i]

    A = [0] * (N + 1)          # final array, 1‑based

    # largest power of two not exceeding N (for order‑statistics search)
    max_log = N.bit_length()

    # Process insertions in reverse order: for i = N … 1
    for i in range(N, 0, -1):
        k = P[i]                # we need the k‑th empty slot
        idx = 0
        bit_mask = 1 << (max_log - 1)
        while bit_mask:
            t = idx + bit_mask
            if t <= N and bit[t] < k:
                k -= bit[t]
                idx = t
            bit_mask >>= 1
        pos = idx + 1           # position where i must finally be placed
        A[pos] = i

        # mark the slot as filled (remove the 1 from BIT)
        p = pos
        while p <= N:
            bit[p] -= 1
            p += p & -p

    sys.stdout.write(' '.join(map(str, A[1:])))

if __name__ == "__main__":
    solve()