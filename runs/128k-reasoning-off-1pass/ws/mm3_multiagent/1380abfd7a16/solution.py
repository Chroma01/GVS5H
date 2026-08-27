import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    P = [0] * (N + 1)  # 1-indexed, P[0] unused
    for i in range(1, N + 1):
        P[i] = int(next(it))

    # Fenwick Tree (1-indexed) to manage empty slots.
    # Initially every slot (1..N) is empty -> store 1.
    size = N
    bit = [0] * (size + 2)
    for i in range(1, size + 1):
        bit[i] += 1
        j = i + (i & -i)
        if j <= size + 1:
            bit[j] += bit[i]

    def bit_add(idx: int, delta: int) -> None:
        # idx is 1-indexed
        while idx <= size:
            bit[idx] += delta
            idx += idx & -idx

    def bit_sum(idx: int) -> int:
        s = 0
        while idx > 0:
            s += bit[idx]
            idx -= idx & -idx
        return s

    def bit_lower_bound(k: int) -> int:
        # find smallest idx such that prefix sum >= k (1 <= k <= total)
        # standard BIT lifting
        idx = 0
        bit_mask = 1 << (size.bit_length() - 1)  # largest power of two <= size
        while bit_mask:
            next_idx = idx + bit_mask
            if next_idx <= size and bit[next_idx] < k:
                k -= bit[next_idx]
                idx = next_idx
            bit_mask >>= 1
        return idx + 1  # 1-indexed position

    res = [0] * N  # final array, 0-indexed positions
    # Process i from N down to 1
    for i in range(N, 0, -1):
        k = P[i]  # P_i-th empty slot
        pos = bit_lower_bound(k)  # 1-indexed
        res[pos - 1] = i
        bit_add(pos, -1)  # mark slot as filled

    sys.stdout.write(' '.join(map(str, res)))

if __name__ == "__main__":
    solve()