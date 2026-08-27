**Solution Explanation**

For every product `i`

* the price of buying `k` units is `k² · P[i]`
* the *incremental* price of the `j`‑th unit (the extra money we have to pay when we
  already have `j‑1` units) is  

```
(2·j – 1) · P[i]          ( 1·P , 3·P , 5·P , … )
```

If we list all incremental prices of all products and sort them,
the cheapest `x` prices are the cheapest `x` units we can ever buy.
Therefore

* the optimal set of bought units is a **prefix** of this sorted list,
* the minimal total price for `x` units is the sum of the first `x` prices,
* we have to find the largest `x` whose sum does not exceed the given budget `M`.

--------------------------------------------------------------------

#### 1.   How many units are cheaper than a given value `X` ?

For a fixed `X` (`X ≥ 0`)

```
(2·j – 1)·P[i] ≤ X   ⇔   2·j – 1 ≤ X / P[i]
```

`q = ⌊ X / P[i] ⌋` is the biggest odd number allowed,  
the number of such `j` is  

```
t[i] = ⌊ (q + 1) / 2 ⌋ = ( X // P[i] + 1 ) // 2
```

All those `t[i]` units are cheaper than `X`.  
The total number of units cheaper than `X`

```
F(X) = Σ t[i]
```

and the total price of those units

```
S(X) = Σ P[i]·t[i]²                ( Σ of first t[i] odd numbers = t[i]² )
```

Both `F` and `S` are monotone non‑decreasing in `X`.

--------------------------------------------------------------------

#### 2.   From “price of a prefix’’ to the answer

Let `X*` be the **largest** value for which we can still afford *all*
units cheaper than `X*` :

```
S(X*) ≤ M ,      S(X*+1) > M               (1)
```

*All* units cheaper than `X*` are bought – their number is `F(X*)`.  
The next possible units have price exactly `X*` (or larger).  
Among the units with price exactly `X*` each product can contribute at most one
(the equation `(2·j-1)·P[i] = X*` has at most one integer solution).

```
cnt_eq = #{ i | X* % P[i] == 0 and (X* / P[i]) is odd }
```

The already spent money is `S(X*)`.  
The remaining money is `R = M – S(X*)`.  
From the `cnt_eq` equally priced units we can afford at most

```
add = min( cnt_eq , R // X* )          (if X* > 0)
```

Hence the maximal number of units we can buy is

```
answer = F(X*) + add
```

`X*` can be found by a binary search because `S(X)` is monotone.

--------------------------------------------------------------------

#### 3.   Algorithm
```
read N, M and the list P[1…N]

#--- find the largest X with S(X) ≤ M  (cost of all units cheaper than X) ---
lo = 0                     # always feasible (S(0)=0)
hi = 1
while S(hi) ≤ M:           # double until it becomes infeasible
        lo = hi
        hi <<= 1

while lo < hi:             # binary search on [lo , hi]
        mid = (lo + hi + 1) // 2
        if S(mid) ≤ M:  lo = mid
        else:          hi = mid - 1
X = lo                     # X is the wanted X*

#--- compute the answer for this X ---
cnt_lt   = 0               # F(X)  – number of units cheaper than X
cost_lt  = 0               # S(X)  – their total price
cnt_eq   = 0               # units with price exactly X

for p in P:
        q = (X-1) // p                # (X-1) because we need *strictly* < X
        t = (q + 1) // 2              # t[i] = number of units cheaper than X
        cnt_lt   += t
        cost_lt  += p * t * t
        if X > 0 and X % p == 0 and ((X // p) & 1):
                cnt_eq += 1            # this product has a unit of price X

remaining = M - cost_lt                 # money left after buying all cheaper units
add = 0
if X > 0:
        add = min(cnt_eq, remaining // X)

print(cnt_lt + add)
```

`S(x)` (the cost of all units cheaper than `x`) is evaluated in `O(N)` :

