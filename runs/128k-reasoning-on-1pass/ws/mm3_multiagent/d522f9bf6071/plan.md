**Solution Explanation**

For every interval `i`

```
l[i] … left end
r[i] … right end
w[i] … weight
```

we have to choose **at most four** intervals

* they must be pairwise non‑overlapping  
  (`r[a] < l[b]` – sharing a border is also forbidden)
* the sum of their weights has to be maximal
* among all optimal solutions the array of chosen indices (written in increasing
  order) has to be lexicographically smallest.



--------------------------------------------------------------------

#### 1.   Ordering the intervals  

Only the order of the right ends matters for the “non‑overlapping” condition.
Sort the intervals by `r` (tie‑break by `l`).  
After sorting

```
r[0] ≤ r[1] ≤ … ≤ r[n‑1]
```

`l[i] , r[i] , w[i] , original_index[i]` are stored in parallel arrays.

For a fixed interval `i` all intervals that can be placed **before** it are
exactly those with `r < l[i]`.  
Because `r` is sorted we can find the last such interval with a binary search

```
prev[i] = largest index j < i  with  r[j] < l[i]
         ( -1 if no such interval )
```

`prev[i]` is obtained by  

```
pos = bisect_left(ends, l[i])          # first r ≥ l[i]
prev[i] = pos-1
```

--------------------------------------------------------------------

#### 2.   DP for at most 4 intervals  

`k` – number of already taken intervals ( `0 … 4` )  

`dp[k][i]` – the best result that uses **at most `k` intervals**
among the first `i+1` intervals (intervals `0 … i`)  

The answer will be the best `dp[k][n‑1]` for `k = 0 … 4`.

For a fixed `i` we have two possibilities

* do **not** use interval `i` → keep the previous best `dp[k][i‑1]`
* use interval `i` as the last one → we need the best result with `k‑1`
  intervals among the intervals that end before `l[i]`

```
candidate_weight = best_weight_of_k-1_intervals_before_i + w[i]
candidate_list   = best_list_of_k-1_intervals_before_i  + [original_index[i]]
```

`dp[k][i]` is the better of the two possibilities:

* larger weight wins
* if the weights are equal – the lexicographically smaller (sorted) list wins

The only remaining difficulty is to obtain the
*best* result for “`k‑1` intervals before `i`” fast.

--------------------------------------------------------------------

#### 3.   Prefix maximum with a Fenwick tree (Binary Indexed Tree)

For every `k = 0 … 4` we keep a Fenwick tree `BIT[k]`.

* `BIT[k][p]` stores the best `(weight , list)` among the intervals
  with index `≤ p` (the tree works on a 1‑based array).
* **update** – after `dp[k][i]` is known we insert it into `BIT[k]` at
  position `i+1`.
* **query** – the best result of `k‑1` intervals that end before `l[i]`
  is simply the prefix query

```
bestPrev = BIT[k-1].query( prev[i] + 1 )          # +1 because BIT is 1‑based
```

If `prev[i] = -1` the query returns the neutral element `(0 , ())`,
i.e. “no previous interval”.

Both operations are `O(log n)`.

--------------------------------------------------------------------

#### 4.   Whole algorithm  

```
sort intervals by (r , l)
store arrays l , r , w , orig
compute prev[i] for every i                         (binary search)

BIT[0] … BIT[4]      # all initially (0 , ())

dpPrev[0..4] = (0 , ())          # best result up to the previous position

for i = 0 … n-1
        for k = 1 … 4
                # best result with k-1 intervals before i
                if prev[i] >= 0
                        bestPrevWeight , bestPrevList = BIT[k-1].query(prev[i]+1)
                else
                        bestPrevWeight , bestPrevList = 0 , ()

                candWeight = bestPrevWeight + w[i]
                # new list = sorted(bestPrevList ∪ {orig[i]})
                candList = tuple(sorted( bestPrevList + (orig[i],) ))

                # previous best without using i
                prevWeight , prevList = dpPrev[k]

                # choose the better one
                if candWeight > prevWeight
                        cur = (candWeight , candList)
                elif candWeight < prevWeight
                        cur = (prevWeight , prevList)
                else                # equal weight → lexicographically smaller list
                        cur = (candWeight, candList if candList < prevList else prevList)

                dpPrev[k] = cur
                BIT[k].update(i+1 , cur)          # make it available for later positions

# after the loop dpPrev[k] = dp[k][n-1] (best with at most k intervals)
answer = the best among dpPrev[0] … dpPrev[4]   (same comparison rule)
return list(answer.list)        # already sorted increasingly
```

