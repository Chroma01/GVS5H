
## ideation
**Solution Explanation**

For a triple of indices `i , j , k   ( 0 ≤ i , j , k < N )`

```
value(i , j , k) = A[i]·B[j] + B[j]·C[k] + C[k]·A[i]
```

All `A , B , C` are given, `N ≤ 2·10⁵` and we have to output the
`K`‑th largest value among the `N³` possible triples.
`K ≤ 5·10⁵`.

--------------------------------------------------------------------

#### 1.   Monotonicity  

Sort the three arrays **in non‑increasing order**

```
A[0] ≥ A[1] ≥ … ≥ A[N-1]      (the same for B and C)
```

For a fixed `j , k`

```
value(i+1 , j , k) - value(i , j , k)
 = (A[i+1] – A[i])·(B[j] + C[k]) ≤ 0               (B[j]+C[k] > 0)
```

The value never increases when we increase an index,
and it never decreases when we *decrease* an index.
The same holds for the second and the third position.
Therefore

```
(i , j , k)  ≤  (i' , j' , k')   (component‑wise)   ⇒
value(i , j , k) ≥ value(i' , j' , k')
```

The whole set of triples is a three‑dimensional monotone lattice.



--------------------------------------------------------------------

#### 2.   Best‑first search on the lattice  

Think of the triples as vertices of a directed acyclic graph.
From a vertex `(i , j , k)` we can go to the three neighbours

```
(i+1 , j , k) , (i , j+1 , k) , (i , j , k+1)          (if the index stays < N)
```

All edges go *downwards* in the value ordering,
so the graph has the same monotone property as above.

We start with the unique maximal vertex `(0,0,0)`.
A **max‑heap** (implemented by `heapq` with negative numbers) stores
all vertices whose value we already know.
At each step we pop the vertex with the largest value,
output it, and push its three neighbours (if they have not been
visited before).  
Because every still unvisited vertex can be reached from a vertex that
is already in the heap, the heap always contains the next largest
value.  
Repeating this `K` times yields the `K` largest triples in descending
order; the value of the `K`‑th popped vertex is the answer.

The set `visited` prevents the same triple from being inserted many
times.  
A triple is encoded as a single integer

```
code(i , j , k) = ((i * N) + j) * N + k        (0 ≤ i , j , k < N ≤ 2·10⁵)
```

so the set contains ordinary Python integers – fast and memory‑friendly.



--------------------------------------------------------------------

#### 3.   Correctness Proof  

We prove that the algorithm prints the required `K`‑th largest value.

---

##### Lemma 1  
For any indices `i , j , k`

```
value(i , j , k) ≥ value(i+1 , j , k) ,
value(i , j , k) ≥ value(i , j+1 , k) ,
value(i , j , k) ≥ value(i , j , k+1) .
```

**Proof.**  
All arrays are sorted non‑increasingly.
Consider the first inequality:

```
value(i+1 , j , k) - value(i , j , k)
 = (A[i+1] – A[i])·(B[j] + C[k]) .
```

`B[j] + C[k]` is positive, while `A[i+1] – A[i] ≤ 0`,
hence the whole product is ≤ 0.
The other two inequalities are analogous. ∎



##### Lemma 2  
Let `S` be the set of triples already removed from the heap
(`S` initially contains only `(0,0,0)`).  
Every triple not in `S` is reachable from at least one vertex that is
currently inside the heap by repeatedly applying one of the three
neighbour moves.

**Proof.**  
The heap always contains *all* neighbours of the vertices that have
just been taken out (unless they are already visited).  
Consequently, after processing the first `t` popped vertices,
the heap contains the boundary of the explored region.
Any vertex outside this region has a coordinate larger than the
corresponding coordinate of *some* vertex on the boundary, otherwise it
would already belong to the explored region.
Thus it can be reached by increasing that coordinate step by step,
i.e. by a path of neighbour moves starting at a boundary vertex that
lies in the heap. ∎



##### Lemma 3  
When the heap pops a vertex `v`, `value(v)` is the largest value among
all triples that have not been popped yet.

**Proof.**  
All not yet popped triples belong to the set `U` (the complement of the
already popped set `S`).  
By Lemma&nbsp;2 each `u ∈ U` can be reached from a vertex `h` that is
currently inside the heap.  
Because of Lemma&nbsp;1 the value never increases along a neighbour
move, therefore `value(h) ≥ value(u)`.  
The heap is a max‑heap, thus the vertex `v` that is removed has the
maximum value among *all* vertices inside the heap, and consequently
`value(v) ≥ value(u)` for every `u ∈ U`. ∎