```
def S(x):
        total = 0
        for p in P:
                q = (x-1) // p
                t = (q + 1) // 2
                total += p * t * t
                if total > M:          # early stop, we only need the comparison
                        break
        return total
```

The binary search needs at most `⌈log₂ Xmax⌉ ≤ 60` iterations,
each iteration scans all `N` products, therefore

```
time   :  O( N · log Xmax )   ≤ 2·10⁵ · 60   ≈ 1.2·10⁷ operations
memory :  O( N )
```

Both are easily fast enough in Python.

--------------------------------------------------------------------

#### 4.   Correctness Proof  

We prove that the algorithm prints the maximum possible number of units.

---

##### Lemma 1  
For every product `i` and every non‑negative integer `k`

```
price of the (k+1)-st unit of product i   =   (2·k+1)·P[i] .
```

**Proof.**  
Price of `k+1` units: `(k+1)²·P[i]`.  
Price of `k` units: `k²·P[i]`.  
Difference: `(k+1)²·P[i] – k²·P[i] = (2k+1)·P[i]`. ∎



##### Lemma 2  
For a fixed `X ≥ 0` the number of units whose price is **strictly**
smaller than `X` equals  

```
t[i] = ( (X-1) // P[i] + 1 ) // 2
```

and the total price of all those units equals  

```
S(X) = Σ P[i]·t[i]² .
```

**Proof.**  
` (2·j-1)·P[i] < X  ⇔  2·j-1 ≤ (X-1) // P[i]`.  
The right hand side is an integer `q`. The largest odd number ≤ `q` is
`2·⌊(q+1)/2⌋-1`, therefore the number of admissible `j` is `⌊(q+1)/2⌋`,
exactly the formula for `t[i]`.  
The sum of the first `t` odd numbers is `t²`, so the total price of those
`t[i]` units is `P[i]·t[i]²`. ∎



##### Lemma 3  
Let `X*` be the largest integer with `S(X*) ≤ M`.  
All units cheaper than `X*` can be bought, and **no** unit with price
greater than `X*` can be bought.

**Proof.**  
By definition `S(X*) ≤ M` – the money for all those cheaper units fits
into the budget, so they are affordable.

Assume there exists a unit with price `Y > X*` that could be bought.
All units with price `< Y` are also cheaper than `Y`, therefore
`S(Y) ≤ M + Y`.  
Because `Y > X*` and `S` is monotone, `S(Y) ≥ S(X*+1) > M`
(the maximality of `X*`).  
Thus `M + Y ≥ S(Y) > M`, a contradiction. ∎



##### Lemma 4  
The maximal number of units that can be bought is  

```
F(X*) + min( cnt_eq , (M - S(X*)) // X* )
```

where  

* `F(X*)` is the number of units cheaper than `X*`,
* `cnt_eq` is the number of units whose price equals `X*`.

**Proof.**  
All units cheaper than `X*` are bought (Lemma&nbsp;3).  
Their count is `F(X*)` and their total price is `S(X*)`.  
The remaining money is `R = M – S(X*)`.

The only further units we could still add are the ones priced exactly `X*`
(because any unit priced larger would make `S` exceed `M`).  
Each such unit costs `X*`, therefore at most `R // X*` of them fit.
Only `cnt_eq` units of that price exist, hence we can add at most
`min(cnt_eq , R // X*)`.  
Adding any more would either need more money or a price larger than `X*`,
both impossible by Lemma&nbsp;3. ∎



##### Lemma 5  
The algorithm finds the value `X*` described in Lemma&nbsp;3.

**Proof.**  
`S(X)` is monotone (Lemma&nbsp;2).  
The algorithm performs a standard binary search on the integer interval
`[0, hi]` where `hi` is the first value with `S(hi) > M`.  
The invariant “`lo` is feasible, `hi` is infeasible’’ is preserved,
so after the loop `lo` is the greatest feasible `X`, i.e. exactly `X*`. ∎



