**Solution Explanation**

For a rating `x` after processing some contests we denote by `f(x)` the rating
after all contests.  
While the contests are processed we keep an array

```
f[i] = rating after the already processed contests
       when the initial rating was i                (1 ≤ i ≤ M)
```

`M` is chosen large enough so that all values that can appear are inside the
array ( `M = max query X + N` is sufficient, because a rating can increase at
most `N` times).

--------------------------------------------------------------------

#### 1.   Behaviour of one contest

For a contest with interval `[L,R]`

```
if L ≤ f[i] ≤ R   →   f[i] += 1
else               →   f[i] unchanged
```

--------------------------------------------------------------------

#### 2.   Important property – monotonicity  

`f` is **non‑decreasing** :

*Initially* `f[i]=i` is increasing.  
Assume after some contests `f` is non‑decreasing.
The set `{ i | L ≤ f[i] ≤ R }` is a (possibly empty) contiguous segment,
because the condition “`f[i] ≥ L`” and “`f[i] ≤ R`” are both monotone
in `i`.  
Adding `1` to this whole segment does not break the order,
hence the new array is again non‑decreasing.
By induction the property holds for all steps.

Consequences

* the set of indices that have to be increased is a single interval
  `[a , b]`
* `a` is the first index with `f[i] ≥ L`  ⇔ `f[i] > L‑1`
* `b` is the last  index with `f[i] ≤ R`  ⇔ `b = (first index with f[i] > R) – 1`

--------------------------------------------------------------------

#### 3.   Data structure  

We need a structure that supports

* range add `+1` on an interval `[a,b]`
* find the first index with value `> val`
* point query (final value of a given `i`)

A lazy segment tree storing only the **maximum** in each node is enough.
With lazy propagation a whole interval can be increased in `O(log M)`,
and the “first index with value `> val`” can be found by descending the tree:
if the left child’s maximum is `> val` we go left, otherwise right.
The point query follows the same path while pushing lazy values.

The tree size is a power of two `size ≥ M+1`.  
Leaves `> M` are filled with `-1`; they never satisfy `> val (val ≥ 0)` and
are never updated, so they never influence the answer.

--------------------------------------------------------------------

#### 4.   Algorithm
```
read N, intervals
read Q, queries
M = max_query + N
build segment tree for i = 1..M :  f[i] = i          (max = i)

for each interval (L,R):
        a = first_index_with_value > L-1
        b = first_index_with_value > R  - 1
        if a ≤ b:
                range_add(a , b , +1)

for each query X:
        answer = point_query(X)
        output answer
```

All operations are `O(log M)`, therefore

```
time   :  O( (N + Q) log (maxX+N) )   ≤ 2·10⁵·log 7·10⁵  + 3·10⁵·log 7·10⁵
memory :  two integer arrays of length 2·size  (≈ 4·size integers)
          size ≤ 2²⁰ = 1 048 576   →   < 120 MiB
```

Both limits satisfy the constraints.

--------------------------------------------------------------------

#### 5.   Correctness Proof  

We prove that the algorithm outputs the correct final rating for every query.

---

##### Lemma 1  
After processing any number of contests the array `f[1…M]` is non‑decreasing.

**Proof.**  
Initially `f[i]=i`, clearly non‑decreasing.  
Assume after some contests `f` is non‑decreasing.
For the next interval `[L,R]` the set
`S = { i | L ≤ f[i] ≤ R }` is an interval `[a,b]`
(because the conditions `f[i] ≥ L` and `f[i] ≤ R` are monotone).
All indices in `S` receive `+1`, all others stay unchanged.
For `i = a-1` we have `f[a-1] ≤ f[a] ≤ R`, after the update
`f'[a-1] = f[a-1] ≤ f[a]+1 = f'[a]`.  
For `i = b` we have `f[b] ≤ R` and `f[b+1] > R`.  
After the update `f'[b] = f[b]+1 ≤ R+1 ≤ f[b+1] = f'[b+1]`.  
All other relations stay unchanged, therefore the new array is again
non‑decreasing. ∎



##### Lemma 2  
Let `a` be the first index with `f[a] ≥ L` and `b` the last index with
`f[b] ≤ R`. Then the set of indices whose rating belongs to `[L,R]`
is exactly the interval `[a,b]`.

**Proof.**  
Because of Lemma&nbsp;1,
`f[i] ≥ L` holds for every `i ≥ a` and fails for `i < a`;
`f[i] ≤ R` holds for every `i ≤ b` and fails for `i > b`.  
Consequently the two conditions are simultaneously true
iff `a ≤ i ≤ b`. ∎



##### Lemma 3  
During the processing of a contest `[L,R]` the algorithm adds `+1`
exactly to those `i` for which the rating would increase in the real
process.

**Proof.**  
The algorithm computes `a = first index with f[i] > L-1`
which is equivalent to “first index with `f[i] ≥ L`”.
It computes `b = (first index with f[i] > R) – 1`,
i.e. the last index with `f[i] ≤ R`.  
By Lemma&nbsp;2 the indices with `L ≤ f[i] ≤ R` are precisely `[a,b]`.
The algorithm performs a range add `+1` on exactly this interval,
so each of those `f[i]` is increased by one and no other index is
changed – exactly the effect of the contest. ∎



