
## ideation
**Solution Explanation**

For every position `i` we have a letter `S[i]` that has to become `T[i]`.
The operation *replace every `x` by `y`* changes **all** occurrences of `x`
simultaneously, therefore for each letter `c` occurring in `S`
all its positions must have the **same** target letter.
If this is not true the task is impossible.

--------------------------------------------------------------------

#### 1.   Building a functional graph

* `U` – the set of letters that appear in `S`
* for `a ∈ U` let `f(a)` be the (unique) letter that the positions of `a`
  have to become (`f(a) = T[i]` for any `i` with `S[i]=a`)

The mapping `f` is a **functional graph** on the 26 lower‑case letters.
Every vertex of `U` has exactly one outgoing edge `a → f(a)`.
Vertices that are not in `U` have no outgoing edge (they are *sinks*).

The graph consists of several connected components.
In each component there is exactly one directed cycle.
All other vertices are trees directed towards that cycle.

* a **fixed point** is a vertex `a` with `f(a)=a` (a cycle of length 1)
* a **cycle of length ≥ 2** contains no sink

--------------------------------------------------------------------

#### 2.   Cost of one component

*`|Ucomp|` – number of vertices of the component that belong to `U`.*

| type of component                              | minimal operations |
|------------------------------------------------|--------------------|
| tree whose root is **not** in `U` (external sink) | `|Ucomp|`          |
| tree whose root **is** a fixed point            | `|Ucomp| – 1`      |
| cycle of length `k ≥ 2`                         | `k + 1 = |Ucomp| + 1` |

*Why these numbers?*  
In a tree we can repeatedly replace a leaf by its parent.
Each operation eliminates one distinct letter, therefore we need
`(#different letters) – (final letters)`.  
The final letter is the root: it is not in `U` for an external sink,
hence we have to eliminate all `|Ucomp|` letters.
If the root is a fixed point it already stays, we eliminate the other
`|Ucomp|‑1` letters.  

A cycle of length `k` has no sink.  
We break it by using one **temporary** letter that does **not** belong
to the component.  
`k+1` operations are necessary and sufficient (standard construction).

--------------------------------------------------------------------

#### 3.   Whole string

Let  

* `|U|` – number of different letters in `S`
* `f`   – number of fixed points in `U` (`a∈U` with `f(a)=a`)
* `C`   – number of components that contain a cycle of length `≥ 2`

Adding the costs of all components

```
base = |U| - f + C                (each component contributes |Ucomp| - fcomp + Ccomp)
```

Only the `C` cycle components need temporary letters.
All other letters already belong to `L = U ∪ (letters appearing in T)`.
Letters **outside** `L` are free temporaries, their number is

```
free = 26 - |L|
```

If `C ≤ free` every cycle can use its own free temporary, no extra cost.
Otherwise we have to borrow `C - free` letters from `L` as temporaries,
each such borrowing forces one additional operation (restore the borrowed
letter later).

```
extra = max(0, C - free)
answer = base + extra
```

--------------------------------------------------------------------

#### 4.   Detecting cycles (`C`)

Only 26 vertices, we can run a simple DFS.

```
visited[26] = false
C = 0
for each vertex a with a∈U and not visited:
        walk following f(a) while
                – the current vertex is in U
                – it was not visited before
                – it is not already in the current path
        if we meet a vertex already in the current path:
                a cycle is found
                its length = (current path length) - (first index of that vertex)
                if length ≥ 2:   C += 1
        mark all vertices of the current path as visited
```

Self‑loops (`f(a)=a`) are detected as cycles of length 1 and are **not**
counted into `C`.

--------------------------------------------------------------------

#### 5.   Correctness Proof  

We prove that the algorithm prints the minimal number of operations or `-1`.

---

##### Lemma 1  
If for some letter `a` the set `{ T[i] | S[i]=a }` contains two different
letters, it is impossible to transform `S` into `T`.

**Proof.**  
All occurrences of `a` are changed together, so after any sequence of
operations every former `a` becomes the same letter.
If two positions of `a` need to become different letters, the task is
impossible. ∎



##### Lemma 2  
If the mapping `f` is well defined, the functional graph built from `f`
has exactly one directed cycle in each connected component.

**Proof.**  
Every vertex of `U` has out‑degree 1, all other vertices have out‑degree 0.
Starting from any vertex and following the unique outgoing edge we must
eventually repeat a vertex; the first repeated vertex closes a directed
cycle. Because every vertex has at most one outgoing edge, no other
cycle can exist in the same weakly connected component. ∎



