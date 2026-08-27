**Solution Explanation**

For a subarray `A[L … R]`

```
S(L,R) = { A[i] | L ≤ i ≤ R }          (set of values appearing in the subarray)
```

During one operation we may choose any interval of *values* `[l , r]` (`l ≤ r`) that
is completely contained in the current set of values, i.e.

```
{ l , l+1 , … , r } ⊆ current set
```

and all occurrences of those values disappear.
The operation removes a whole contiguous block of values.

--------------------------------------------------------------------

#### 1.   From operations to the answer `f(L,R)`

Write the distinct values of `S(L,R)` in increasing order

```
v1 < v2 < … < vk
```

Two different values can be erased together **iff** they are consecutive
integers, because the chosen block must contain *every* integer between its
ends.
Therefore the values are split into maximal consecutive groups

```
{1,2,3} , {5,6} , {8}
```

Each group can be erased in one operation, and we can never erase two
different groups together (the missing integer between them is not present).
Consequently

```
f(L,R) = number of groups of consecutive values in S(L,R)
```

If `d = |S(L,R)|` (the number of distinct values) and
`e` is the number of adjacent pairs `{v , v+1}` that are both present,
the groups are exactly the connected components of the graph consisting of
those vertices and the edges `{v , v+1}`.
For a forest   `components = vertices – edges`, thus

```
f(L,R) = d(L,R) – e(L,R)                              (1)
```

The required sum is

```
 Σ f(L,R) = Σ d(L,R)  –  Σ e(L,R)                     (2)
```

So we have to compute the two sums in (2) independently.



--------------------------------------------------------------------

#### 2.   Σ d(L,R) – the sum of “number of distinct values”

For each position `i` (`1‑based`) let `prev[i]` be the previous occurrence of
`A[i]` (`0` if none).  
In a subarray `[L,R]` the *first* occurrence of the value `A[i]` is at position
`i` **iff** `L` lies in the interval `(prev[i] , i]`.
The right end `R` can be any index `≥ i`.

```
#subarrays where i is the first occurrence of A[i] = (i – prev[i]) · (N – i + 1)
```

Summation over all positions gives the total number of distinct elements
over all subarrays.

```
totalDistinct = Σ (i – prev[i]) · (N – i + 1)          (3)
```

`prev[i]` is obtained by a simple array `lastPos[value]` while scanning the
sequence once – **O(N)** time.



--------------------------------------------------------------------

#### 3.   Σ e(L,R) – the sum of “adjacent value pairs”

Fix a concrete pair of values `{v , v+1}` (`1 ≤ v ≤ N‑1`).
For a fixed right end `R` let

```
lastV(R) = last index ≤ R where value v occurs (0 if never)
lastV1(R) = last index ≤ R where value v+1 occurs
```

A subarray `[L,R]` contains both values `v` and `v+1`
iff `L ≤ min(lastV(R), lastV1(R))`.
Therefore the number of such subarrays ending at `R` equals
`min(lastV(R), lastV1(R))` (or `0` if one of the two values never appeared).

Summed over all `R` we obtain the contribution of the pair `{v , v+1}`.
The total number of adjacent pairs over all subarrays is

```
totalAdj = Σ_R  Σ_{v=1}^{N-1}  min( lastV(R) , lastV1(R) )      (4)
```

The inner sum contains `N‑1` terms, but only two of them change when we move
`R` one step to the right – the pairs that involve the newly seen value
`A[R]`.  
Consequences:

* for a fixed `R` we keep the current value  

  `cur = Σ_v min(lastV , lastV1)` (the inner sum of (4) for this `R`);
* `cur` can be updated in **O(1)** by recomputing the two affected minima;
* the answer `totalAdj` is `cur[1] + cur[2] + … + cur[N]`.

Implementation details

```
cur = 0
for R = 1 … N
        a = A[R]
        for each v in { a-1 , a } that lies in [1 , N-1]
                old = min( last[v] , last[v+1] )
                store old
        last[a] = R                     # update the last occurrence of a
        for each stored v
                new = min( last[v] , last[v+1] )
                cur += new - old
        totalAdj += cur
```

Only two iterations per position, overall **O(N)** time,
`O(N)` extra memory for the `last` array.



--------------------------------------------------------------------

#### 4.   Final answer

From (2), (3) and (4)

```
answer = totalDistinct – totalAdj
```

Both parts are computed in linear time, so the whole algorithm works in
`O(N)` time and `O(N)` memory, well within the limits (`N ≤ 3·10⁵`).

--------------------------------------------------------------------

#### 5.   Correctness Proof  

We prove that the algorithm outputs the required sum.

---

##### Lemma 1  
For any subarray `A[L…R]` the minimal number of operations `f(L,R)` equals
the number of connected components of the set `S(L,R)` of distinct values,
where two values are adjacent if they are consecutive integers.

**Proof.**  
An operation may delete a whole interval `[l,r]` of values only if *all*
values `l,…,r` are present. Consequently an operation can delete values that
belong to a single connected component and cannot delete values from two
different components (the missing integer between the components is not
present).  

If a component contains more than one value, deleting it in one operation is
possible, and splitting a component into several operations can only increase
the total number of operations.  
Therefore the optimal strategy is to delete each component in a single
operation, and the optimal number of operations equals the number of
components. ∎



##### Lemma 2  
For a subarray let `d` be the number of distinct values and `e` the number of
adjacent value pairs `{v , v+1}` that are both present.
Then the number of components of the set of distinct values is `d – e`.