##### Lemma 6  
For the value `X*` found by the algorithm the program computes

```
cnt_lt = F(X*) ,    cost_lt = S(X*) ,    cnt_eq = #{ i | X* % P[i]==0 and (X* / P[i]) odd } .
```

**Proof.**  
The loop uses the formulas of Lemma&nbsp;2 with `X = X*`,
hence `t = ((X*-1)//P[i] + 1)//2` equals the number of units cheaper than `X*`.
Summation gives `cnt_lt = F(X*)` and `cost_lt = S(X*)`.  

`cnt_eq` is increased exactly when `X*` is an odd multiple of `P[i]`,
i.e. when the product has a unit of price `X*`. ∎



##### Lemma 7  
`add = min(cnt_eq , (M - cost_lt) // X*)` computed by the program equals
the second term in Lemma&nbsp;4.

**Proof.**  
`cost_lt = S(X*)` and `M - cost_lt` is the remaining money `R`.  
`X* > 0` in the division, otherwise `add` is set to `0`, which is correct
because no unit has price `0`. ∎



##### Theorem  
The number printed by the program equals the maximum possible total
number of units that can be bought with at most `M` yen.

**Proof.**  
By Lemma&nbsp;5 the program obtains the correct threshold `X*`.  
Lemma&nbsp;6 shows that the program correctly evaluates
`F(X*)`, `S(X*)` and `cnt_eq`.  
Lemma&nbsp;7 shows that the program computes exactly the second term
of Lemma&nbsp;4.
Consequently the final value `cnt_lt + add` equals the expression of
Lemma&nbsp;4, which is the optimal number of units. ∎



--------------------------------------------------------------------

#### 5.   Complexity Analysis

```
N ≤ 2·10⁵ ,   M ≤ 10¹⁸
Xmax ≤ 2·10¹⁴   (at most 2·√(M·max(P)) )
```

*Binary search* : at most `⌈log₂ Xmax⌉ ≤ 60` iterations.  
Each iteration scans all `N` products (`O(N)`).  

```
Time   :  O( N · log Xmax )   ≤ 2·10⁵ · 60   ≈ 1.2·10⁷ operations
Memory :  O( N )
```

Both well within the limits for Python.

--------------------------------------------------------------------

#### 6.   Reference Implementation  (Python 3)

```python
import sys

def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    N = next(it)
    M = next(it)
    P = [next(it) for _ in range(N)]

    # ---------- helper: total cost of all units with price < X ----------
    def cost_lt(X: int) -> int:
        """sum_i P[i] * t[i]^2, where t[i] = ((X-1)//P[i] + 1)//2
           (units whose price is strictly smaller than X)"""
        total = 0
        # loop over all products, stop early if already over M
        for p in P:
            q = (X - 1) // p
            t = (q + 1) // 2
            total += p * t * t
            if total > M:
                break
        return total

    # ---------- find the largest X with cost_lt(X) <= M ----------
    lo = 0          # always feasible (cost of empty set = 0)
    hi = 1
    while cost_lt(hi) <= M:
        lo = hi
        hi <<= 1          # double until it becomes infeasible

    # binary search on [lo, hi]
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if cost_lt(mid) <= M:
            lo = mid
        else:
            hi = mid - 1
    X = lo                     # X is the maximal threshold described in the proof

    # ---------- compute the answer for this X ----------
    cnt_lt = 0        # number of units cheaper than X
    cost_lt_val = 0   # their total price
    cnt_eq = 0        # units whose price equals exactly X

    for p in P:
        q = (X - 1) // p
        t = (q + 1) // 2
        cnt_lt += t
        cost_lt_val += p * t * t

        if X > 0 and (X % p == 0) and ((X // p) & 1):
            cnt_eq += 1

    remaining = M - cost_lt_val
    add = 0
    if X > 0:
        add = min(cnt_eq, remaining // X)

    print(cnt_lt + add)


if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required input / output format.