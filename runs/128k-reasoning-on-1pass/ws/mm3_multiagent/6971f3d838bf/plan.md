**Solution Explanation**

For the given array `nums` we may (once) choose a value `x` and delete **all**
occurrences of `x`.  
The remaining elements keep their original order, therefore after the
deletion the array is exactly the original array with the elements equal to
`x` removed.

For a fixed `x`

*the remaining array* = the original array where every `x` is replaced by
`0` (the deleted elements do not belong to the subarray any more).

So for a fixed `x`

```
f(x) = maximum sub‑array sum of   b[i] = 0   if nums[i] == x
                                   = nums[i] otherwise
```

`f(x)` is the best sub‑array sum that can be obtained when we delete `x`.
The answer of the problem is

```
max(  original maximum sub‑array sum ,   max over all existing x of f(x) )
```

The original maximum is obtained by the usual Kadane algorithm.
The difficulty is to compute `f(x)` for *all* values `x` that appear in the
array (`≤ n` different values) fast enough.



--------------------------------------------------------------------

#### 1.   Decomposition into blocks

For a concrete value `x` let  

```
pos[0] , pos[1] , … , pos[k-1]          (sorted)
```

be the positions of `x` in the array.  
The array is split into `k+1` **blocks** – maximal contiguous parts that
contain **no** `x`.

```
block 0 : [0          , pos[0]-1]
block 1 : [pos[0]+1   , pos[1]-1]
…
block k : [pos[k-1]+1 , n-1]
```

A sub‑array of the compressed array (i.e. after deleting `x`) can start in
any block `i`, end in any later block `j` and inside each block it can use
any *prefix* of the first block, the *whole* interior blocks and any
*suffix* of the last block.

For a block we need four numbers

* `total`   – sum of the whole block
* `pref`    – maximum sum of a **prefix** of the block
* `suff`    – maximum sum of a **suffix** of the block
* `best`    – maximum sub‑array sum **inside** the block

If we know those four numbers for every block of a value `x`,
the best possible sum that uses several blocks is

```
suff[i]  +  (total of all whole blocks i+1 … j-1)  +  pref[j]      (i < j)
```

and a sub‑array that lies completely inside a single block contributes
`best` of that block.

For a fixed `x` let its blocks be `B0 … Bm-1` (`m` blocks).  
Define

```
T[t] = total of block t
P[t] = pref  of block t
S[t] = suff  of block t
B[t] = best  of block t
```

Let `prefSum[t] = T[0] + … + T[t-1]`  (`prefSum[0] = 0`).

For `i < j`

```
suff[i] + (prefSum[j] - prefSum[i+1]) + pref[j]
= (suff[i] - prefSum[i+1]) + prefSum[j] + pref[j]
```

The first term depends only on `i`, the second only on `j`.  
Scanning the blocks from left to right we keep

```
bestA = max_{i < current j} (suff[i] - prefSum[i+1])
```

and for each `j` we can test the candidate

```
bestA + prefSum[j] + pref[j]
```

All candidates are examined in `O(m)` time.

The value `f(x)` for this `x` is the maximum of

* `B[t]` for all blocks (sub‑array completely inside one block)
* the cross‑block candidates described above.

The whole procedure for one `x` needs `O(number of its blocks)`.



--------------------------------------------------------------------

#### 2.   Obtaining the four numbers of a block

All block data are obtained by queries on the original array.
A segment tree stores for every interval `[l,r]`

* `sum`   – total sum
* `pref`  – maximum prefix sum
* `suff`  – maximum suffix sum
* `best`  – maximum sub‑array sum

Both building the tree and answering a query are `O(log n)`.
The tree is built once in `O(n)`.



--------------------------------------------------------------------

#### 3.   Whole algorithm

```
build segment tree on nums
orig = root.best                                 # original answer

group all positions of each distinct value x   (dictionary value → list)

answer = orig
for each value x and its sorted position list:
        build the list of its blocks:
                for every gap between two consecutive x positions
                query the segment tree for that interval → (total,pref,suff,best)
        if there is no block (x occurs everywhere) -> continue
        run the linear DP described in section 1
        answer = max(answer, f(x))

return answer
```

*Number of blocks over all values*  

For a value that occurs `c` times we have `c+1` blocks.
Summed over all values  

```
Σ (occurrences[x] + 1) = n + (number of distinct values) ≤ 2·n
```

Hence the total number of segment‑tree queries is `O(n)` and the total
time of the linear scans is also `O(n)`.  
Overall complexity  

```
time   :  O( n log n )
memory :  O( n )
```

`n ≤ 10^5` easily fits into the limits.



--------------------------------------------------------------------

#### 4.   Correctness Proof  

We prove that the algorithm returns the required maximum sub‑array sum.

---

##### Lemma 1  
For a fixed value `x` the maximum sub‑array sum of the array after
deleting all occurrences of `x` equals the maximum sub‑array sum of the
array `B` where `B[i] = 0` if `nums[i] = x` and `B[i] = nums[i]` otherwise.

