
## ideation
**Solution Explanation**

For a subsequence of length 5 the middle element is the element that
occupies the third position in the original order.
Fix this middle position `i` (`0 ≤ i < n`) and let `v = nums[i]`.
We have to count how many ways we can choose two indices left of `i`
and two indices right of `i` such that the value `v` is the **unique**
most frequent value in the five chosen elements.

--------------------------------------------------------------------

#### 1.   Notation for a fixed `i`

```
L[w]  – occurrences of value w in positions < i
R[w]  – occurrences of value w in positions > i
Lv = L[v] ,  Rv = R[v]
Lnv = i            - Lv          (non‑v on the left)
Rnv = (n-1-i)      - Rv          (non‑v on the right)
```

Only the number of extra `v`’s matters:

```
extra v's on left  = l   (0 … 2)
extra v's on right = r   (0 … 2)
total v’s in the subsequence c = 1 + l + r   (c = 2 … 5)
```

The six possible `(l,r)` are enumerated in the table below.
All other values may appear at most `c‑1` times.
For `c = 5,4,3` the condition is always satisfied,
for `c = 2` the three non‑`v` elements must be pairwise different.

| c | (l,r) | condition on the other three picks | formula |
|---|-------|------------------------------------|---------|
| 5 | (2,2) | –                                  | `C(Lv,2)·C(Rv,2)` |
| 4 | (1,2) | one non‑v on the left               | `Lv·C(Rv,2)·Lnv` |
| 4 | (2,1) | one non‑v on the right              | `C(Lv,2)·Rv·Rnv` |
| 3 | (0,2) | two non‑v on the left               | `C(Lnv,2)·C(Rv,2)` |
| 3 | (1,1) | one non‑v on each side              | `Lv·Lnv·Rv·Rnv` |
| 3 | (2,0) | two non‑v on the right              | `C(Lv,2)·C(Rnv,2)` |
| 2 | (0,1) | left non‑v pair, right v + right non‑v, all three non‑v different | `Rv·(Rnv·A – B)` |
| 2 | (1,0) | left v + left non‑v, right non‑v pair, all three non‑v different | `Lv·(Lnv·Ap – Bp)` |

`A , Ap` count unordered pairs of non‑`v` positions with **different**
values:

```
A  = number of unordered left‑non‑v pairs with distinct values
   = (Lnv² – Σ L[w]²) / 2      (sum over w ≠ v)

Ap = (Rnv² – Σ R[w]²) / 2
```

`B , Bp` count the “bad’’ triples where a left (right) non‑`v`
coincides with the right (left) non‑`v`:

```
B  = Σ_{w≠v} L[w]·R[w]·(Lnv – L[w])
Bp = Σ_{w≠v} L[w]·R[w]·(Rnv – R[w])
```

All sums are taken over values different from `v`.

--------------------------------------------------------------------

#### 2.   Computing the needed sums

`n ≤ 1000`, therefore `O(n²)` operations are easily fast enough.
We keep two hash maps while scanning the array:

* `left_counts` – frequencies of values left of the current `i`
* `right_counts` – frequencies of values right of the current `i`

Initially `right_counts` contains all elements.
Before processing index `i` we remove `nums[i]` from `right_counts`;
after the processing we insert it into `left_counts`.

For the current `i` we can obtain all required quantities in
`O(K)` where `K` is the number of distinct values in the left or right
part (at most `n`).

```
Lv = left_counts[v]                (0 if absent)
Rv = right_counts[v]               (0 if absent)
Lnv = i            - Lv
Rnv = (n-1-i)      - Rv

sumL2 = Σ cnt²  over left_counts
sumR2 = Σ cnt²  over right_counts
Σ L[w]·R[w]  (w≠v) is not needed directly,
          it appears only inside B and Bp.
```

The needed auxiliary values are

```
A  = (Lnv*Lnv - (sumL2 - Lv*Lv)) // 2
Ap = (Rnv*Rnv - (sumR2 - Rv*Rv)) // 2

B  = Σ_{w≠v} Lcnt[w] * Rcnt[w] * (Lnv - Lcnt[w])
Bp = Σ_{w≠v} Lcnt[w] * Rcnt[w] * (Rnv - Rcnt[w])
```

All loops iterate over the at most `n` keys of `left_counts`.

--------------------------------------------------------------------

#### 3.   Adding the contributions

For each `i` we evaluate the eight formulas from the table,
add them together and update the answer modulo `10⁹+7`.
Every subsequence of length 5 has exactly one middle index,
therefore the sum over all `i` equals the required result.

