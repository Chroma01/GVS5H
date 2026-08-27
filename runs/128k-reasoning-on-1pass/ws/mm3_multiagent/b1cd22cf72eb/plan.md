**Solution Explanation**

For every position `i ( 1 … N )`

* `U[i]` – length of the upper tooth  
* `D[i]` – length of the lower tooth  

Only the following operation is allowed

```
choose one tooth with positive length and decrease it by 1   (cost = 1)
```

So a tooth can become any integer value between `0` and its original length.

--------------------------------------------------------------------

#### 1.   What does “fit together well’’ mean ?

After all operations we have new lengths `U'[i] , D'[i]`.

```
U'[i] + D'[i] = H            (the same H for every i)          (1)
|U'[i] - U'[i+1]| ≤ X        for all i < N                     (2)
```

`H` must be an integer.  
From (1) we get `D'[i] = H – U'[i]`.  
Because a tooth cannot become negative, for a fixed `H`

```
max(0 , H - D[i]) ≤ U'[i] ≤ min(U[i] , H)                (3)
```

For a given `H` the set of possible values of `U'[i]` is the interval

```
A[i] = max(0 , H - D[i])                (lower bound)
B[i] = min(U[i] , H)                    (upper bound)
```

--------------------------------------------------------------------

#### 2.   Cost for a fixed `H`

The total reduction on the `i`‑th pair is

```
(U[i] - U'[i]) + (D[i] - D'[i]) = (U[i] + D[i]) - H
```

It does **not** depend on how the reduction is distributed between the
two teeth.  
Let  

```
S[i] = U[i] + D[i]          (original sum of the i‑th pair)
totalS = Σ S[i]
```

If we decide to use the common sum `H`, the total amount of money we have
to pay is

```
cost(H) = Σ (S[i] - H) = totalS - N·H                (4)
```

`cost(H)` is a linear decreasing function of `H`.  
Therefore the best `H` is the **largest** `H` for which a feasible
sequence `U'[i]` exists.

`H` can never be larger than `min_i S[i]`, because a pair can only be
shortened, never lengthened.

--------------------------------------------------------------------

#### 3.   Feasibility test for a given `H`

We have intervals `[A[i] , B[i]]` (3) and a Lipschitz condition  
`|U'[i] - U'[i+1]| ≤ X`.  
The classic way to test existence of a sequence with such constraints
is to keep the *range* of values that are still reachable for the
current position.

```
let L … R be the set of possible values of U'[i-1]
for the next position i
    U'[i] must belong to its own interval [A[i] , B[i]]
    and also be at distance ≤ X from at least one value in [L , R]
    → U'[i] ∈ [A[i] , B[i]] ∩ [L - X , R + X]
```

Therefore the new reachable interval is

```
L' = max( A[i] , L - X )
R' = min( B[i] , R + X )
```

If after some step `L' > R'` the instance is infeasible,
otherwise after processing all positions it is feasible.

The test works in `O(N)` time.

--------------------------------------------------------------------

#### 4.   Monotonicity

When `H` decreases, both `A[i]` and `B[i]` can only move **downwards**
(`A[i]` never increases, `B[i]` never increases).  
Consequently a sequence that works for a larger `H` can be “shifted
down’’ (maybe after a small local adjustment) to work for any smaller
`H`.  
Thus feasibility is monotone:

```
H feasible  ⇒  every H' < H feasible
```

Because of this monotonicity the maximum feasible `H` can be found by
binary search on the integer range `[0 , min_i S[i]]`.

--------------------------------------------------------------------

#### 5.   Whole algorithm

```
read N , X and all pairs (U[i] , D[i])
compute S[i] = U[i] + D[i] , totalS = Σ S[i] , minS = min S[i]

binary search lo = 0 , hi = minS
    while lo < hi
        mid = (lo + hi + 1) // 2
        if feasible(mid) : lo = mid
        else               : hi = mid - 1
Hmax = lo
answer = totalS - N * Hmax                (formula (4))
print answer
```

`feasible(H)` is the `O(N)` interval‑propagation test described in
section&nbsp;3.

--------------------------------------------------------------------

#### 6.   Correctness Proof  

We prove that the algorithm prints the minimum possible total cost.

---

##### Lemma 1  
For a fixed integer `H` the set of all possible values of `U'[i]`
satisfying (1) is exactly the interval `[A[i] , B[i]]` defined by (3).

**Proof.**  
From `U'[i] + D'[i] = H` we have `D'[i] = H - U'[i]`.  
`U'[i]` must be non‑negative and at most its original length `U[i]`;
`D'[i]` must be non‑negative and at most `D[i]`.  
These four inequalities are equivalent to (3). ∎



##### Lemma 2  
For a fixed `H` the total amount of money necessary to achieve (1) is
`cost(H) = totalS - N·H` (formula (4)), regardless of how the reductions
are distributed.

**Proof.**  
On the `i`‑th pair we have to reduce the sum from `S[i]` down to `H`,
i.e. by exactly `S[i] - H`.  
The operation reduces one unit of length for one yen, therefore the
total cost is the sum of these reductions,
`Σ (S[i] - H) = totalS - N·H`. ∎