**Proof.**  
After deletion the remaining elements are exactly the non‑`x` elements,
in the same order.  
A sub‑array of the remaining array is a contiguous block of those
elements, i.e. a sub‑array of the original array that does not contain `x`.
The sum of such a sub‑array is the sum of all numbers it contains,
which is exactly the sum of the same positions in `B` (all `x` contribute
`0`). ∎



##### Lemma 2  
For a fixed `x` let its blocks be `B0 … Bm-1` (maximal intervals without `x`).
For each block define  

* `T[t]` – sum of the whole block,
* `P[t]` – maximum prefix sum,
* `S[t]` – maximum suffix sum,
* `B[t]` – maximum sub‑array sum inside the block.

Then the maximum sub‑array sum after deleting `x` equals  

```
max (  max_t B[t] ,
       max_{i<j} ( S[i] + (T[i+1]+…+T[j-1]) + P[j] ) )
```

**Proof.**  
Any sub‑array of the compressed array (i.e. after deleting `x`) must be of
one of the two forms.

*It lies completely inside a single block.*  
Its sum is bounded by `B[t]` of that block, and the best possible such
sum is `max_t B[t]`.

*It uses at least two blocks.*  
Let it start somewhere in block `i` and end somewhere in block `j` (`i<j`).
All elements of the first block before the start contribute `0`,
the part after the start is a suffix of block `i` – its maximal possible
contribution is `S[i]`.  
All whole blocks `i+1 … j-1` are taken completely – contribution
`T[i+1]+…+T[j-1]`.  
The part of block `j` after the start of the sub‑array is a prefix of
block `j` – maximal contribution `P[j]`.  
Thus any such sub‑array has sum at most `S[i] + (interior total) + P[j]`,
and this bound is attainable (choose the appropriate suffix/prefix).
The best among all `i<j` is exactly the second term of the formula. ∎



##### Lemma 3  
For a fixed `x` the algorithm computes the value described in Lemma&nbsp;2
in `O(number of blocks of x)` time.

**Proof.**  
The algorithm stores for each block the four numbers
`T, P, S, B` (obtained by a segment‑tree query, each `O(log n)`).
It first records `bestInside = max_t B[t]`.

Let `prefSum[t] = Σ_{0..t-1} T` (`prefSum[0]=0`).  
For `i<j`

```
S[i] + (prefSum[j] - prefSum[i+1]) + P[j]
= (S[i] - prefSum[i+1]) + prefSum[j] + P[j]
```

While scanning the blocks from left to right it keeps

```
bestA = max_{i < current j} (S[i] - prefSum[i+1])
```

and for the current `j` evaluates the candidate  
`bestA + prefSum[j] + P[j]`.  
All `i<j` are examined, the maximum of all candidates together with
`bestInside` is exactly the expression of Lemma&nbsp;2.
The scan is linear in the number of blocks, therefore `O(m)`. ∎



##### Lemma 4  
For every value `x` that can be deleted (i.e. the array after deletion is
non‑empty) the algorithm computes `f(x)`, the maximum sub‑array sum after
deleting `x`.

**Proof.**  
If `x` appears at all positions, the algorithm detects the empty block
list and skips this `x` – deletion would leave an empty array, which is
forbidden.

Otherwise the list of blocks is non‑empty.
By Lemma&nbsp;1 the desired value is the maximum sub‑array sum of the
array where `x` is replaced by `0`.  
By Lemma&nbsp;2 this maximum is exactly the expression examined in
Lemma&nbsp;3.  
Lemma&nbsp;3 shows that the algorithm evaluates precisely this expression,
hence returns `f(x)`. ∎



##### Lemma 5  
Let `ans` be the value returned by the algorithm.
`ans` is not smaller than the answer of the problem.

**Proof.**  
The answer of the problem is the maximum of

* the original maximum sub‑array sum (no operation),
* `f(x)` for every deletable value `x`.

`ans` is initialised with the original maximum.
For each value `x` the algorithm (Lemma&nbsp;4) computes `f(x)` and
updates `ans = max(ans, f(x))`.  
Consequently after processing all values `ans` is at least the maximum
over the whole set described above, i.e. at least the required answer. ∎



##### Lemma 6  
`ans` is not larger than the answer of the problem.

**Proof.**  
`ans` is only ever assigned one of the two kinds of numbers:

* the original maximum sub‑array sum – this is a legal result (do nothing);
* a value `f(x)` for some deletable `x` – by definition this is the best
  sub‑array sum that can be obtained after deleting that particular `x`.

Both are attainable results, therefore `ans` cannot exceed the optimal
value. ∎



##### Theorem  
The algorithm returns exactly the maximum possible sub‑array sum after
performing at most one deletion of a single value.