##### Lemma 3  
For a component `K` let `U_K = U ∩ K`.  
The minimal number of operations needed to transform the letters of
`U_K` into the required ones is

* `|U_K|`                if the root of `K` is not in `U`,
* `|U_K| - 1`            if the root of `K` is a fixed point,
* `|U_K| + 1`            if `K` contains a cycle of length at least 2.

**Proof.**  

*Tree, external sink.*  
The root (a letter not appearing in `S`) never occurs in the string,
so it cannot be used as a source of an operation.
Every vertex of `U_K` must disappear, each operation can eliminate at
most one distinct letter, therefore at least `|U_K|` operations are
necessary. Performing them leaf‑by‑leaf (replace a leaf by its parent)
achieves exactly `|U_K|` operations, thus it is optimal.

*Tree, fixed point root.*  
The root stays unchanged, all other `|U_K|-1` letters have to disappear.
Again each operation removes at most one distinct letter, so at least
`|U_K|-1` operations are required. The leaf‑by‑leaf procedure uses exactly
`|U_K|-1` operations, therefore it is optimal.

*Cycle of length `k ≥ 2`.*  
No vertex of the component is a sink, thus at least one operation must
introduce a temporary letter that is not in the component, otherwise the
letters would stay inside the cycle forever.
Using one such temporary the standard construction needs `k+1` operations,
hence the cost is at least `k+1 = |U_K|+1`. The construction shows that
`|U_K|+1` operations are sufficient, proving optimality. ∎



##### Lemma 4  
Let  

* `C` – number of components that contain a cycle of length ≥ 2,
* `f` – number of fixed points in `U`,
* `|U|` – number of different letters in `S`.

Then the sum of the optimal costs of all components equals  
`|U| - f + C`.

**Proof.**  
Split every component into the three cases of Lemma&nbsp;3.

* external‑sink tree contributes `|U_K|`,
* fixed‑point tree contributes `|U_K|-1`,
* cycle contributes `|U_K|+1`.

Summation over all components gives

```
Σ|U_K|  - (number of fixed‑point components) + (number of cycle components)
```

Every fixed point is a fixed‑point component consisting of a single vertex,
hence the number of fixed‑point components equals `f`.  
Every cycle component is counted once, therefore the second term is `C`.  
All vertices of `U` belong to exactly one component, thus `Σ|U_K| = |U|`. ∎



##### Lemma 5  
Let `L = U ∪ (letters appearing in T)`.  
Let `free = 26 - |L|`.  
If `C ≤ free` the minimal number of operations is `|U| - f + C`.  
If `C > free` it is `|U| - f + C + (C - free)`.

**Proof.**  
Only the `C` cycle components need a temporary letter.
There are `free` letters that never appear in `S` nor in `T`; they can be
used as temporaries without any side effect.
If `C ≤ free` we give each cycle a distinct free temporary, no extra
operation is necessary, the total cost is exactly the sum from Lemma 4.

If `C > free` we still use all `free` free temporaries, the remaining
`C - free` cycles must borrow a letter from `L`.  
A borrowed letter appears somewhere in the current string, therefore after
the cycle is resolved we have to restore that letter to its correct
value – this needs **one** additional operation per such cycle.
Thus the total minimal cost is the sum from Lemma 4 plus `C - free`. ∎



##### Lemma 6  
The algorithm described in Sections&nbsp;4 and&nbsp;5 computes the
values `|U|`, `f`, `C`, `|L|` correctly.

**Proof.**  

*`|U|`* – by counting distinct letters of `S`.  

*`f`* – a vertex `a∈U` is a fixed point exactly when `f(a)=a`; the
algorithm checks this condition for every `a∈U`.  

*`|L|`* – the union of letters of `S` and `T` is built by a boolean
array, its size is counted directly.  

*`C`* – the DFS walks along the unique outgoing edges.
Whenever it meets a vertex already present in the current path, a directed
cycle is found. The cycle length is the distance between the two
occurrences; it is at least 2 precisely when the component is not a
single self‑loop. The algorithm increments `C` exactly in this case.
Every cycle belongs to a unique component, and the algorithm marks all
vertices of that component as visited, therefore each cycle is counted
once and only once. ∎



