
## ideation
```python
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
    # Initialize Fenwick tree with N ones (all positions empty)
    bit = [0] * (N + 1)
    for i in range(1, N + 1):
        bit[i] += 1
        j = i + (i & -i)
        if j <= N:
            bit[j] += bit[i]
    A = [0] * (N + 1)
    # Process insertions in reverse order
    for i in range(N, 0, -1):
        k = P[i]  # we need the P_i-th empty slot for i
        # Find the index of the k-th 1 in the BIT (order statistics)
        idx = 0
        bit_mask = 1 << (N.bit_length() - 1)
        while bit_mask:
            t = idx + bit_mask
            if t <= N and bit[t] < k:
                idx = t
                k -= bit[t]
            bit_mask >>= 1
        pos = idx + 1
        A[pos] = i
        # Mark the slot as filled (set to 0)
        p = pos
        while p <= N:
            bit[p] -= 1
            p += p & -p
    sys.stdout.write(' '.join(map(str, A[1:])))

if __name__ == "__main__":
    solve()
```

## worker: Read input: parse N and the list P₁…Pₙ from stdin.
- The problem asks to build an array by inserting `i` at position `P_i` (1‑based) in the current array.
- Reversing the process is easier: when we have only the numbers `1 … i` left, the element `i` must be the `P_i`‑th from the left among the remaining empty positions.
- A Fenwick tree (BIT) maintains a multiset of empty slots (initially `N` ones). It supports:
  * **Point update** – mark a slot as filled (`‑1`).
  * **Order‑statistics query** – find the index of the `k`‑th `1` in `O(log N)` using binary lifting.
- The algorithm runs in `O(N log N)` time and `O(N)` memory, well within the limits (`N ≤ 5·10⁵`).
- Edge cases (e.g., `N = 1`) are handled automatically.