`n ≤ 5·10⁴ , k ≤ 4` → time `O( n·k·log n )`  
`≈ 5·10⁴·4·log₂5·10⁴   <   7·10⁶` operations – easily fast enough.

Memory consumption  

* arrays of size `n` for the sorted data – `O(n)`
* five Fenwick trees, each `n+1` entries → `O(n)`
* only the previous row of the DP is kept – `O(k)`

Overall `O(n)` memory (well below the limits).

--------------------------------------------------------------------

#### 5.   Correctness Proof  

We prove that the algorithm returns exactly the lexicographically smallest
array of at most four indices whose total weight is maximal.

---

##### Lemma 1  
For any interval `i` the set of intervals that can appear **before** `i`
in a feasible solution is exactly the set of indices `j` with `j ≤ prev[i]`.

**Proof.**  
All intervals are sorted by increasing right end.
`j ≤ prev[i]` ⇔ `r[j] < l[i]` (definition of `prev[i]`).  
`r[j] < l[i]` is precisely the condition “interval `j` ends strictly before
interval `i` starts”, i.e. they do not overlap.
No other interval can be placed before `i`. ∎



##### Lemma 2  
After processing intervals `0 … i` the value stored in `BIT[k]` at any
position `p` equals the best `(weight , list)` among all
solutions that

* use **at most `k` intervals**,
* end at some interval with index `≤ p`.

**Proof.**  
Induction over `i`.

*Base (`i = -1`).*  
No interval processed, all tree entries are the neutral element
`(0 , ())`. The statement holds.

*Induction step.*  
Assume the statement true after interval `i‑1`.  
When interval `i` is processed the algorithm computes `dp[k][i]`,
the optimal result that may use interval `i` as its last element.
`dp[k][i]` is inserted into `BIT[k]` at position `i+1`.
All later positions (`> i+1`) also receive the better of the old value
and the new one because the Fenwick update propagates the new value
to all ancestors.
Therefore after the update every entry of `BIT[k]` stores the best
solution among intervals `0 … i`. ∎



##### Lemma 3  
When the algorithm processes interval `i` and a fixed `k (1 ≤ k ≤ 4)`,
the query  

```
bestPrev = BIT[k-1].query(prev[i] + 1)
```

returns the optimal `(weight , list)` of a solution that

* uses **at most `k‑1` intervals**,
* ends at an interval whose index `j` satisfies `j ≤ prev[i]`.

**Proof.**  
By Lemma&nbsp;2 `BIT[k‑1]` contains exactly those optimal results for all
indices `≤ p`.  
The query asks for the best among indices `≤ prev[i]`, i.e. among all
intervals that end before `l[i]`.  
Because of Lemma&nbsp;1 those are exactly the intervals that may appear
before interval `i` in a feasible solution. ∎



##### Lemma 4  
For every `k (0 … 4)` and every `i (0 … n‑1)` the value `dpPrev[k]`
after processing interval `i` equals the optimal result that

* uses **at most `k` intervals**,
* is restricted to intervals `0 … i`,
* has the smallest possible (sorted) index list among all optimal
  solutions with the same weight.

**Proof.**  
Induction over `i`.

*Base (`i = 0`).*  
The algorithm examines the two possibilities

* not using interval 0 → `(0, ())`
* using interval 0 → ` (w[0] , (orig[0]) )` (or the same after sorting)

and stores the better one according to the rule
“larger weight, then lexicographically smaller list”.
Thus the invariant holds.

