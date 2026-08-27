**Solution Explanation**

For a lattice point `(x , y)` (`0 ≤ x ≤ W , 0 ≤ y ≤ H`) we call it a *block* if

```
x < L   or   x > R   or   y < D   or   y > U                     (1)
```

All other points are forbidden – they contain no block.

Snuke may start on any block, then repeatedly move one step

```
(x , y) → (x+1 , y)   or   (x , y+1)
```

but the destination also has to be a block.
A *path* is the sequence of visited points, the length may be `0`
(the trivial path that stays where he started).

We have to count all possible paths, modulo  

```
MOD = 998244353   (prime)
```

--------------------------------------------------------------------

#### 1.   DP formulation

For every block `(x , y)` let  

```
dp[x][y] = number of paths that start at (x , y) and stay inside the block set
```

The obvious recurrence (moving only right or up) is

```
dp[x][y] = 1                                 (the trivial path)
           + (if (x+1 , y) is a block) dp[x+1][y]
           + (if (x , y+1) is a block) dp[x][y+1]                (2)
```

The answer we need is

```
Ans = Σ  dp[x][y]   over all blocks (x , y)                     (3)
```

--------------------------------------------------------------------

#### 2.   Paths that never visit the forbidden rectangle

If the forbidden rectangle did **not** exist, the whole board would be a
` (W+1) × (H+1) ` grid.
For a point `(x , y)` the number of monotone paths to any point
inside that full grid is a well known binomial:

```
full[x][y] = Σ_{dx=0}^{W-x} Σ_{dy=0}^{H-y} C(dx+dy , dx)
          = C( (W-x)+(H-y)+2 , (W-x)+1 )  – 1                (4)
```

(`–1` because the empty path to the point itself is not counted in the
double sum.)

The forbidden rectangle removes the points

```
L ≤ x ≤ R ,   D ≤ y ≤ U                                      (5)
```

Consequently

```
Ans = Σ_{all points} full[x][y]          –   Σ_{forbidden points} full[x][y]
    – (paths that start outside the rectangle and first enter it)      (6)
```

The three terms can be computed without enumerating all points.

--------------------------------------------------------------------

#### 3.   Sum of `full` over the whole board

From (4)

```
full[x][y] depends only on (dx , dy) = (W-x , H-y)
```

Let `i = W-x , j = H-y` (`0 ≤ i ≤ W , 0 ≤ j ≤ H`).

```
Σ_{all} full = Σ_{i=0}^{W} Σ_{j=0}^{H} ( C(i+j+2 , i+1) – 1 )
             =  ( Σ_{i,j} C(i+j+2 , i+1) ) – (W+1)(H+1)
```

The double sum of the binomial is known (a simple Vandermonde‑type
identity)

```
Σ_{i=0}^{W} Σ_{j=0}^{H} C(i+j+2 , i+1) = C(W+H+4 , W+2) – (W+H+4)    (7)
```

Therefore

```
TOTAL = C(W+H+4 , W+2) – (W+H+4) – (W+1)(H+1)                (8)
```

`TOTAL` is the first term of (6).

--------------------------------------------------------------------

#### 4.   Sum of `full` over the forbidden rectangle

For a fixed `x = i` (`L ≤ i ≤ R`) we need

```
Σ_{j=D}^{U} full[i][j] = Σ_{j=D}^{U} ( C( (W-i)+(H-j)+2 , (W-i)+1 ) – 1 )
```

Put `dx = W-i` and `t = H-j` (`t` runs from `H-U` to `H-D`).

```
Σ_{t=a}^{b} C( dx + t + 2 , dx + 1 )                (9)
```

(`a = H-U , b = H-D`)

The partial sums of this binomial are again elementary:

```
P(t) = Σ_{k=0}^{t} C(dx+k+2 , dx+1)
     = C(dx+t+3 , dx+2) – 1                         (10)
```

Hence the sum (9) equals

```
C(dx+b+3 , dx+2) – C(dx+a+2 , dx+2)                (11)
```

The wanted sum of `full` for this column is the value (11) minus the
number of rows `U-D+1`.

Doing this for all `i = L … R` gives the second term of (6).

The loop needs at most `R-L+1 ≤ 10^6` iterations – easily fast enough.

--------------------------------------------------------------------

#### 5.   Paths that first enter the rectangle