**Proof.**  
Consider the graph whose vertices are the distinct values and whose edges are
exactly the present adjacent pairs. This graph is a disjoint union of paths,
i.e. a forest. For a forest the relation  

```
#components = #vertices – #edges
```

holds, giving `d – e`. ∎



##### Lemma 3  
`totalDistinct` computed by formula (3) equals  
` Σ_{L≤R} d(L,R) `, the sum of the numbers of distinct values over all
subarrays.

**Proof.**  
Fix a position `i`. In a subarray `[L,R]` the *first* occurrence of the value
`A[i]` is at `i` exactly when `L` is after the previous occurrence of the same
value (`L > prev[i]`) and `L ≤ i`. The number of possible `L` is `i‑prev[i]`.
For a fixed such `L` the right end `R` may be any index `≥ i`, i.e. `N‑i+1`
possibilities. Hence the value `A[i]` contributes `1` to the distinct count of
exactly `(i‑prev[i])·(N‑i+1)` subarrays. Summation over all positions counts
each distinct value once for each subarray, which is precisely the total sum
of distinct counts. ∎



##### Lemma 4  
`totalAdj` computed by the algorithm equals  
` Σ_{L≤R} e(L,R) `, the sum of the numbers of present adjacent pairs over
all subarrays.

**Proof.**  
Consider a fixed pair `{v , v+1}`. For a fixed right end `R` let
`lastV(R) , lastV1(R)` be the last occurrences of `v` and `v+1` not exceeding
`R` (or `0` if absent). A subarray `[L,R]` contains both values iff
`L ≤ min(lastV,lastV1)`. The number of such left ends equals
`min(lastV,lastV1)` (or `0`). Therefore the total number of subarrays that
contain this pair is  

```
 Σ_R  min(lastV(R), lastV1(R)).
```

Summing this equality over all `v = 1 … N‑1` yields exactly the right hand side
of (4).  

During the scan the algorithm maintains for the current `R` the quantity  

```
cur(R) = Σ_v min(lastV(R), lastV1(R)).
```

When the next element `a = A[R]` is processed, only the two pairs
`{a‑1 , a}` and `{a , a+1}` (if they exist) can change their minima.
The algorithm recomputes the old minima, updates `last[a]`, recomputes the
new minima and adds the difference to `cur`. Consequently after the update
`cur` equals `cur(R)`. Adding `cur` to the accumulator after each step gives

```
totalAdj = Σ_R cur(R) = Σ_R Σ_v min(lastV(R),lastV1(R)),
```

which is the required sum. ∎



##### Lemma 5  
For every subarray `A[L…R]`

```
f(L,R) = d(L,R) – e(L,R).
```

**Proof.**  
By Lemma&nbsp;1 `f(L,R)` equals the number of components of `S(L,R)`.  
By Lemma&nbsp;2 that number equals `|S(L,R)| – e(L,R) = d(L,R) – e(L,R)`. ∎



##### Lemma 6  
The algorithm outputs  

```
 Σ_{L≤R} f(L,R) .
```

**Proof.**  
Using Lemma&nbsp;5 and the linearity of summation

```
 Σ f(L,R) = Σ d(L,R) – Σ e(L,R).
```

By Lemma&nbsp;3 the first sum equals `totalDistinct`, by Lemma&nbsp;4 the
second sum equals `totalAdj`. The algorithm returns `totalDistinct –
totalAdj`, therefore it returns the desired sum. ∎



##### Theorem  
`solve` prints the correct answer for every input satisfying the
constraints.

**Proof.**  
The program computes `totalDistinct` and `totalAdj` exactly as described in
Lemmas&nbsp;3 and&nbsp;4, using only linear‑time scans of the array.
By Lemma&nbsp;6 the printed value equals  
` Σ_{L≤R} f(L,R)`, which is the problem’s required output. ∎



--------------------------------------------------------------------

#### 6.   Complexity Analysis

```
building prev array          : O(N)
first scan (totalDistinct)  : O(N)
second scan (totalAdj)      : O(N)   (only 2 updates per step)
total time                  : O(N)   ( ≤ 3·10⁵ operations )
memory                      : O(N)   (arrays of size N+2)
```

Both limits easily satisfy the constraints.



--------------------------------------------------------------------

#### 7.   Reference Implementation  (Python 3)

```python
import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    # ---------- 1. total number of distinct elements ----------
    last_pos = [0] * (N + 2)          # last occurrence of each value (1..N)
    total_distinct = 0
    for i, v in enumerate(A):
        prev = last_pos[v]
        # i is 0‑based, position = i+1
        total_distinct += (i + 1 - prev) * (N - i)
        last_pos[v] = i + 1

    # ---------- 2. total number of adjacent pairs ----------
    last = [0] * (N + 2)              # last occurrence of each value
    cur = 0                           # Σ_v min(last[v], last[v+1]) for current R
    total_adj = 0

    for i, a in enumerate(A):
        # pairs that may change: (a-1 , a)  and  (a , a+1)
        vs = []
        if a > 1:
            vs.append(a - 1)
        if a < N:
            vs.append(a)

        # old minima before updating last[a]
        old_mins = [min(last[v], last[v + 1]) for v in vs]

        # update the last occurrence of a
        last[a] = i + 1

        # new minima and update cur
        for v, old in zip(vs, old_mins):
            new = min(last[v], last[v + 1])
            cur += new - old

        total_adj += cur

    # ---------- 3. answer ----------
    ans = total_distinct - total_adj
    sys.stdout.write(str(ans))

if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above and conforms
to the required input‑output format.