##### Lemma 4  
The sequence of values taken from the heap is strictly non‑increasing
and contains each possible triple exactly once.

**Proof.**  
*Strictly non‑increasing* follows from Lemma&nbsp;3: each newly popped
value is not larger than any value that will be popped later.  

*Uniqueness* is guaranteed by the `visited` set.
A triple is inserted into the heap only when it is first discovered,
i.e. when a neighbour move from an already popped vertex reaches it.
Before insertion we test `code(i,j,k) ∉ visited`; after insertion the
code is added to `visited`.  
Hence the same code can never be inserted again, therefore the same
triple is never taken from the heap twice. ∎



##### Lemma 5  
After the `K`‑th extraction the algorithm has output the `K` largest
values among all `N³` triples.

**Proof.**  
By Lemma&nbsp;3 the first extracted value is the overall maximum,
the second extracted value is the largest among the remaining ones,
and so on.  
Thus after the `K`‑th extraction we have obtained the `K` largest
values, each exactly once (Lemma&nbsp;4). ∎



##### Theorem  
The program prints the `K`‑th largest value of  
`A[i]·B[j] + B[j]·C[k] + C[k]·A[i]` over all triples
`0 ≤ i , j , k < N`.

**Proof.**  
The algorithm extracts triples in descending order of their values
(Lemmas&nbsp;3–5).  
When the loop counter reaches `K` the currently popped triple has the
`K`‑th largest value, which is stored in the variable `answer` and
printed. ∎



--------------------------------------------------------------------

#### 4.   Complexity Analysis  

*Sorting* three arrays: `O(N log N)` time, `O(N)` memory.  

*Heap operations*  

* at most `3·K` insertions and `K` deletions  
* each `heapq` operation costs `O(log M)` where `M ≤ 3·K`

```
Time   :  O( K log K )   ≤  O(5·10⁵ · log 5·10⁵)   < 2·10⁷ operations
Memory :  O( K ) for the heap  +  O( K ) for the visited set
          ≤  a few hundred megabytes, well inside typical limits
```

The algorithm never materialises the `N³` triples.

--------------------------------------------------------------------

#### 5.   Reference Implementation  (Python 3)

```python
import sys
import heapq

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    K = int(next(it))

    A = [int(next(it)) for _ in range(N)]
    B = [int(next(it)) for _ in range(N)]
    C = [int(next(it)) for _ in range(N)]

    # sort decreasing, this gives the monotone property
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    a, b, c = A, B, C               # local names (speed)
    n = N

    # encode a triple (i,j,k) into a single integer
    def encode(i: int, j: int, k: int) -> int:
        return ((i * n) + j) * n + k

    # value of a triple
    def val(i: int, j: int, k: int) -> int:
        return a[i] * b[j] + b[j] * c[k] + c[k] * a[i]

    heap = []                       # max‑heap via negative values
    heapq.heappush(heap, (-val(0, 0, 0), 0, 0, 0))

    visited = set()
    visited.add(0)                  # encode(0,0,0)

    answer = None
    for step in range(K):
        neg, i, j, k = heapq.heappop(heap)
        cur = -neg
        if step == K - 1:           # K‑th extraction
            answer = cur
            break

        # neighbour (i+1, j, k)
        if i + 1 < n:
            code = encode(i + 1, j, k)
            if code not in visited:
                visited.add(code)
                heapq.heappush(heap, (-val(i + 1, j, k), i + 1, j, k))

        # neighbour (i, j+1, k)
        if j + 1 < n:
            code = encode(i, j + 1, k)
            if code not in visited:
                visited.add(code)
                heapq.heappush(heap, (-val(i, j + 1, k), i, j + 1, k))

        # neighbour (i, j, k+1)
        if k + 1 < n:
            code = encode(i, j, k + 1)
            if code not in visited:
                visited.add(code)
                heapq.heappush(heap, (-val(i, j, k + 1), i, j, k + 1))

    sys.stdout.write(str(answer))

if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above and
conforms to the required input / output format.

## worker: finalize
- Sorting the three arrays in non‑increasing order makes the expression  
  `A[i]·B[j] + B[j]·C[k] + C[k]·A[i]` monotone non‑increasing in each index,  
  enabling a best‑first search on a 3‑dimensional lattice.
- A max‑heap (implemented by storing negative values) always extracts the current
  largest unvisited triple, and the `K`‑th extraction yields the K‑th largest value.
- The algorithm runs in `O(N log N + K log K)` time and uses `O(N + K)` memory,  
  well within the limits (`K ≤ 5·10⁵`).