##### Lemma 4  
After processing the first `k` contests (`0 ≤ k ≤ N`) the array `f`
stored in the segment tree equals the true rating after those `k` contests
for every initial rating `i (1 ≤ i ≤ M)`.

**Proof by induction over `k`.**  

*Base `k = 0`.*  
The tree is initialised with `f[i]=i`, which is the correct rating
before any contest.

*Induction step.*  
Assume the statement true after `k-1` contests.
For the `k`‑th contest the algorithm applies the update described in
Lemma&nbsp;3, which is exactly the rule of the real process.
Therefore after the update the array `f` coincides with the true ratings
after `k` contests. ∎



##### Lemma 5  
For any query `X` the value returned by `point_query(X)` equals the final
rating after all `N` contests when the initial rating is `X`.

**Proof.**  
By Lemma&nbsp;4 with `k = N` the segment tree stores the true final
ratings for every index. The point query reads that stored value. ∎



##### Theorem  
The algorithm prints the correct answer for every query.

**Proof.**  
For each query `X` the algorithm outputs the result of `point_query(X)`.
By Lemma&nbsp;5 this value equals the real final rating.
Thus all printed numbers are correct. ∎



--------------------------------------------------------------------

#### 6.   Complexity Analysis  

```
M = maxX + N   ≤ 5·10⁵ + 2·10⁵ = 7·10⁵
size = smallest power of two ≥ M+1 ≤ 2²⁰ = 1 048 576

building the tree:          O(size)
each of the N intervals:    O(log size)   (two searches + one range add)
each of the Q queries:      O(log size)   (point query)

Total time   O((N+Q) log size)  ≤  (5·10⁵)·20  < 1·10⁷ operations
Memory       two integer arrays of length 2·size  (< 120 MiB)
```

Both bounds satisfy the limits.

--------------------------------------------------------------------

#### 7.   Reference Implementation  (Python 3)

```python
import sys

def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    N = next(it)
    intervals = [(next(it), next(it)) for _ in range(N)]

    Q = next(it)
    queries = [next(it) for _ in range(Q)]
    if not queries:
        return

    max_x = max(queries)
    M = max_x + N                     # enough for all possible values

    # ----- build segment tree (only maximum and lazy value) -----
    size = 1
    while size < M + 1:               # we need a leaf for every 1..M
        size <<= 1

    maxv = [-1] * (2 * size)          # maximum in the node interval
    lazy = [0] * (2 * size)           # pending addition

    for i in range(1, M + 1):
        maxv[size + i] = i
    for i in range(size - 1, 0, -1):
        maxv[i] = max(maxv[i << 1], maxv[i << 1 | 1])

    n = M                              # largest valid index

    # ----- helper functions -----
    def push(node: int) -> None:
        """propagate lazy value to children"""
        if lazy[node]:
            v = lazy[node]
            l = node << 1
            r = l | 1
            maxv[l] += v
            lazy[l] += v
            maxv[r] += v
            lazy[r] += v
            lazy[node] = 0

    def range_add(node: int, l: int, r: int, ql: int, qr: int, val: int) -> None:
        """add val to interval [ql,qr]"""
        if ql <= l and r <= qr:
            maxv[node] += val
            lazy[node] += val
            return
        push(node)
        mid = (l + r) // 2
        if ql <= mid:
            range_add(node << 1, l, mid, ql, qr, val)
        if qr > mid:
            range_add(node << 1 | 1, mid + 1, r, ql, qr, val)
        maxv[node] = max(maxv[node << 1], maxv[node << 1 | 1])

    def first_gt(node: int, l: int, r: int, val: int) -> int:
        """precondition: maxv[node] > val, returns leftmost index with value > val"""
        if l == r:
            return l
        push(node)
        mid = (l + r) // 2
        if maxv[node << 1] > val:
            return first_gt(node << 1, l, mid, val)
        else:
            return first_gt(node << 1 | 1, mid + 1, r, val)

    def find_first_gt(val: int) -> int:
        """returns first index with value > val, or n+1 if none"""
        if maxv[1] <= val:
            return n + 1
        return first_gt(1, 1, size, val)

    def point_query(node: int, l: int, r: int, idx: int) -> int:
        """value at position idx"""
        while l != r:
            push(node)
            mid = (l + r) // 2
            if idx <= mid:
                node = node << 1
                r = mid
            else:
                node = node << 1 | 1
                l = mid + 1
        return maxv[node]

    # ----- process all contests -----
    for L, R in intervals:
        a = find_first_gt(L - 1)          # first index with f[i] >= L
        b = find_first_gt(R) - 1          # last  index with f[i] <= R
        if a <= b:
            range_add(1, 1, size, a, b, 1)

    # ----- answer queries -----
    out = []
    for x in queries:
        out.append(str(point_query(1, 1, size, x)))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required input‑output format.