##### Lemma 7  
The number printed by the algorithm equals the minimal possible number
of operations, or `-1` if the transformation is impossible.

**Proof.**  
If Lemma 1 detects a conflict, the answer is `-1`, which is correct.  
Otherwise the mapping `f` is well defined.  
By Lemma 6 the algorithm obtains the exact values `|U|`, `f`, `C`,
`|L|`.  
Lemma 5 shows that with these values the minimal number of operations is

```
|U| - f + C + max(0, C - (26 - |L|))
```

which is exactly what the algorithm outputs. ∎



##### Theorem  
The program always prints  

* `-1` if and only if it is impossible to make `S` equal to `T`,
* otherwise the minimum number of allowed operations.

**Proof.**  
Directly from Lemma 1 (impossibility) and Lemma 7 (optimality). ∎



--------------------------------------------------------------------

#### 6.   Complexity Analysis

*Building the mapping* – `O(N)`  
*All other work* – at most 26 vertices, therefore `O(26²)` (constant).  

Memory consumption – `O(26)` for the arrays.

Both limits easily satisfy the constraints (`N ≤ 2·10⁵`).

--------------------------------------------------------------------

#### 7.   Reference Implementation  (Python 3)

```python
import sys

def solve() -> None:
    input = sys.stdin.readline
    N_line = input()
    if not N_line:
        return
    N = int(N_line)
    S = input().strip()
    T = input().strip()

    # target[a] = letter that a has to become (only for a in S)
    target = [-1] * 26
    for i in range(N):
        a = ord(S[i]) - 97
        b = ord(T[i]) - 97
        if target[a] == -1:
            target[a] = b
        elif target[a] != b:
            print(-1)
            return

    # letters that appear in S
    inS = [False] * 26
    for ch in S:
        inS[ord(ch) - 97] = True

    # letters that appear in S or in T
    inL = [False] * 26
    for ch in S:
        inL[ord(ch) - 97] = True
    for ch in T:
        inL[ord(ch) - 97] = True

    U_size = sum(inS)                 # |U|
    f = 0
    for a in range(26):
        if inS[a] and target[a] == a:
            f += 1                    # fixed points

    # count cycles of length >= 2
    visited = [False] * 26
    C = 0
    for start in range(26):
        if not inS[start] or visited[start]:
            continue
        path = []
        pos = {}
        cur = start
        while True:
            if not inS[cur]:                 # reached a sink
                for v in path:
                    visited[v] = True
                break
            if visited[cur]:
                for v in path:
                    visited[v] = True
                break
            if cur in pos:                    # found a cycle
                idx = pos[cur]
                cycle_len = len(path) - idx
                if cycle_len >= 2:
                    C += 1
                for v in path:
                    visited[v] = True
                break
            pos[cur] = len(path)
            path.append(cur)
            cur = target[cur]
        # loop always breaks inside, no extra handling needed

    L_size = sum(inL)                 # |L|
    free = 26 - L_size
    extra = max(0, C - free)
    ans = U_size - f + C + extra
    print(ans)


if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required input‑output format.

## worker: (Omitted because task is complete.)
The provided solution follows the classic analysis for this AtCoder problem (ABC285 Ex or similar).  
Key steps:  

1. **Feasibility check** – each letter in `S` must map to a single target letter; otherwise answer is `-1`.  
2. **Functional graph** on 26 vertices: edges are `a → f(a)`. Each component is either a tree rooted at an external sink, a tree rooted at a fixed point, or a directed cycle of length ≥ 2.  
3. **Cost per component** (from Lemma 3): external sink → `|Ucomp|`, fixed point → `|Ucomp|−1`, cycle → `|Ucomp|+1`.  
4. **Total base cost** = `|U| − f + C` where `f` = number of fixed points, `C` = number of cycles of length ≥ 2.  
5. **Temporary letters**: only the `C` cycles need a temporary. Free temporaries are letters not in `L = U ∪ (letters in T)`. If `C` exceeds the number of free temporaries, each missing temporary adds one extra operation.  
6. The algorithm computes `|U|`, `f`, `C`, `|L|` by a simple DFS on the tiny 26‑vertex graph, then outputs `|U| − f + C + max(0, C − (26−|L|))`.  

All steps are `O(N)` time (due to reading the strings) and `O(1)` extra memory (constant arrays of size 26). The solution is proven correct in the detailed reasoning above.
