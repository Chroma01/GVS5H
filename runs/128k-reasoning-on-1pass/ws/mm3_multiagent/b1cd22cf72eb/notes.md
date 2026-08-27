
## ideation
```python
import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    X = int(next(it))

    U = [0] * N
    D = [0] * N
    totalS = 0
    minS = 10 ** 30  # larger than any possible sum

    for i in range(N):
        u = int(next(it))
        d = int(next(it))
        U[i] = u
        D[i] = d
        s = u + d
        totalS += s
        if s < minS:
            minS = s

    # ------------------------------------------------------------
    # Feasibility test for a given common sum H
    def feasible(H: int) -> bool:
        # reachable interval for the previous position
        L = -10 ** 30
        R = 10 ** 30
        x = X
        for i in range(N):
            # interval of possible U'[i] for this position
            low = H - D[i]
            if low < 0:
                low = 0
            up = U[i]
            if up > H:
                up = H

            # intersect with the shifted previous interval
            L = low if low > L - x else L - x   # max(low, L - X)
            R = up  if up  < R + x else R + x   # min(up,  R + X)
            if L > R:
                return False
        return True
    # ------------------------------------------------------------

    lo, hi = 0, minS
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1

    Hmax = lo
    answer = totalS - N * Hmax
    print(answer)


if __name__ == "__main__":
    solve()
```

## worker: finalize
The solution follows the described algorithm:

1. For each pair `i` compute `S[i] = U[i] + D[i]`.  
   If we decide to end with a common sum `H`, the total cost is `Σ(S[i]−H) = totalS − N·H`, which depends only on `H`.  
   Hence we must maximize `H`.

2. `H` can be at most `min_i S[i]`, because a pair can only be shortened.

3. For a fixed `H` the allowed range for the upper tooth is  
   `[A[i], B[i]] = [max(0, H−D[i]), min(U[i], H)]`.  
   We also need `|U'[i]−U'[i+1]| ≤ X`.

4. Feasibility of a given `H` is tested in `O(N)` by maintaining the
   reachable interval `[L,R]` of possible values for the current
   position and intersecting it with `[A[i],B[i]]` and the shifted
   previous interval `[L−X, R+X]`. If the interval becomes empty, the
   `H` is infeasible.

5. Feasibility is monotone: if `H` works, any smaller `H` also works.
   Therefore the maximum feasible `H` is found by binary search on
   `[0, minS]`.

6. The answer is `totalS − N·Hmax`, which is the minimum possible cost.

Complexities: `O(N log max(U_i+D_i))` time (≈ 6·10⁶ operations for the limits) and `O(N)` additional memory.

The program reads all input from standard input, executes the algorithm, and prints the result.