*Induction step.*  
Assume the invariant true after interval `i‑1`.  
For interval `i` the algorithm evaluates

* `candidate` – the best solution that ends with `i` and uses at most
  `k` intervals.  
  By Lemma&nbsp;3 the prefix query yields the optimal `(k‑1)`‑solution
  before `i`; adding `i` gives the optimal `k`‑solution that ends at `i`.
  The new list is built by inserting `orig[i]` into the already sorted
  list, therefore it is the sorted list of that solution.
* `previous` – the optimal solution among intervals `0 … i‑1`
  (induction hypothesis) – possibly using fewer than `k` intervals.

The algorithm keeps the better of the two according to the same
comparison rule.  
Consequently after the update `dpPrev[k]` is the optimal solution among
intervals `0 … i` that uses at most `k` intervals and is lexicographically
minimal among all optimal ones. ∎



##### Lemma 5  
After the whole loop finishes, for every `k` the value `dpPrev[k]`
is the optimal result that uses **at most `k` intervals** among *all*
intervals.

**Proof.**  
Immediate from Lemma&nbsp;4 with `i = n‑1`. ∎



##### Lemma 6  
Let `best` be the element of  
`{ dpPrev[0] , … , dpPrev[4] }` with the largest weight;
if several have this weight, `best` has the lexicographically smallest
(sorted) index list among them.

**Proof.**  
The final selection step of the algorithm compares the five candidates
exactly with the rule “larger weight, then smaller list”. ∎



##### Lemma 7  
`best` corresponds to a feasible set of at most four non‑overlapping
intervals whose total weight is maximal among all feasible sets,
and its list of indices is the lexicographically smallest among all
optimal sets.

**Proof.**  

*Feasibility.*  
Every DP transition adds a new interval only if the previous solution
ended at an interval `j` with `r[j] < l[i]`.  
Thus all intervals in any DP‑state are pairwise non‑overlapping.
`best` is one of those states, therefore feasible.

*Optimality.*  
For any feasible set `S` of at most four intervals,
let its intervals be ordered by increasing right end.
The last interval of `S` is some `i`.  
All earlier intervals of `S` are among those with index `≤ prev[i]`,
hence their total weight is at most the weight of the best
`(k‑1)`‑solution before `i` (Lemma&nbsp;3).  
Adding `w[i]` gives a weight not larger than the candidate weight
considered by the DP for the same `k = |S|`.  
Consequently the DP state for this `k` (and for all larger `k`) has weight
≥ weight(`S`).  
Taking the maximum over all `k ≤ 4` shows that `best`’s weight is at
least the weight of any feasible set – i.e. it is maximal.

*Lexicographic minimality.*  
Assume there is another optimal set `T` with the same maximal weight
but a lexicographically smaller (sorted) index list.
Let `k = |T|`.  
While processing the intervals the DP examines exactly the same
possibilities that build `T`; by Lemma&nbsp;4 the DP state for `k`
always stores the lexicographically smallest list among all optimal
solutions of weight `weight(T)`.  
Hence the DP cannot contain a list larger than that of `T`.  
The final selection (Lemma&nbsp;6) would therefore pick `T`’s list,
contradiction.  So no such `T` exists. ∎



##### Theorem  
`maximumWeight` returns the lexicographically smallest array of at most
four indices whose intervals are pairwise non‑overlapping and whose total
weight is maximal.

**Proof.**  
The method returns the list part of `best`.  
By Lemma&nbsp;7 `best` satisfies exactly the required properties,
hence the returned list is correct. ∎



--------------------------------------------------------------------

#### 6.   Complexity Analysis  

*Sorting* : `O(n log n)`  
*Binary searches for `prev[i]`* : `O(n log n)`  

*Main DP* : for each of the `n` intervals and each `k = 1 … 4`

* one Fenwick query   → `O(log n)`
* one Fenwick update   → `O(log n)`

Total `O( n·k·log n )   ≤ 4·n·log₂ n   ≤ 3·10⁶` operations.

Memory  

