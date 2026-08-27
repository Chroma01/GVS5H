import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    # Read P_1..P_N
    P = [0] * (n + 1)  # 1-indexed
    for i in range(1, n + 1):
        P[i] = int(next(it))
    
    # Fenwick tree
    size = n
    bit = [0] * (size + 1)
    # initialize with all 1s (empty slots)
    # We can build by adding 1 to each index, but that's O(N log N).
    # Instead, we can set the tree directly using a build operation.
    for i in range(1, size + 1):
        bit[i] += 1
    for i in range(1, size + 1):
        j = i + (i & -i)
        if j <= size:
            bit[j] += bit[i]
    
    def kth(k: int) -> int:
        """Return the index of the k-th one (1-indexed) in the BIT."""
        # find largest power of 2 <= size
        idx = 0
        bit_mask = 1 << (size.bit_length() - 1)
        while bit_mask:
            t = idx + bit_mask
            if t <= size and bit[t] < k:
                idx = t
                k -= bit[t]
            bit_mask >>= 1
        return idx + 1
    
    res = [0] * n
    for i in range(n, 0, -1):
        pos = kth(P[i])          # find P[i]-th empty slot
        res[pos - 1] = i         # place number i
        # mark slot as filled: add -1 at pos
        idx = pos
        while idx <= size:
            bit[idx] -= 1
            idx += idx & -idx
    
    sys.stdout.write(' '.join(map(str, res)))

if __name__ == "__main__":
    solve()