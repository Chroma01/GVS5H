
## ideation
```python
import sys

def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    N = next(it)
    M = next(it)
    P = [next(it) for _ in range(N)]

    # total cost of all units whose price is strictly less than X
    def cost_lt(X: int) -> int:
        total = 0
        for p in P:
            q = (X - 1) // p
            t = (q + 1) // 2
            total += p * t * t
            if total > M:
                break
        return total

    # find the largest X such that cost_lt(X) <= M
    lo = 0          # always feasible (cost of empty set = 0)
    hi = 1
    while cost_lt(hi) <= M:
        lo = hi
        hi <<= 1

    # binary search on [lo, hi]
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if cost_lt(mid) <= M:
            lo = mid
        else:
            hi = mid - 1
    X = lo                     # X is the maximal threshold described in the proof

    # compute the number of units cheaper than X and the number with price exactly X
    cnt_lt = 0        # F(X)  – number of units cheaper than X
    cost_lt_val = 0   # S(X)  – their total price
    cnt_eq = 0        # units with price exactly X

    for p in P:
        q = (X - 1) // p
        t = (q + 1) // 2
        cnt_lt += t
        cost_lt_val += p * t * t
        if X > 0 and (X % p == 0) and ((X // p) & 1):
            cnt_eq += 1

    remaining = M - cost_lt_val                 # money left after buying all cheaper units
    add = 0
    if X > 0:
        add = min(cnt_eq, remaining // X)

    print(cnt_lt + add)


if __name__ == "__main__":
    solve()
```

## worker: finalize
**Algorithm Overview**

For product `i` the price of the `j`‑th unit (the extra money for the `j`‑th copy) is  
`(2·j‑1)·P[i]`.  
If we list all units of all products by this incremental price and sort them,
the cheapest `x` units are exactly the first `x` elements of this list.
Hence the optimal purchase is a prefix of this sorted list.

Define `S(X)` = total cost of all units whose price is **strictly** smaller than `X`.  
`S(X)` is monotone non‑decreasing in `X`.  
Let `X*` be the largest integer with `S(X*) ≤ M`.  
All units cheaper than `X*` can be bought, and no unit with price larger than `X*`
can be bought. The only units we might still add are those priced exactly `X*`.

For a fixed `X` we can compute `S(X)` efficiently:

* For product `i`, the condition `(2·j‑1)·P[i] < X` is equivalent to  
  `2·j‑1 ≤ (X‑1)//P[i]`.  
  Let `q = (X‑1)//P[i]`. The number of admissible `j` is `t = (q+1)//2`.  
* The sum of the first `t` odd numbers is `t²`, so the cost contributed by
  product `i` is `P[i]·t²`.

Thus  
`S(X) = Σ P[i]·t[i]²` with `t[i] = ((X‑1)//P[i] + 1)//2`.

We binary‑search the maximal `X*` with `S(X*) ≤ M`.  
The search range is found by repeatedly doubling `hi` until `S(hi) > M`.  
Each evaluation of `S(X)` scans all `N` products, so the binary search costs
`O(N·log Xmax)` time (≈ 60·N operations).

After finding `X*` we also need:

* `cnt_lt = Σ t[i]` – number of units cheaper than `X*`.
* `cost_lt = S(X*)` – their total price.
* `cnt_eq` – number of products for which `X*` is an odd multiple of `P[i]`
  (i.e. there exists a unit priced exactly `X*`).

The remaining money is `R = M – cost_lt`.  
From the `cnt_eq` equally priced units we can afford at most `R // X*` of them,
so we add `add = min(cnt_eq, R // X*)` (if `X* > 0`).

The answer is `cnt_lt + add`.

**Correctness Proof**

*Lemma 1* – The incremental price of the `j`‑th unit of product `i` is `(2j‑1)P[i]`.  
*Proof.* Price of `k` units is `k²P[i]`. Difference between `k` and `k‑1` units is
`(k²-(k‑1)²)P[i] = (2k‑1)P[i]`. ∎

*Lemma 2* – For any `X ≥ 0` the number of units of product `i` with price `< X`
is `t[i] = ((X‑1)//P[i] + 1)//2` and their total cost is `P[i]·t[i]²`.  
*Proof.* `(2j‑1)P[i] < X ⇔ 2j‑1 ≤ (X‑1)//P[i]`. The right side is an integer `q`;
the largest odd number ≤ `q` is `2·⌊(q+1)/2⌋‑1`, giving exactly `⌊(q+1)/2⌋`
solutions for `j`. The sum of the first `t` odd numbers equals `t²`. ∎

*Lemma 3* – Let `X*` be the largest integer with `S(X*) ≤ M`.  
All units cheaper than `X*` are affordable, and no unit with price `> X*` is affordable.  
*Proof.* By definition `S(X*) ≤ M`, so the cheaper units fit in the budget.
If a unit with price `Y > X*` were affordable, then `S(Y) ≤ M + Y`.  
Monotonicity of `S` gives `S(Y) ≥ S(X*+1) > M` (maximality of `X*`), contradiction. ∎

*Lemma 4* – The maximal number of units equals  
`F(X*) + min(cnt_eq, (M‑S(X*)) // X*)`, where `F(X*)` is the number of units
cheaper than `X*` and `cnt_eq` the number of units priced exactly `X*`.  
*Proof.* All cheaper units are bought (Lemma 3). Their count is `F(X*)` and cost `S(X*)`.  
Remaining money `R = M‑S(X*)`. Any further unit must cost at least `X*`; the only
candidates are the `cnt_eq` units of price exactly `X*`. Each costs `X*`, so at most
`R // X*` can be added. Adding any unit of higher price would exceed the budget,
contradicting Lemma 3. ∎

*Lemma 5* – The binary search returns exactly `X*`.  
*Proof.* `S(X)` is monotone (Lemma 2). The loop maintains the invariant
“`lo` feasible, `hi` infeasible”. The standard binary search on a monotone
predicate therefore ends with `lo = X*`. ∎

*Lemma 6* – The final loop computes `cnt_lt = F(X*)`, `cost_lt = S(X*)`,
and `cnt_eq` as defined.  
*Proof.* It uses the formulas of Lemma 2 with `X = X*`. The condition
`X % p == 0 and (X//p) odd` is precisely the existence of a unit of price `X*`. ∎

*Theorem* – The program outputs the maximum possible total number of units.  
*Proof.* By Lemma 5 the program obtains the correct threshold `X*`.  
Lemma 6 shows it correctly evaluates `F(X*)`, `S(X*)` and `cnt_eq`.  
The added amount `add` equals the second term of Lemma 4, so the printed value
`cnt_lt + add` is exactly the optimum. ∎

**Complexity Analysis**

* `S(X)` evaluation: `O(N)`.
* Binary search: at most `⌈log₂ Xmax⌉ ≤ 60` iterations.
* Total time: `O(N·log Xmax) ≤ 2·10⁵·60 ≈ 1.2·10⁷` operations.
* Memory: `O(N)` for the list of prices.

Both are well within the limits for Python.