A path can **first** be inside the rectangle only at a point on its
left side (`x = L`) or on its bottom side (`y = D`), because the
preceding step must come from outside the rectangle.

*Entry from the left side*  
The previous point is `(L-1 , j)` (`D ≤ j ≤ U`).  
All paths that end at this neighbour stay completely left of the
rectangle, therefore the number of such paths is the same as in a
full board of width `L` :

```
leftCnt(j) = C( (L-1) + j + 2 , (L-1) + 1 ) – 1
           = C( L + j + 1 , L ) – 1                     (12)
```

After reaching `(L , j)` the continuation can be any monotone path
inside the *full* board, counted by `full[L][j]`.

Hence the contribution of all left‑side entries is

```
Sleft = Σ_{j=D}^{U} leftCnt(j) * full[L][j]            (13)
```

*Entry from the bottom side* – completely symmetric:

```
bottomCnt(i) = C( i + D + 1 , i + 1 ) – 1               (14)
Sbottom = Σ_{i=L}^{R} bottomCnt(i) * full[i][D]        (15)
```

Both sums are evaluated by simple loops (`≤ 10^6` iterations).

The third term of (6) is `Sbad = Sleft + Sbottom`.

--------------------------------------------------------------------

#### 6.   Final formula

Putting everything together

```
Ans = TOTAL                                 // (8)
    – Σ_{forbidden points} full               // section 4
    – Sleft – Sbottom                        // section 5
      (all modulo MOD)                       (16)
```

All needed binomial coefficients are of the form `C(n,k)` with

```
n ≤ W + H + 5   ( ≤ 2·10^6 + 5 )
k ≤ W + 2
```

so factorials up to `W+H+5` are pre‑computed, `C` is obtained in
`O(1)` time, and the whole algorithm works in `O(W+H)` time
(`≈ 2·10^6` operations) and `O(W+H)` memory.

--------------------------------------------------------------------

#### 7.   Correctness Proof  

We prove that the algorithm returns exactly the number of admissible
paths.

---

##### Lemma 1  
For a point `(x , y)` the number of monotone lattice paths that start
there and stay inside the *full* board is  

```
full[x][y] = C( (W-x)+(H-y)+2 , (W-x)+1 ) – 1 .
```

**Proof.**  
A path is completely described by the numbers of right moves `dx` and up
moves `dy`.  The number of different orders of these moves is the
binomial coefficient `C(dx+dy , dx)`.  Summation over all admissible
`dx , dy` gives a double sum that is known to equal the right hand side
(standard Vandermonde identity, e.g. derived from the generating
function of binomial coefficients). ∎



##### Lemma 2  
`TOTAL`, defined in (8), equals  

```
Σ_{all board points} full[x][y] .
```

**Proof.**  
Replace `dx = W-x , dy = H-y`.  Then `full[x][y] = C(dx+dy+2 , dx+1) – 1`.  
Summation over all `dx , dy` gives the double sum of the binomial,
which is (7).  Subtracting `(W+1)(H+1)` (the contribution of the `–1`
for every point) yields (8). ∎



##### Lemma 3  
For a fixed column `x = i` (`L ≤ i ≤ R`)  

```
Σ_{j=D}^{U} full[i][j] = 
      ( C(dx+b+3 , dx+2) – C(dx+a+2 , dx+2) ) – (U-D+1)
```

where `dx = W-i , a = H-U , b = H-D`.

**Proof.**  
`full[i][j] = C(dx+(H-j)+2 , dx+1) – 1`.  
Put `t = H-j`; then `t` runs from `a = H-U` to `b = H-D`.  
The sum of the binomial part is (11) (derived from the partial sum
formula (10)).  Subtracting `1` for each of the `U-D+1` rows gives the
claimed expression. ∎



##### Lemma 4  
`Sleft` (13) equals the total number of admissible paths whose **first**
blocked point lies on the left side of the rectangle (`x = L`).

**Proof.**  
A path that first enters at `(L , j)` (`D ≤ j ≤ U`) must reach the
neighbour `(L-1 , j)` without ever touching the rectangle, then step
right.  
All points left of the rectangle are independent of the rectangle,
hence the number of ways to reach `(L-1 , j)` is exactly the value
`leftCnt(j)` from (12) – the number of monotone paths in a full board
of width `L`.  
After the entry step the continuation is unrestricted, i.e. any
monotone path counted by `full[L][j]`.  
Multiplying and summing over all possible `j` gives (13). ∎



