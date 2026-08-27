**Solution Explanation**

For each position `i`

* `A[i] = -1` – we may put any non‑negative integer there  
* `B[i] = -1` – we may put any non‑negative integer there  
* otherwise the value is fixed

We may also permute the whole array `A`.  
We have to make all sums `A[i] + B[i]` equal to the same non‑negative integer `C`.

--------------------------------------------------------------------

#### 1.   Observations

* If a position has `A[i] ≠ -1` then at that place `C = A[i] + B[i] ≥ A[i]`.  
  Hence for every **fixed** `A[i]` we must have `C ≥ A[i]`.  
  The same holds for every fixed `B[i]`.

* If a position has both `A[i]` and `B[i]` fixed, the sum is already fixed:
  `A[i] + B[i] = C`.  
  Therefore **all** such positions must have the same sum, and that sum is the
  only possible value of `C`.

* If there is **no** position with both numbers fixed, we are free to choose any
  `C` (as large as we want) and we can always set the missing numbers.
  Moreover the number of positions with `B = -1` is exactly `N – (#fixed B)`,
  which is at least the number of fixed `A`.  
  So a solution always exists.

* Consequently the only interesting case is when at least one position has
  both numbers fixed.  
  Let  

```
C0 = A[i] + B[i]  (the first such position)
```

  All both‑fixed positions must have sum `C0`.  
  The whole problem is now:  

  *Can we achieve the same `C0` for all positions?*

--------------------------------------------------------------------

#### 2.   What is still free?

* Fixed `A` values have to be placed somewhere.
* Fixed `B` values already stay at their original places.
* For a fixed `B = b` we may put any `A = C0 – b` there
  (the `-1` of `A` is used).  
  If we want to use a **fixed** `A = a` at that place we must have
  `a + b = C0`.

Thus we may create *pairs* `(a , b)` with `a` from the set of fixed `A`,
`b` from the set of fixed `B` and `a + b = C0`.  
Each such pair uses one fixed `A` and one fixed `B`.

--------------------------------------------------------------------

#### 3.   How many pairs are necessary?

* `cntBoth` – number of positions with both numbers fixed  
  (they already contain a fixed `B`; we may keep the original `A` or replace it)

* `cntNone` – number of positions with both numbers `-1`

* `cntAonly` – `A` fixed, `B = -1`  
* `cntBonly` – `B` fixed, `A = -1`

All fixed `A` must be placed somewhere.

* If we create `k` pairs `(a , b)` with `a + b = C0`, the remaining
  `(#fixed A) – k` fixed `A` have to be placed at positions with `B = -1`.
  The number of such positions is `cntAonly + cntNone`.

Therefore we need

```
(#fixed A) – k  ≤  cntAonly + cntNone
⇔ k ≥ #fixed A – (cntAonly + cntNone)
```

`#fixed A = cntBoth + cntAonly` and `cntAonly + cntNone = N – cntFB`
so the right hand side simplifies to

```
k ≥ cntBoth – cntNone .
```

Define  

```
need = max( 0 , cntBoth – cntNone ) .
```

We must be able to create at least `need` disjoint pairs with sum `C0`.

--------------------------------------------------------------------

#### 4.   Maximum number of pairs for a fixed sum `C0`

Let  

```
cntA[x] = how many fixed A equal x
cntB[y] = how many fixed B equal y
```

For a fixed `C0` a pair `(a , b)` is possible iff `b = C0 – a`.
The number of possible pairs using value `a` is `min(cntA[a] , cntB[C0–a])`.
Summing over all possible `a` gives the maximum number of disjoint pairs:

```
pairs(C0) = Σa  min( cntA[a] , cntB[C0 – a] ) .
```

If `pairs(C0) ≥ need` we can realise the required number of pairs,
the remaining fixed `A` fit into the free `B = -1` positions,
and all sums are `C0`.  
If `pairs(C0) < need` the task is impossible.

--------------------------------------------------------------------

#### 5.   Final decision rules

*If there is no position with both numbers fixed* → answer **Yes**  
*(we can always choose a large enough `C` and fill the missing numbers).*

*Otherwise* (`cntBoth > 0`)