The whole algorithm works in `O(n·K) = O(n²) ≤ 10⁶` elementary
operations and needs `O(n)` extra memory.

--------------------------------------------------------------------

#### 4.   Correctness Proof  

We prove that the algorithm returns exactly the number of
subsequences of length 5 whose middle element is the unique mode.

---

##### Lemma 1  
For a fixed middle index `i` and a fixed distribution of extra `v`’s
`(l,r)` the number of ways to choose the remaining four indices is
given by the corresponding formula in the table of Section&nbsp;1.

**Proof.**  
The table enumerates all possibilities for `(l,r)` with `c≥2`.

* `c=5` – both left and right picks are `v`.  
  The left pair can be any unordered pair of the `Lv` occurrences of `v`
  on the left, the right pair any unordered pair of the `Rv` occurrences
  on the right.  Hence `C(Lv,2)·C(Rv,2)`.

* `c=4, (1,2)` – left contains one `v` and one non‑`v`,
  right contains two `v`.  
  Choose the left `v` (`Lv` ways), the left non‑`v` (`Lnv` ways)
  and the right pair of `v` (`C(Rv,2)` ways).  
  Product `Lv·C(Rv,2)·Lnv`.

* `c=4, (2,1)` – symmetric, gives `C(Lv,2)·Rv·Rnv`.

* `c=3, (0,2)` – left pair of non‑`v`, right pair of `v`.  
  `C(Lnv,2)·C(Rv,2)`.

* `c=3, (1,1)` – one `v` and one non‑`v` on each side.  
  `Lv·Lnv·Rv·Rnv`.

* `c=3, (2,0)` – symmetric, gives `C(Lv,2)·C(Rnv,2)`.

* `c=2, (0,1)` – left non‑`v` pair, right side contains one `v`
  (`Rv` possibilities) and one non‑`v`.  
  The three non‑`v` values must be pairwise different.
  The number of triples consisting of an unordered left pair with
  distinct values and a right non‑`v` whose value is different from both
  left values is `Rnv·A – B` (proved in Lemma&nbsp;2 below).  
  Multiplying by the `Rv` possibilities for the right `v` yields
  `Rv·(Rnv·A – B)`.

* `c=2, (1,0)` – symmetric, gives `Lv·(Lnv·Ap – Bp)`.

All formulas follow directly from counting independent choices,
hence the lemma holds. ∎



##### Lemma 2  
For a fixed middle index `i`

```
#{(unordered left pair, right non‑v)  :  the three values are distinct}
   = Rnv·A – B .
```

**Proof.**  
`A` is the number of unordered left pairs with two different values.
For each such pair there are `Rnv` possible right non‑`v` positions,
hence `A·Rnv` triples before the distinctness restriction.

A triple is *bad* iff the right non‑`v` value equals one of the two
left values.
Fix a value `w ≠ v`.  
A bad triple can be built by
  * choosing a left occurrence of `w` (`L[w]` ways),
  * choosing a left occurrence of a different value
    (`Lnv – L[w]` ways – the unordered pair is uniquely determined by
    the distinguished `w`),
  * choosing a right occurrence of `w` (`R[w]` ways).

This gives `L[w]·R[w]·(Lnv – L[w])` bad triples for the fixed `w`,
and summing over all `w ≠ v` yields exactly `B`.  
Every bad triple is counted once, therefore the number of good triples
is `A·Rnv – B`. ∎



##### Lemma 3  
For a fixed middle index `i` the algorithm adds to the answer exactly
the number of length‑5 subsequences whose middle element is `v`
and `v` is the unique mode of the subsequence.

**Proof.**  
All possible distributions `(l,r)` of extra `v`’s are covered in
Lemma&nbsp;1.  
For each distribution the algorithm uses the formula proved in
Lemma&nbsp;1, which counts **all** ways to pick the remaining four
indices that satisfy the required multiplicity condition.
The six cases with `c≥3` have no additional restriction,
the two cases with `c=2` use Lemma&nbsp;2 to enforce that the three
non‑`v` values are all different, which is precisely the condition
`v` must be the unique mode.
Summation over the six cases therefore counts exactly the desired
subsequences for the fixed middle `i`. ∎



##### Lemma 4  
Every length‑5 subsequence with a unique middle mode is counted exactly
once by the algorithm.

**Proof.**  
A subsequence of length 5 has a unique middle index `i` (the third
position in the original order).  
The algorithm processes this `i` and, by Lemma&nbsp;3, counts the
subsequence while processing `i`.  
For any other index `j ≠ i` the middle element of the same subsequence
is not `nums[j]`, so the subsequence is not counted when `j` is the
fixed middle position.  Hence the subsequence is counted exactly once. ∎