##### Lemma 3  
For a fixed `H` the interval‑propagation test (`feasible(H)`) returns
*True* iff there exists a sequence `U'[i]` satisfying (1) and (2).

**Proof.**  
*If part.*  
Assume the test finishes with a non‑empty interval `[L,R]` for the last
position. By construction for every `i` the interval `[L_i,R_i]` equals
the set of values that can be assigned to `U'[i]` while respecting the
previous choices and the condition `|U'[i]-U'[i+1]| ≤ X`.  
Thus any value in the final interval can be taken for `U'[N]` and a
preceding value can be chosen for each earlier position – a feasible
sequence exists.

*Only‑if part.*  
Suppose a feasible sequence `U'[i]` exists.  
Induction over `i` shows that after processing position `i` the algorithm’s
interval `[L_i,R_i]` contains the true value `U'[i]`.  
Indeed, for `i=1` the interval is exactly `[A[1],B[1]]` (Lemma&nbsp;1) and
contains `U'[1]`.  
Assume it holds for `i-1`. Because `|U'[i]-U'[i-1]| ≤ X`,
`U'[i]` belongs to `[L_{i-1}-X , R_{i-1}+X]`.  
It also belongs to its own interval `[A[i],B[i]]`.  
Hence it lies in the intersection used by the algorithm, i.e. in the
new interval `[L_i,R_i]`.  
Thus the interval never becomes empty, the test returns *True*. ∎



##### Lemma 4  
If `H` is feasible, then every `H'` with `0 ≤ H' < H` is also feasible.

**Proof.**  
Decrease `H` by one. All lower bounds `A[i] = max(0, H-D[i])` can only
decrease, all upper bounds `B[i] = min(U[i],H)` can only decrease.
Therefore each interval `[A[i],B[i]]` for the new `H'` is a (not necessarily
strict) subset of the old interval shifted downwards.
Take a feasible sequence for the larger `H`.  
If a value exceeds the new upper bound, lower it to the new bound;
if it falls below the new lower bound, raise it to the new bound.
Because the original sequence already satisfies the Lipschitz condition
with bound `X`, the adjusted sequence also satisfies it – the adjustments
do not increase any difference by more than the amount the interval
moved, which is at most `1`. Repeating this argument for any number of
steps shows feasibility for all smaller `H`. ∎



##### Lemma 5  
`H_max` found by the binary search equals the maximum integer `H` for
which a feasible sequence exists.

**Proof.**  
By Lemma&nbsp;4 the predicate “`H` is feasible’’ is monotone:
*True, True, …, True, False, False, …*.  
Binary search on a monotone predicate always returns the largest index
with value *True*. ∎



##### Lemma 6  
Let `H_max` be the value returned by the binary search.
The minimum possible total amount of money equals `totalS - N·H_max`.

**Proof.**  
*Existence:* By Lemma&nbsp;5 there is a feasible sequence for `H_max`.
Using Lemma&nbsp;2 the cost of this sequence is exactly
`totalS - N·H_max`.

*Optimality:* Any feasible sequence uses some integer `H` (its common
sum). By Lemma&nbsp;5 we have `H ≤ H_max`.  
From Lemma&nbsp;2 the cost of any feasible sequence is
`totalS - N·H ≥ totalS - N·H_max`.  
Thus no solution can be cheaper than `totalS - N·H_max`. ∎



##### Theorem  
The algorithm prints the minimum total amount of money Takahashi has to
pay to make his teeth “fit together well”.

**Proof.**  
The algorithm

* computes `totalS` and `minS = min_i S[i]`,
* binary searches the largest feasible `H` (Lemma&nbsp;5) using the
  correct feasibility test (Lemma&nbsp;3),
* outputs `totalS - N·H_max`.

By Lemma&nbsp;6 this value is exactly the optimal cost. ∎



--------------------------------------------------------------------

#### 7.   Complexity Analysis

*Feasibility test* : `O(N)` time, `O(1)` extra memory.  
*Binary search* : at most `⌈log2(minS+1)⌉ ≤ 31` iterations.  

```
Total time   :  O(N log max(U_i+D_i))  ≤ 2·10^5 · 31  ≈ 6·10^6 operations
Total memory :  O(N)   (arrays U and D)
```

Both are easily fast enough for the given limits.

--------------------------------------------------------------------

#### 8.   Reference Implementation  (Python 3)

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
    minS = 10 ** 30                # larger than any possible sum

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
    # feasibility test for a given H
    def feasible(H: int) -> bool:
        # reachable interval for the previous position
        L = -10 ** 30
        R = 10 ** 30
        x = X
        Ul = U
        Dl = D
        for i in range(N):
            # interval of possible U'[i]
            low = H - Dl[i]
            if low < 0:
                low = 0
            up = Ul[i]
            if up > H:
                up = H

            # intersect with the shifted previous interval
            L = low if low > L - x else L - x
            R = up  if up  < R + x else R + x
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

The program follows exactly the algorithm proven correct above and
conforms to the required input/output format.