**Proof.**  
From Lemma&nbsp;5 the returned value `ans` is **≥** the optimum,
from Lemma&nbsp;6 it is **≤** the optimum.  Hence it equals the optimum. ∎



--------------------------------------------------------------------

#### 5.   Complexity Analysis  

*Segment tree* – `O(n)` memory, `O(n)` build time.  

*For each distinct value* – number of its blocks ≤ `occurrences[x] + 1`.  
Summed over all values the total number of blocks is `≤ 2·n`.

```
building tree                : O(n)
queries for all blocks       : O(n log n)
linear scans over blocks     : O(n)
-------------------------------------------------------------
total time                   : O(n log n)   ( ≤ 2·10^6 operations for n=10^5 )
additional memory            : O(n) for positions + O(n) for the tree
```

Both bounds satisfy the required limits.



--------------------------------------------------------------------

#### 6.   Reference Implementation  (Python 3)

```python
import sys
from typing import List
from collections import defaultdict

# ------------------------------------------------------------
# segment tree that can answer max sub‑array sum for any interval
# ------------------------------------------------------------
class SegTree:
    def __init__(self, arr: List[int]):
        self.n = len(arr)
        size = 1
        while size < self.n:
            size <<= 1
        self.size = size
        # four parallel arrays: sum, pref, suff, best
        self.sum = [0] * (2 * size)
        self.pref = [0] * (2 * size)
        self.suff = [0] * (2 * size)
        self.best = [0] * (2 * size)

        # leaves
        for i, v in enumerate(arr):
            p = size + i
            self.sum[p] = self.pref[p] = self.suff[p] = self.best[p] = v

        # internal nodes
        for p in range(size - 1, 0, -1):
            self._pull(p)

    def _pull(self, p: int):
        l = p << 1
        r = l | 1
        s = self.sum[l] + self.sum[r]
        self.sum[p] = s
        self.pref[p] = max(self.pref[l], self.sum[l] + self.pref[r])
        self.suff[p] = max(self.suff[r], self.sum[r] + self.suff[l])
        self.best[p] = max(self.best[l], self.best[r],
                           self.suff[l] + self.pref[r])

    # inclusive query [l, r]
    def query(self, l: int, r: int):
        l += self.size
        r += self.size
        left_res = None
        right_res = None
        while l <= r:
            if l & 1:
                node = (self.sum[l], self.pref[l],
                        self.suff[l], self.best[l])
                left_res = node if left_res is None else self._combine(left_res, node)
                l += 1
            if not (r & 1):
                node = (self.sum[r], self.pref[r],
                        self.suff[r], self.best[r])
                right_res = node if right_res is None else self._combine(node, right_res)
                r -= 1
            l //= 2
            r //= 2
        if left_res is None:
            return right_res
        if right_res is None:
            return left_res
        return self._combine(left_res, right_res)

    @staticmethod
    def _combine(a, b):
        # a,b are tuples (sum,pref,suff,best)
        s = a[0] + b[0]
        pref = max(a[1], a[0] + b[1])
        suff = max(b[2], b[0] + a[2])
        best = max(a[3], b[3], a[2] + b[1])
        return (s, pref, suff, best)


# ------------------------------------------------------------
# main solution class
# ------------------------------------------------------------
class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        seg = SegTree(nums)

        # original answer (do nothing)
        ans = seg.query(0, n - 1)[3]      # best field

        # collect positions of each value
        pos = defaultdict(list)
        for i, v in enumerate(nums):
            pos[v].append(i)

        NEG_INF = -10**30   # safe for all possible sums

        for x, positions in pos.items():
            blocks = []                     # each block = (total, pref, suff, best)
            prev = 0
            for p in positions:
                if p > prev:                # non‑empty interval
                    node = seg.query(prev, p - 1)
                    blocks.append(node)    # (total,pref,suff,best)
                prev = p + 1
            if prev < n:
                node = seg.query(prev, n - 1)
                blocks.append(node)

            if not blocks:                  # deleting x would empty the array
                continue

            m = len(blocks)
            total = [b[0] for b in blocks]
            pref  = [b[1] for b in blocks]
            suff  = [b[2] for b in blocks]
            best  = [b[3] for b in blocks]

            # best sub‑array completely inside a single block
            best_overall = max(best)

            # prefix sums of total values
            pref_sum = [0] * (m + 1)
            for i in range(m):
                pref_sum[i + 1] = pref_sum[i] + total[i]

            # linear DP for sub‑arrays that span several blocks
            best_A = NEG_INF
            for j in range(m):
                if j > 0:
                    cand = best_A + pref_sum[j] + pref[j]
                    if cand > best_overall:
                        best_overall = cand
                # update best_A for the next j (i = j)
                val = suff[j] - pref_sum[j + 1]
                if val > best_A:
                    best_A = val

            if best_overall > ans:
                ans = best_overall

        return ans
```

The program follows exactly the algorithm proven correct above
and conforms to the required `O(n log n)` time and `O(n)` memory limits.