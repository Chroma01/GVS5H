
## ideation
### Solution Explanation

For a lattice point `(x , y)` (`0 ≤ x ≤ W , 0 ≤ y ≤ H`) we call it a **block** if it is not inside the
forbidden rectangle  

```
L ≤ x ≤ R   and   D ≤ y ≤ U                                   (1)
```

All other points of the rectangle are empty (no block).  
Snuke may

* start on any block,
* repeatedly move one unit to the right or upward,
* the destination must also be a block.

A *path* is the sequence of visited blocks, the empty path (length 0) is also allowed.
We have to count all possible paths modulo  

```
MOD = 998244353   (prime)
```

--------------------------------------------------------------------

#### 1.   DP on the whole board

If the rectangle did **not** exist, the whole board `(0…W) × (0…H)` would be a full grid.
For a point `(x , y)` let

```
full[x][y] = number of monotone paths that start at (x , y) and stay inside the full board
```

A path is completely described by the numbers of right moves `dx` and up moves `dy`.
The number of different orders of these moves is the binomial coefficient `C(dx+dy , dx)`.
Summation over all admissible `dx , dy` gives

```
full[x][y] = Σ_{dx=0}^{W-x} Σ_{dy=0}^{H-y} C(dx+dy , dx)
           = C( (W-x)+(H-y)+2 , (W-x)+1 ) – 1                (2)
```

(The `–1` removes the empty path from the double sum.)

--------------------------------------------------------------------

#### 2.   What must be subtracted?

`full[x][y]` counts **all** monotone paths from `(x , y)` in the full board.
A path is valid only if it never steps into the rectangle.
The total number of paths that start **anywhere** (including forbidden points) is

```
TOTAL = Σ_{all points} full[x][y]                              (3)
```

We can compute `TOTAL` without enumerating all points.
From (2) with `i = W-x , j = H-y`

```
TOTAL = Σ_{i=0}^{W} Σ_{j=0}^{H} ( C(i+j+2 , i+1) – 1 )
      = C(W+H+4 , W+2) – (W+H+4) – (W+1)(H+1)                 (4)
```

The first term is the sum of the binomial part, the second term removes the `–1` for each
of the `(W+1)(H+1)` points.

Now we have to remove everything that is not allowed.

* **Points inside the rectangle** are not blocks, therefore the contribution of
  these points must be removed completely:

  ```
  BLOCKED = Σ_{x=L}^{R} Σ_{y=D}^{U} full[x][y]                  (5)
  ```

* **Paths that start outside the rectangle but first step into it**
  are also invalid.  
  The first such step can only be from the left side (`x = L`) or from the bottom side
  (`y = D`), because a step from inside the rectangle would already be invalid.
  For a fixed entry point we count the number of ways to reach the neighbour
  outside, multiply by the number of possible continuations (the `full` value of the
  entry point) and sum over all possible entry points.

  *Entry from the left side* (`x = L`):
  The neighbour is `(L-1 , y)`.  
  All paths that end there staying left of the rectangle are counted by
  `leftCnt(y) = C(L + y + 1 , L) – 1`.  
  The continuation after entering is `full[L][y]`.  
  Hence

  ```
  Sleft = Σ_{y=D}^{U} leftCnt(y) · full[L][y]                  (6)
  ```

  *Entry from the bottom side* (`y = D`) is symmetric:

  ```
  Sbottom = Σ_{x=L}^{R} bottomCnt(x) · full[x][D]              (7)
  bottomCnt(x) = C(x + D + 1 , x+1) – 1
  ```

All invalid paths are counted exactly once in `Sleft + Sbottom`.

--------------------------------------------------------------------

#### 3.   Closed forms for the sums

All needed sums have simple closed formulas.

*Sum over the rectangle* (5)  
For a fixed column `x = i` let `dx = W-i`.  
`full[i][y] = C(dx + (H-y) + 2 , dx+1) – 1`.  
Put `t = H-y`; then `t` runs from `a = H-U` to `b = H-D`.  

```
Σ_{t=a}^{b} C(dx + t + 2 , dx+1)
    = C(dx + b + 3 , dx+2) – C(dx + a + 2 , dx+2)            (8)
```

The `–1` part contributes `U-D+1` rows, therefore

```
BLOCKED = Σ_{i=L}^{R} ( C(dx+b+3,dx+2) – C(dx+a+2,dx+2) – (U-D+1) )   (9)
```

*Left entry sum* (6) and *bottom entry sum* (7) are ordinary loops over at most
`10⁶` elements – easily fast enough.

--------------------------------------------------------------------

#### 4.   Final formula

```
Ans = TOTAL               –  BLOCKED  –  Sleft  –  Sbottom          (10)
```

All terms are taken modulo `MOD`.

--------------------------------------------------------------------

#### 5.   Computing binomial coefficients

All binomials are of the form `C(n , k)` with  

