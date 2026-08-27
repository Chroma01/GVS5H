
## ideation
```python
import sys

def solve():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    N = data[0]
    X = data[1:]

    # gaps[i] = X[i+1] - X[i] for i = 0..N-2 (1-indexed gap i+1)
    gaps = [X[i+1] - X[i] for i in range(N-1)]

    # Separate gaps by parity of their index (1-indexed)
    odd_gaps = [gaps[i] for i in range(N-1) if i % 2 == 0]   # indices 1,3,5,...
    even_gaps = [gaps[i] for i in range(N-1) if i % 2 == 1]  # indices 2,4,6,...

    # Sort each parity group in ascending order
    odd_gaps.sort()
    even_gaps.sort()

    # Reconstruct the gap sequence: assign smallest odd gap to smallest odd position, etc.
    new_gaps = [0] * (N-1)
    for i, val in enumerate(odd_gaps):
        new_gaps[2*i] = val
    for i, val in enumerate(even_gaps):
        new_gaps[2*i + 1] = val

    # Compute the minimal sum using the formula:
    # total = N * X[0] + sum_{j=1}^{N-1} (N - j) * new_gaps[j-1]
    total = N * X[0]
    for j, g in enumerate(new_gaps):
        total += (N - (j + 1)) * g

    print(total)

if __name__ == "__main__":
    solve()
```

## worker: Read \(N\) and the sorted list \(X\).
- The operation on four consecutive pieces `a < b < c < d` replaces the middle two by their reflections across the midpoint `(a+d)/2`.  
  This swaps the outer gaps while keeping the middle gap unchanged:  
  `g1 = b-a`, `g2 = c-b`, `g3 = d-c` → `g1' = g3`, `g2' = g2`, `g3' = g1`.
- Therefore the only allowed permutation of gaps is swapping gaps whose indices differ by 2.  
  The gaps form two independent chains: odd‑indexed gaps and even‑indexed gaps.  
  Any permutation inside each chain is reachable (by bubble‑sort using adjacent swaps of distance 2).
- The leftmost piece (`x₁`) and the rightmost piece (`x_N`) never move, so they are fixed.
- The sum of coordinates equals  
  `S = N·x₁ + Σ_{i=1}^{N-1} (N-i)·g_i`.  
  The weight `N-i` decreases as `i` increases, so we want larger gaps to have smaller weight.
- Because we can reorder gaps only within the same parity, the optimal arrangement is:
  * sort the odd‑indexed gaps in non‑decreasing order and place them at odd positions 1,3,5,…,
  * sort the even‑indexed gaps in non‑decreasing order and place them at even positions 2,4,6,…
- The algorithm runs in `O(N log N)` time (sorting) and `O(N)` memory, easily handling the limits (`N ≤ 2·10⁵`).