1. Check that **all** both‑fixed positions have the same sum `C0`.  
   If not → **No**.

2. Let `maxA = max fixed A` (or `0` if none), `maxB = max fixed B`.  
   If `C0 < maxA` or `C0 < maxB` → **No** (a fixed value would need a negative partner).

3. `need = max(0 , cntBoth – cntNone)`.  
   If `need = 0` → **Yes** (enough free positions for the remaining fixed `A`).

4. Build the frequency tables `cntA` and `cntB`.  
   Compute `pairs(C0)` as described above.  
   If `pairs(C0) ≥ need` → **Yes**, else **No**.

All operations are linear in `N` (building the tables and a single pass over
the distinct values of `A`).  
`N ≤ 2000`, so this easily fits the limits.

--------------------------------------------------------------------

#### 6.   Correctness Proof  

We prove that the algorithm prints “Yes” exactly for the instances for which
the required operations are possible.

---

##### Lemma 1  
If a position has a fixed `A = a` then in any feasible final configuration
`C ≥ a`.  
If a position has a fixed `B = b` then in any feasible final configuration
`C ≥ b`.

**Proof.**  
`C = a + B` and `B` is a non‑negative integer, therefore `C ≥ a`.  
The same argument for `B`. ∎



##### Lemma 2  
If there exists a position with both numbers fixed and its sum is `s`,
then every feasible configuration must have `C = s`.

**Proof.**  
At that position `A` and `B` are already fixed, hence their sum is `s`.
All sums must be equal, so `C = s`. ∎



##### Lemma 3  
If no position has both numbers fixed then a solution always exists.

**Proof.**  
Let `C = max( max fixed A , max fixed B , 0 )`.  
For every fixed `A = a` put it at a position where `B = -1` (there are at least
as many such positions as fixed `A`, see the counting in the analysis) and set
`B = C – a`.  
For every fixed `B = b` put it at a position where `A = -1` and set
`A = C – b`.  
All `-1` entries are now non‑negative and every sum equals `C`. ∎



##### Lemma 4  
Assume there is at least one both‑fixed position and let `C0` be their common
sum.  
Let  

```
need = max(0 , cntBoth – cntNone) .
```

In any feasible final configuration at least `need` disjoint pairs
`(a , b)` with `a + b = C0` must be created (i.e. a fixed `A` is placed at a
fixed `B` position).

**Proof.**  
We have `cntBoth` fixed `B` values coming from both‑fixed positions.
`cntNone` positions have both numbers `-1`; they can be used to set an
arbitrary `A` for a fixed `B` without consuming a fixed `A`.  
Consequently at most `cntNone` fixed `B` can be paired with a free `A`.  
All remaining fixed `B` (there are `cntBoth – cntNone` of them) need a
fixed `A` to achieve sum `C0`, i.e. they must belong to a pair `(a , b)`.  
If `cntBoth ≤ cntNone` no such pair is necessary, otherwise at least
`cntBoth – cntNone` pairs are required. ∎



##### Lemma 5  
For a fixed `C0` the maximum number of disjoint pairs `(a , b)` with
`a + b = C0` is  

```
pairs(C0) = Σa  min( cntA[a] , cntB[C0 – a] ) .
```

**Proof.**  
For a concrete value `a` the only possible partner is `b = C0 – a`.
At most `cntB[C0 – a]` different `B`‑positions are available, and at most
`cntA[a]` different `A`‑values are available, therefore at most
`min(cntA[a] , cntB[C0 – a])` pairs can use this `a`.  
Pairs using different `a` are independent, so the total maximum is the sum
over all `a`. ∎



##### Lemma 6  
If `pairs(C0) ≥ need` then a feasible configuration with sum `C0` exists.

**Proof.**  
Take any collection of `need` disjoint pairs achieving the value `pairs(C0)`.
Place the `A` of each pair at the position of its `B`.  
All remaining fixed `A` (there are `cntFA – need` of them) are placed at
positions with `B = -1`; their number is at most the number of such positions
because  

```
cntFA – need = (cntBoth + cntAonly) – (cntBoth – cntNone) = cntAonly + cntNone .
```