```
n ≤ W + H + 4   ( ≤ 2·10⁶ + 4 )
k ≤ W + 2
```

We pre‑compute factorials and inverse factorials up to `W+H+5`,
then evaluate each binomial in `O(1)` time.

--------------------------------------------------------------------

#### 6.   Correctness Proof  

We prove that the algorithm returns exactly the number of admissible paths.

---

##### Lemma 1  
For any point `(x , y)` the number of monotone lattice paths that start there
and stay inside the full board is given by (2).

**Proof.**  
A path is described by `dx` right moves and `dy` up moves, the number of
different orders is `C(dx+dy , dx)`. Summation over all `dx , dy` with
`0 ≤ dx ≤ W-x , 0 ≤ dy ≤ H-y` yields the double sum.
The well‑known Vandermonde‑type identity  

```
Σ_{dx=0}^{A} Σ_{dy=0}^{B} C(dx+dy , dx) = C(A+B+2 , A+1) – 1
```

transforms the sum to the right hand side of (2). ∎



##### Lemma 2  
`TOTAL` computed by (4) equals `Σ_{all points} full[x][y]`.

**Proof.**  
Replace `i = W-x , j = H-y`. Then `full[x][y] = C(i+j+2 , i+1) – 1`.  
Summing over all `i , j` gives the double sum of the binomial part
minus `(W+1)(H+1)`.  
The double sum is `C(W+H+4 , W+2) – (W+H+4)` (another standard identity),
hence (4). ∎



##### Lemma 3  
For a fixed column `x = i` (`L ≤ i ≤ R`) the sum of `full` over the rows
`D … U` equals the expression inside the sum of (9).

**Proof.**  
With `dx = W-i` and `t = H-y` we have
`full[i][y] = C(dx + t + 2 , dx+1) – 1`.  
Summation over `t = a … b` (where `a = H-U , b = H-D`) uses the partial‑sum
identity  

```
Σ_{t=0}^{k} C(dx + t + 2 , dx+1) = C(dx + k + 3 , dx+2) – 1
```

which gives (8). Subtracting `1` for each of the `U-D+1` rows yields the term
in (9). ∎



##### Lemma 4  
`Sleft` defined in (6) equals the number of admissible paths whose **first**
forbidden point lies on the left side of the rectangle.

**Proof.**  
A path that first enters the rectangle at `(L , y)` must reach the neighbour
`(L-1 , y)` without ever touching the rectangle, then step right.
All points left of the rectangle form a full board of width `L`
(`x = 0 … L-1`). The number of monotone paths ending at `(L-1 , y)` inside that
board is exactly `leftCnt(y) = C(L+y+1 , L) – 1` (Lemma&nbsp;1 applied to the
left board). After the entering step the continuation can be any monotone path
inside the whole board, counted by `full[L][y]`. Multiplying and summing over
all `y` gives (6). ∎



##### Lemma 5  
`Sbottom` defined in (7) equals the number of admissible paths whose first
forbidden point lies on the bottom side of the rectangle.

**Proof.**   Symmetric to Lemma&nbsp;4, using the neighbour `(x , D-1)`. ∎



##### Lemma 6  
Every admissible path that ever visits the rectangle is counted **once**
in `Sleft + Sbottom`.

**Proof.**  
The first forbidden point of such a path cannot be inside the rectangle,
because the previous step must come from outside.
Hence its first forbidden point has either `x = L` (entered from the left) or
`y = D` (entered from the bottom). The two cases are disjoint, therefore the
path is counted either in `Sleft` (Lemma&nbsp;4) or in `Sbottom` (Lemma&nbsp;5) and
never in both. ∎



##### Lemma 7  
`TOTAL – BLOCKED – Sleft – Sbottom` equals the sum of `dp[x][y]` over all
blocks.

**Proof.**  
`TOTAL` is the sum of `full` over **all** board points (Lemma&nbsp;2).  
Subtracting `BLOCKED` removes the contribution of the forbidden points,
leaving the sum of `full` over all blocks.  
Any remaining term corresponds to a path that starts on a block.
If the path never visits the rectangle it is already a valid path and is kept.
If it does visit the rectangle, its first forbidden point is counted exactly
once in `Sleft + Sbottom` (Lemma&nbsp;6). Subtracting that sum removes all such
invalid paths. The remaining terms are exactly the numbers of valid paths
starting at each block, i.e. the required sum of `dp`. ∎



##### Lemma 8  
The program computes `TOTAL`, `BLOCKED`, `Sleft` and `Sbottom` exactly as
described in Lemmas&nbsp;2–5.

**Proof.**  
`TOTAL` is evaluated by the closed formula (4).  
`BLOCKED` uses the per‑column formula (9) derived in Lemma&nbsp;3, summed over
all columns `i = L … R`.  
`Sleft` and `Sbottom` are computed by the direct loops (6) and (7).  
All binomial coefficients are obtained from pre‑computed factorials, therefore
the numerical values are identical to the mathematical definitions. ∎



