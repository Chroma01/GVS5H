**Solution Explanation**

For a permutation `P = (P1 , … , PN)` we may repeatedly

*choose `i ( 1 ≤ i ≤ N‑1 )`, pay `i` and swap `Pi , Pi+1`.*

The cost of a swap is the index of the left element.
We have to obtain the sorted permutation `(1,2,…,N)` with minimum total cost.



--------------------------------------------------------------------

#### 1.   What does a swap mean for the two elements ?

When the element at position `i` (call it **L** – the larger one) swaps with the
element at `i+1` (call it **S** – the smaller one) the two numbers exchange
their relative order.
Only the left element moves to the right, therefore the cost `i` is paid **once**
for this inversion.
So each inversion (pair `L > S` which is currently in the wrong order) is
resolved by exactly one swap, and the price of that swap is the current
position of the larger element.



--------------------------------------------------------------------

#### 2.   How many times does a fixed element move to the right ?

Consider a fixed value `v`.

* `r(v)` – number of *smaller* elements that are **right** of `v`
  in the original permutation.  
  Those are exactly the inversions where `v` is the larger element,
  therefore `v` has to move to the right `r(v)` times.

* `l(v)` – number of *larger* elements that are **left** of `v`.  
  In those inversions `v` is the smaller element, therefore it moves **left**
  `l(v)` times (this movement is free – the cost is paid by the larger
  elements).

If we first move `v` left across all larger elements on its left,
its position becomes

```
pos(v) – l(v)               (1)
```

and afterwards it has to move right `r(v)` times.
During the `k`‑th right move (k = 0 … r(v)-1) its position is

```
pos(v) – l(v) + k          (2)
```

Hence the total contribution of `v` to the answer is the sum of (2) for all
`k` :

```
cost(v) = r(v)·(pos(v) – l(v)) + r(v)·(r(v) – 1) / 2          (3)
```

--------------------------------------------------------------------

#### 3.   A simple identity

From the definition of `l(v)` and `r(v)`

```
pos(v) – 1 = l(v) + (v-1 – r(v))                (elements left of v)
```

and therefore

```
pos(v) – l(v) = v – r(v)                       (4)
```

Insert (4) into (3)

```
cost(v) = r(v)·(v – r(v)) + r(v)·(r(v) – 1)/2
        = r(v)·v – r(v)·(r(v) + 1)/2                     (5)
```

Only `r(v)` is needed.



--------------------------------------------------------------------

#### 4.   Computing `r(v)` for all values

While scanning the values in increasing order we keep a Fenwick tree
(`BIT`) that stores, for each position, whether a *smaller* value already
appeared.

* `leftSmaller = BIT.sum( pos(v) – 1 )` – how many already processed
  (i.e. smaller) values are left of `v`.
* `r(v) = (v-1) – leftSmaller` – the other smaller values must be on the
  right.

Both operations are `O(log N)`.



--------------------------------------------------------------------

#### 5.   Whole algorithm

```
read N and permutation P
pos[value] = its index (1‑based)
BIT = empty
answer = 0
for v = 1 … N
        leftSmaller = BIT.prefix_sum( pos[v] - 1 )
        r = (v-1) - leftSmaller
        answer += r * v - r * (r + 1) // 2
        BIT.add( pos[v] , 1 )          # insert v into the structure
print answer
```

`answer` fits easily into Python’s arbitrary precision integers
(the worst case is `Θ(N³) ≈ 1.3·10¹⁵` for `N = 2·10⁵`).

--------------------------------------------------------------------

#### 6.   Correctness Proof  

We prove that the algorithm outputs the minimum possible total cost.

---

##### Lemma 1  
For a value `v` the number of times `v` moves to the right during any sorting
process equals `r(v)` (the number of smaller elements originally to the right
of `v`).

**Proof.**  
Each smaller element to the right of `v` forms an inversion with `v`.
To resolve this inversion `v` must be on the right side of that element,
hence `v` must move right at least once for each such element.
Conversely, `v` can never move right without crossing a smaller element on
its right, otherwise the relative order of `v` and that element would stay
wrong. ∎



##### Lemma 2  
In any sorting process the position of `v` when it makes its `k`‑th
rightward move (`k = 0 … r(v)-1`) is at least `v – r(v) + k`.