##### Theorem  
`subsequencesWithMiddleMode` returns the number of subsequences of
`nums` of size 5 whose middle element is the unique mode, modulo
`10⁹+7`.

**Proof.**  
By Lemma&nbsp;3, for each possible middle index `i` the algorithm adds
the exact number of valid subsequences having `i` as middle.
By Lemma&nbsp;4 these sets of subsequences are disjoint and their union
is the set of all valid subsequences.
Summing over all `i` therefore yields the total number of required
subsequences.  The algorithm performs the sum modulo `10⁹+7`,
hence the returned value is the correct answer modulo the required
prime. ∎



--------------------------------------------------------------------

#### 5.   Complexity Analysis

```
n ≤ 1000
```

*Updating the two hash maps* – `O(1)` per index.  
*Inside the loop* we iterate over all distinct values in the left side
(at most `n`) a constant number of times (four passes).

```
Time   :  O(n · distinct values)  ≤  O(n²)  ≤ 10⁶ operations
Memory :  O(n)   (the two dictionaries)
```

Both limits are easily satisfied for the given constraints.

--------------------------------------------------------------------

#### 6.   Reference Implementation  (Python 3)

```python
from typing import List
from collections import defaultdict

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10 ** 9 + 7
        n = len(nums)

        # helper for C(x,2)
        def comb2(x: int) -> int:
            return x * (x - 1) // 2 if x >= 2 else 0

        left_counts = defaultdict(int)      # values left of current i
        right_counts = defaultdict(int)     # values right of current i
        for x in nums:
            right_counts[x] += 1

        ans = 0
        for i in range(n):
            v = nums[i]

            # move current element from right side to the "processed" side
            right_counts[v] -= 1
            if right_counts[v] == 0:
                del right_counts[v]

            Lv = left_counts.get(v, 0)
            Rv = right_counts.get(v, 0)

            Lnv = i - Lv                     # non‑v on the left
            Rnv = (n - 1 - i) - Rv           # non‑v on the right

            # sums of squares (including the value v)
            sumL2 = 0
            for cnt in left_counts.values():
                sumL2 += cnt * cnt
            sumR2 = 0
            for cnt in right_counts.values():
                sumR2 += cnt * cnt

            # exclude the value v
            sumL2_excl = sumL2 - Lv * Lv
            sumR2_excl = sumR2 - Rv * Rv

            # unordered pairs of non‑v positions with different values
            A = (Lnv * Lnv - sumL2_excl) // 2
            Ap = (Rnv * Rnv - sumR2_excl) // 2

            # auxiliary sums for the c = 2 case
            B = 0
            Bp = 0
            for w, cntL in left_counts.items():
                if w == v:
                    continue
                cntR = right_counts.get(w, 0)
                if cntR == 0:
                    continue
                B += cntL * cntR * (Lnv - cntL)
                Bp += cntL * cntR * (Rnv - cntR)

            # ----- contributions for the eight (l,r) possibilities -----
            # c = 5
            c5 = comb2(Lv) * comb2(Rv)

            # c = 4
            c4 = (Lv * comb2(Rv) * Lnv) + (comb2(Lv) * Rv * Rnv)

            # c = 3
            c3 = (comb2(Lnv) * comb2(Rv)) + (comb2(Lv) * comb2(Rnv)) \
                 + (Lv * Lnv * Rv * Rnv)

            # c = 2
            term1 = Rv * (Rnv * A - B)   # (l=0, r=1)
            term2 = Lv * (Lnv * Ap - Bp) # (l=1, r=0)
            c2 = term1 + term2

            ans = (ans + c5 + c4 + c3 + c2) % MOD

            # finally add the current element to the left side for the next step
            left_counts[v] += 1

        return ans
```

The program follows exactly the algorithm proven correct above
and conforms to the required `O(n²)` time and `O(n)` memory limits.

## worker: Implement the solution in Python: write the `subse
The algorithm enumerates every possible middle index `i` of a length‑5 subsequence.  
For each `i` we keep the frequencies of values on the left (`left_counts`) and on the right (`right_counts`).  
From these we compute the number of ways to pick two left and two right elements so that the middle value `v` is the **unique** mode.  
All cases are covered by the six distributions of extra `v`’s (`c = 2,3,4,5`).  
The needed combinatorial quantities (`A`, `Ap`, `B`, `Bp`) are expressed only through the counts and sums of squares, allowing an `O(n²)` overall solution (since `n ≤ 1000`).  
The final result is taken modulo `10⁹+7`.