##### Lemma 5  
`Sbottom` (15) equals the total number of admissible paths whose first
blocked point lies on the bottom side of the rectangle (`y = D`).

**Proof.**  
Completely symmetric to Lemma&nbsp;4, using the neighbour
`(i , D-1)` and the value `bottomCnt(i)` from (14). ∎



##### Lemma 6  
Every admissible path that ever visits the rectangle is counted **once**
in `Sleft + Sbottom`.

**Proof.**  
The first blocked point of such a path cannot be inside the rectangle,
because the previous step must come from outside.  
Consequently the first blocked point has either `x = L` (entered from the
left) or `y = D` (entered from the bottom).  
The two cases are disjoint, therefore the path is counted either in
`Sleft` (Lemma&nbsp;4) or in `Sbottom` (Lemma&nbsp;5) and never in both. ∎



##### Lemma 7  
`TOTAL – Σ_{forbidden} full – (Sleft+Sbottom)` equals  

```
Σ_{all blocks} dp[x][y] .
```

**Proof.**  
`TOTAL` is the sum of `full` over *all* board points (Lemma&nbsp;2).  
Subtracting the contribution of the forbidden points removes the terms
that must not be present in the answer.  
Every remaining path either never visits the rectangle – then it is
already counted in the remaining sum – or visits it, and by Lemma&nbsp;6
its first visit is accounted for exactly once in `Sleft+Sbottom`.
Thus after subtracting `Sleft+Sbottom` we obtain exactly the sum of
`dp` over all blocks. ∎



##### Lemma 8  
The algorithm computes `TOTAL`, the sum over the forbidden rectangle,
`Sleft` and `Sbottom` exactly as described in Lemmas&nbsp;2–5.

**Proof.**  
All four quantities are evaluated using the closed formulas derived in
those lemmas, each in `O(number of terms)` time, where the number of
terms never exceeds `10^6`.  The binomial coefficients are obtained
from pre‑computed factorials, therefore the computed values are
identical to the mathematical definitions. ∎



##### Theorem  
The number printed by the program equals the number of possible
paths Snuke could have taken (mod 998 244 353).

**Proof.**  
By Lemma&nbsp;8 the program obtains the exact values of the four
quantities appearing in Lemma&nbsp;7.
Lemma&nbsp;7 shows that the combination performed by the program is
exactly the sum of `dp[x][y]` over all blocks.
By (3) this sum is precisely the required answer. ∎



--------------------------------------------------------------------

#### 8.   Complexity Analysis

```
pre‑computation of factorials :  O(W+H)      ( ≤ 2·10^6 )
loop over i = L … R          :  O(R-L+1)    ( ≤ 10^6 )
loop over j = D … U          :  O(U-D+1)    ( ≤ 10^6 )
remaining work                :  O(1)
memory                       :  O(W+H)      (factorial arrays)
```

Both time and memory easily satisfy the limits.

--------------------------------------------------------------------

#### 9.   Reference Implementation  (Python 3)

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

    # ---------- helper functions ----------
    def full(x: int, y: int) -> int:
        """full[x][y] = number of monotone paths from (x,y) in the full board."""
        dx = W - x
        dy = H - y
        return (C(dx + dy + 2, dx + 1) - 1) % MOD

    # ---------- TOTAL : sum of full over the whole board ----------
    total = (C(W + H + 4, W + 2) - (W + H + 4) - (W + 1) * (H + 1)) % MOD

    # ---------- sum of full over the forbidden rectangle ----------
    blocked = 0
    rows = U - D + 1
    a = H - U          # smallest t = H - j
    b = H - D          # largest  t = H - j
    for i in range(L, R + 1):
        dx = W - i
        # sum_{j=D}^{U} C(dx + (H-j) + 2 , dx + 1)  =  C(dx+b+3,dx+2) - C(dx+a+2,dx+2)
        sumC = (C(dx + b + 3, dx + 2) - C(dx + a + 2, dx + 2)) % MOD
        blocked = (blocked + sumC - rows) % MOD

    # ---------- paths that first enter the rectangle ----------
    # left side (x = L)
    Sleft = 0
    if L > 0:                 # otherwise no neighbour to the left
        for j in range(D, U + 1):
            # number of ways to reach (L-1 , j) without ever touching the rectangle
            leftCnt = (C(L + j + 1, L) - 1) % MOD
            # continuation after entering at (L , j)
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