**Proof.**  
Before any rightward move, `v` has already passed all larger elements that were
originally to its left, i.e. it has moved left `l(v)` steps.
Its position is therefore `pos(v) – l(v) = v – r(v)` (by (4)).
Each rightward move increases the position by one, so after `k` moves the
position is `v – r(v) + k`.  No sorting can make `v` cross a smaller element
earlier (more left) because that would require `v` to have moved left more
than `l(v)` steps, which is impossible. ∎



##### Lemma 3  
The total cost contributed by a value `v` in any sorting process is at least
`r(v)·v – r(v)·(r(v)+1)/2`.

**Proof.**  
By Lemma&nbsp;1 the element `v` moves right `r(v)` times.
By Lemma&nbsp;2 the cheapest possible positions for these moves are
`v‑r(v) , v‑r(v)+1 , … , v‑1`.  
The sum of the cheapest possible positions is exactly the expression of the
lemma, therefore any sorting process pays at least that amount for `v`. ∎



##### Lemma 4  
The algorithm’s sum `Σ ( r(v)·v – r(v)·(r(v)+1)/2 )` equals the total cost of
the following concrete strategy:

*Process the values in increasing order.
For the current value `v` first move it left across all larger elements that
are still left of it (free), then move it right across the remaining smaller
elements one by one.*

**Proof.**  
When we start processing `v` all larger values have already been placed at
their final positions (to the right of `v`).  
All leftward moves of `v` happen now, its position becomes `v‑r(v)`.
Now exactly the `r(v)` smaller elements that are still on the right are
crossed one after another, each crossing costs the current position
`v‑r(v) , v‑r(v)+1 , … , v‑1`.  
The total cost of `v` in this construction is precisely the term of the
algorithm. Summation over all `v` gives the claimed total cost. ∎



##### Lemma 5  
The algorithm’s answer can be achieved (i.e. the strategy of Lemma&nbsp;4
is feasible).

**Proof.**  
The described sequence consists only of adjacent swaps, therefore it is a
legal sequence of operations.
Each swap is performed at the current position of the left element,
hence its cost is exactly the left index, as required. ∎



##### Theorem  
The number printed by the algorithm is the minimum possible total cost to
sort the permutation.

**Proof.**  
*Lower bound*: By Lemma&nbsp;3 any sorting process pays at least
`r(v)·v – r(v)·(r(v)+1)/2` for each `v`, thus at least the sum of those
terms.

*Upper bound*: Lemma&nbsp;4 shows that a concrete sorting process with exactly
that total cost exists, and Lemma&nbsp;5 guarantees its feasibility.

Since the lower bound equals the upper bound, the sum computed by the
algorithm is optimal. ∎



--------------------------------------------------------------------

#### 7.   Complexity Analysis

*Fenwick tree operations* – `O(log N)` each.  
We perform one query and one update for every value `v` → `O(N log N)` time.

Memory consumption: the permutation positions (`N+1` integers) and the
Fenwick tree (`N+1` integers) → `O(N)`.



--------------------------------------------------------------------

#### 8.   Reference Implementation  (Python 3)

```python
import sys

# -------------------------------------------------------------

class Fenwick:
    """1‑based Fenwick tree for prefix sums."""
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx: int, delta: int) -> None:
        while idx <= self.n:
            self.bit[idx] += delta
            idx += idx & -idx

    def sum(self, idx: int) -> int:
        s = 0
        while idx:
            s += self.bit[idx]
            idx -= idx & -idx
        return s

# -------------------------------------------------------------

def solve() -> None:
    input = sys.stdin.readline
    N = int(input())
    P = list(map(int, input().split()))
    pos = [0] * (N + 1)           # pos[value] = index (1‑based)
    for i, v in enumerate(P, start=1):
        pos[v] = i

    bit = Fenwick(N)
    ans = 0

    for v in range(1, N + 1):
        # number of already processed (smaller) values left of v
        left_smaller = bit.sum(pos[v] - 1)
        r = (v - 1) - left_smaller          # smaller elements to the right
        # contribution of v, formula (5)
        ans += r * v - r * (r + 1) // 2
        bit.add(pos[v], 1)                  # insert v

    print(ans)

# -------------------------------------------------------------
if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above and conforms
to the required input‑output format.