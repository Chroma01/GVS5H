
## ideation
```python
import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    # Count occurrences and sum of 1‑based positions for each value
    cnt = [0] * M
    sumPos = [0] * M
    for idx, val in enumerate(A):
        cnt[val] += 1
        sumPos[val] += idx + 1          # positions are 1‑based

    # ------------------------------------------------------------
    # Initial inversion number for k = 0 (B = A)
    size = M
    bit = [0] * (size + 2)            # Fenwick tree (1‑based)

    def bit_add(i: int, x: int) -> None:
        while i <= size:
            bit[i] += x
            i += i & -i

    def bit_sum(i: int) -> int:
        s = 0
        while i:
            s += bit[i]
            i -= i & -i
        return s

    inv0 = 0
    for idx, val in enumerate(A):
        v = val + 1                    # shift because BIT is 1‑based
        # previous elements greater than val = idx - (# previous ≤ val)
        inv0 += idx - bit_sum(v)
        bit_add(v, 1)

    # ------------------------------------------------------------
    # Compute answers for all k using the transition formula
    ans = [0] * M
    ans[0] = inv0
    for k in range(1, M):
        v = (M - k) % M                 # value whose elements wrap now
        c = cnt[v]
        sp = sumPos[v]
        delta = 2 * sp - c * (N + 1)    # change from ans[k-1] to ans[k]
        ans[k] = ans[k - 1] + delta

    sys.stdout.write('\n'.join(str(x) for x in ans))

if __name__ == "__main__":
    solve()
```

## worker: finalize
- For each `k`, `B_i = (A_i + k) mod M`.  
- When we increase `k` by one, all elements with original value `v = (M‑k) mod M` change from `M‑1` to `0`; every other element just increases by one.  
- Pairs of two non‑wrapping elements keep their relative order, and pairs of two wrapping elements also keep order (both become `0`).  
- A pair where exactly one element wraps changes its contribution:
  * non‑wrap before wrap: becomes an inversion (adds +1)
  * wrap before non‑wrap: stops being an inversion (adds ‑1)  
- Summing over all wrapping positions gives the net change  
  `delta(k) = 2·sumPos[v] – cnt[v]·(N+1)`, where `sumPos[v]` is the sum of 1‑based indices of all occurrences of `v`.  
- Compute the inversion count for `k=0` with a Fenwick tree over the value range `[0, M‑1]` in `O(N log M)`.  
- Then apply the formula for `k = 1 … M‑1` in `O(M)` time.  
- Overall complexity `O((N+M) log M)`, memory `O(N+M)`, which fits the limits (`N, M ≤ 2·10⁵`).