For every such `A = a` we set `B = C0 – a` (non‑negative because `C0 ≥ a`).
All other positions (the `cntNone` both‑`-1` ones) are filled arbitrarily,
e.g. `A = 0 , B = C0`.  
All sums are now `C0`. ∎



##### Lemma 7  
If `pairs(C0) < need` then no feasible configuration exists.

**Proof.**  
By Lemma&nbsp;4 any feasible configuration must contain at least `need` disjoint
pairs `(a , b)` with `a + b = C0`.  
The total number of such pairs that can ever be formed is bounded by the
maximum possible, which is `pairs(C0)` (Lemma&nbsp;5).  
If `pairs(C0) < need`, the required number of pairs cannot be created,
hence the configuration is impossible. ∎



##### Lemma 8  
The algorithm outputs “Yes” exactly when a feasible configuration exists.

**Proof.**  

*If the algorithm prints “Yes”*  

*   No both‑fixed positions: by Lemma&nbsp;3 a solution exists.  

*   Both‑fixed positions exist:  
    *All* their sums are equal (`C0`) – otherwise the algorithm would have
    rejected.  
    `C0` is at least every fixed `A` and every fixed `B` – otherwise rejected.  
    If `need = 0` the algorithm accepts; by Lemma&nbsp;3 (with the
    “enough free positions” condition proved in the analysis) a solution
    exists.  
    If `need > 0` the algorithm checks `pairs(C0) ≥ need`.  
    By Lemma&nbsp;6 a solution exists.

*If the algorithm prints “No”*  

*   Either the both‑fixed sums are inconsistent – by Lemma&nbsp;2 impossible.  
*   Or `C0` is smaller than a fixed `A` or `B` – contradicts Lemma&nbsp;1.  
*   Or `pairs(C0) < need` – by Lemma&nbsp;7 impossible.

Thus in every case the algorithm’s answer coincides with the true
possibility. ∎



##### Theorem  
The program described in the “Solution” section prints “Yes” if and only if
the given sequences can be transformed (by filling `-1` entries with arbitrary
non‑negative integers and permuting `A`) so that all sums `A[i] + B[i]` become
equal.

**Proof.**  
Directly from Lemma&nbsp;8. ∎



--------------------------------------------------------------------

#### 7.   Complexity Analysis

*Reading & classification* – `O(N)`  
*Finding the common sum `C0`* – `O(N)`  
*Computing `maxA` and `maxB`* – `O(N)`  
*Building the frequency tables* – `O(N)`  
*Computing `pairs(C0)`* – one pass over the distinct values of `A`
(at most `N`) → `O(N)`

Memory consumption: the two frequency tables store at most `N` integers each,
`O(N)`.

With `N ≤ 2000` this easily satisfies the limits.

--------------------------------------------------------------------

#### 8.   Reference Implementation  (Python 3)

```python
import sys
from collections import Counter

def solve() -> None:
    it = iter(sys.stdin.read().split())
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    B = [int(next(it)) for _ in range(N)]

    fa = []          # fixed A values
    fb = []          # fixed B values
    cntBoth = 0
    cntNone = 0

    C0 = None        # common sum if any both‑fixed position exists
    for a, b in zip(A, B):
        if a != -1 and b != -1:
            cntBoth += 1
            fa.append(a)
            fb.append(b)
            s = a + b
            if C0 is None:
                C0 = s
            elif C0 != s:
                print("No")
                return
        elif a != -1 and b == -1:
            fa.append(a)
        elif a == -1 and b != -1:
            fb.append(b)
        else:               # both -1
            cntNone += 1

    # No position with both numbers fixed -> always possible
    if cntBoth == 0:
        print("Yes")
        return

    # Now C0 is defined
    maxA = max(fa) if fa else 0
    maxB = max(fb) if fb else 0
    if C0 < maxA or C0 < maxB:
        print("No")
        return

    need = cntBoth - cntNone
    if need < 0:
        need = 0
    if need == 0:
        print("Yes")
        return

    cntA = Counter(fa)
    cntB = Counter(fb)

    pairs = 0
    for v, ca in cntA.items():
        w = C0 - v
        if w in cntB:
            pairs += min(ca, cntB[w])
            if pairs >= need:
                print("Yes")
                return

    print("No")

if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required input and output format.