* sorted data : `4·n` integers  →  `O(n)`
* five Fenwick trees : `5·(n+1)` entries → `O(n)`
* only the previous DP row → `O(k)`

Overall `O(n)` additional memory (well below the limits).

--------------------------------------------------------------------

#### 7.   Reference Implementation  (Python 3)

```python
import bisect
from typing import List, Tuple

class BIT:
    """Fenwick tree for prefix maximum of (weight, list) pairs."""
    __slots__ = ('n', 'tree')

    def __init__(self, n: int):
        self.n = n
        self.tree = [(0, ())] * (n + 1)          # 1‑based

    def _better(self, a: Tuple[int, Tuple[int, ...]],
                b: Tuple[int, Tuple[int, ...]]) -> Tuple[int, Tuple[int, ...]]:
        """return the better of two states (weight, list)."""
        if a[0] != b[0]:
            return a if a[0] > b[0] else b
        # equal weight → lexicographically smaller list
        return a if a[1] < b[1] else b

    def update(self, idx: int, val: Tuple[int, Tuple[int, ...]]) -> None:
        """set position idx (1‑based) to the better of current and val."""
        n = self.n
        tree = self.tree
        while idx <= n:
            tree[idx] = self._better(tree[idx], val)
            idx += idx & -idx

    def query(self, idx: int) -> Tuple[int, Tuple[int, ...]]:
        """best value in prefix [1 .. idx] (inclusive)."""
        res = (0, ())
        tree = self.tree
        while idx:
            res = self._better(res, tree[idx])
            idx -= idx & -idx
        return res


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        # ---------- 1. sort by right end ----------
        n = len(intervals)
        indexed = list(enumerate(intervals))                # (orig_idx, [l,r,w])
        indexed.sort(key=lambda x: (x[1][1], x[1][0]))      # sort by r, then l

        ends = [0] * n
        starts = [0] * n
        weights = [0] * n
        orig_idx = [0] * n

        for i, (orig, iv) in enumerate(indexed):
            l, r, w = iv
            starts[i] = l
            ends[i] = r
            weights[i] = w
            orig_idx[i] = orig

        # ---------- 2. predecessor for each interval ----------
        prev = [-1] * n
        for i in range(n):
            # last index with end < start[i]
            pos = bisect.bisect_left(ends, starts[i]) - 1
            prev[i] = pos

        # ---------- 3. DP with Fenwick trees ----------
        MAXK = 4
        bits = [BIT(n) for _ in range(MAXK + 1)]   # bits[0] is never updated
        # dpPrev[k] = best (weight, list) using at most k intervals up to previous i
        dpPrev = [(0, ())] * (MAXK + 1)            # dpPrev[0] always (0, ())

        for i in range(n):
            w = weights[i]
            idx = orig_idx[i]
            p = prev[i]

            for k in range(1, MAXK + 1):
                # best result with k-1 intervals that end before start[i]
                if p >= 0:
                    bestPrevW, bestPrevL = bits[k - 1].query(p + 1)
                else:
                    bestPrevW, bestPrevL = 0, ()

                candW = bestPrevW + w
                # new list = sorted(bestPrevL ∪ {idx})
                candL = tuple(sorted(bestPrevL + (idx,)))

                # previous best without using i
                prevW, prevL = dpPrev[k]

                # choose the better one
                if candW > prevW:
                    cur = (candW, candL)
                elif candW < prevW:
                    cur = (prevW, prevL)
                else:                           # equal weight → smaller list
                    cur = (candW, candL) if candL < prevL else (prevW, prevL)

                dpPrev[k] = cur
                bits[k].update(i + 1, cur)      # i+1 because BIT is 1‑based

        # ---------- 4. pick the overall best ----------
        best = (0, ())
        for k in range(MAXK + 1):
            w, lst = dpPrev[k]
            if w > best[0] or (w == best[0] and lst < best[1]):
                best = (w, lst)

        return list(best[1])                     # already sorted increasingly
```

The code follows exactly the algorithm proven correct above
and conforms to the required function signature.