##### Theorem  
The number printed by the program equals the number of possible paths Snuke
could have taken (mod 998 244 353).

**Proof.**  
By Lemma&nbsp;8 the program obtains the exact values of the four quantities in
(10). Lemma&nbsp;7 shows that the combination performed in (10) is precisely the
sum of `dp[x][y]` over all blocks, which by definition is the answer. ∎



--------------------------------------------------------------------

#### 7.   Complexity Analysis

```
pre‑computation of factorials :  O(W+H)      ( ≤ 2·10⁶ )
loop over i = L … R          :  O(R-L+1)    ( ≤ 10⁶ )
loop over y = D … U          :  O(U-D+1)    ( ≤ 10⁶ )
remaining work                :  O(1)
memory                       :  O(W+H)      (factorials)
```

Both time and memory easily satisfy the limits.

--------------------------------------------------------------------

#### 8.   Reference Implementation  (Python 3)

```python
import sys

MOD = 998244353

def main() -> None:
    W, H, L, R, D, U = map(int, sys.stdin.readline().split())

    # ---------- pre‑compute factorials ----------
    max_n = W + H + 5          # safe upper bound for all binomials
    fact = [1] * (max_n + 1)
    for i in range(1, max_n + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (max_n + 1)
    inv_fact[max_n] = pow(fact[max_n], MOD - 2, MOD)
    for i in range(max_n, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    def C(n: int, k: int) -> int:
        if k < 0 or k > n:
            return 0
        return fact[n] * inv_fact[k] % MOD * inv_fact[n - k] % MOD

    # ---------- TOTAL : sum of full over the whole board ----------
    total = (C(W + H + 4, W + 2) - (W + H + 4) - (W + 1) * (H + 1)) % MOD

    # ---------- sum of full over the forbidden rectangle ----------
    blocked = 0
    rows = U - D + 1
    a = H - U          # smallest t = H - j
    b = H - D          # largest  t = H - j
    for i in range(L, R + 1):
        dx = W - i
        # sum_{j=D}^{U} C(dx + (H-j) + 2 , dx + 1)
        # = C(dx+b+3,dx+2) - C(dx+a+2,dx+2)
        sumC = (C(dx + b + 3, dx + 2) - C(dx + a + 2, dx + 2)) % MOD
        blocked = (blocked + sumC - rows) % MOD

    # ---------- paths that first enter the rectangle ----------
    # helper: full[x][y] for the full board
    def full(x: int, y: int) -> int:
        dx = W - x
        dy = H - y
        return (C(dx + dy + 2, dx + 1) - 1) % MOD

    # left side (x = L)
    Sleft = 0
    if L > 0:                 # otherwise no neighbour to the left
        for j in range(D, U + 1):
            leftCnt = (C(L + j + 1, L) - 1) % MOD
            dp_after = full(L, j)
            Sleft = (Sleft + leftCnt * dp_after) % MOD

    # bottom side (y = D)
    Sbottom = 0
    if D > 0:                 # otherwise no neighbour below
        for i in range(L, R + 1):
            bottomCnt = (C(i + D + 1, i + 1) - 1) % MOD
            dp_after = full(i, D)
            Sbottom = (Sbottom + bottomCnt * dp_after) % MOD

    # ---------- final answer ----------
    ans = (total - blocked - Sleft - Sbottom) % MOD
    print(ans)


if __name__ == "__main__":
    main()
```

The program follows exactly the algorithm proven correct above
and conforms to the required time and memory limits.

## worker: Write the full Python implementation in the CURREN
The solution counts all monotone paths that start on a block (i.e., a lattice point not inside the rectangle \([L,R]\times[D,U]\)).  
For the full board the number of paths from a point \((x,y)\) is  

\[
\text{full}[x][y]=\sum_{dx=0}^{W-x}\sum_{dy=0}^{H-y}\binom{dx+dy}{dx}
                 =\binom{(W-x)+(H-y)+2}{W-x+1}-1 .
\]

Summing \(\text{full}\) over the whole board gives the closed form  

\[
\text{TOTAL}= \binom{W+H+4}{W+2}-(W+H+4)-(W+1)(H+1).
\]

From this we subtract the contributions of the forbidden rectangle and of all paths that start outside the rectangle but first step into it.  
A path can first enter only from the left side (\(x=L\)) or the bottom side (\(y=D\)).  
For a left entry at \((L,j)\) the number of ways to reach the neighbour \((L-1,j)\) is  

\[
\text{leftCnt}(j)=\binom{L+j+1}{L}-1,
\]

and after entering the continuation can be any path counted by \(\text{full}[L][j]\).  
The bottom side is symmetric.  
All these sums are evaluated in \(O(1)\) per point using pre‑computed factorials, giving an overall \(O(W+H)\) time algorithm with \(O(W+H)\) memory.
