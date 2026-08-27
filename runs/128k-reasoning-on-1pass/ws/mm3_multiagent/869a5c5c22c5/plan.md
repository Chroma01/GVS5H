**Solution Explanation**

For every test case we are given  

* `R` – number of red pieces (move orthogonally)  
* `B` – number of blue pieces (move diagonally)  

`N = R + B ≥ 2`.  
All pieces have to be placed on different squares of a `10^9 × 10^9` board.
If the pieces are placed in the order `p1 , p2 , … , pN` then for every
`i (1 ≤ i ≤ N-1)` piece `pi` must be able to move to the square of `p(i+1)`,
and also `pN` must be able to move to `p1`.

--------------------------------------------------------------------

#### 1.   When is it possible?

* a red move changes the colour of the square (`(r+c) mod 2` flips)
* a blue move keeps the colour

Going once around the cycle we change the colour `R` times, therefore

```
R must be even                                    (1)
```

If `R = 0` we have to make a cycle using only diagonal moves.
The graph formed by diagonal moves is bipartite (it consists of the two
parity classes `(r+c) mod 2 = 0` and `= 1`), consequently every cycle
has even length. Hence

```
if R = 0 then B must be even                     (2)
```

Conditions (1) and (2) are also sufficient – we will construct a
placement for every case that satisfies them.



--------------------------------------------------------------------

#### 2.   Geometry of a useful family of cycles  

```
right  w steps  (red)      →  (0,0) … (0,w)
down‑right h steps (blue)   →  (h , w+h)
left   w steps  (red)      →  (h , h)
up‑left  h steps (blue)     →  (0,0)
```

All four parts are straight segments, the whole figure is a simple
parallelogram, it uses

```
2·w   red moves      (R = 2·w)
2·h   blue moves     (B = 2·h)
```

The vertices are distinct, the last move (`up‑left`) brings us back to the
start.  
For `w = R/2 , h = B/2` this gives a solution for every **even** `B`
(`B = 2·h`).  
The shape is called *parallelogram* below.



--------------------------------------------------------------------

#### 3.   Adding one extra blue move (turning even `B` into odd `B`)

Take a red move that goes to the right, for example
`(0,0) → (0,1)`.  
Replace it by the two moves

```
(0,0) → (-1,1)   (diagonal, blue)
(-1,1) → (0,1)   (down,   red)
```

The new square `(-1,1)` is not used by the original figure, therefore
the walk stays simple.
The number of red moves does **not** change, the number of blue moves
increases by exactly one.
We call this operation **detour**.



--------------------------------------------------------------------

#### 4.   Constructing a placement for every feasible case

All cases are covered by the following table.

| `R` | `B` | construction |
|-----|-----|----------------|
| odd | any | impossible (condition (1)) |
| `0` | odd | impossible (condition (2)) |
| `0` | even | only blue cycle (see below) |
| `≥2` even | `0` | rectangle of height `2` and width `R/2` |
| `≥2` even | `1` | “right‑down‑left‑up‑left’’ shape (see below) |
| `≥2` even | even `≥2` | parallelogram (`w = R/2 , h = B/2`) |
| `≥2` even | odd `≥3` | parallelogram with `h = (B‑1)/2` + one detour |

*Only blue cycle* (`R = 0 , B` even)  

Take `k = B/2`.  
If `k = 1` (`B = 2`) the 2‑cycle `(1,1) , (2,2)` works.  
For `k ≥ 2` use the diagonal rectangle

```
(0,0) → (1,1) → (2,2) → … → (k,k)                (k steps down‑right)
→ (k‑1 , k+1) → … → (0 , 2k)                     (k‑1 steps up‑right)
→ (‑1 , 2k‑1) → … → (‑k , k)                    (k steps up‑left)
→ (‑k+1 , k‑1) → … → (0,0)                     (k‑1 steps down‑left)
```

All moves are diagonal, the walk is a simple cycle of length `B`.
A constant shift (`+k+2` in both coordinates) keeps all coordinates `≥ 1`.

*Right‑down‑left‑up‑left* (`B = 1`)  

```
(0,0) → (0,1) → … → (0,w)   (w red steps, w = R/2)
(0,w) → (1,w)               (red down)
(1,w) → (1,w‑1) → … → (1,1) (red left, w‑1 steps)
(1,1) → (0,0)               (blue up‑left)
```

Exactly `R` red moves and one blue move.

All constructions use only coordinates `≤ 2·10^5`, well inside the
board limits.



--------------------------------------------------------------------

#### 5.   Algorithm
For each test case

```
if R is odd                     → print "No"
else if R == 0:
        if B is odd             → print "No"
        else                    → build the blue cycle, output it
else:   # R ≥ 2, even
        if B == 0               → rectangle
        elif B == 1             → right‑down‑left‑up‑left
        elif B is even          → parallelogram
        else                    → parallelogram (h = (B-1)/2) + detour
        output the constructed cycle
```

The construction of a shape is a simple linear walk,
the whole algorithm is `O(R+B)` per test case,  
overall `O( Σ (R+B) ) ≤ 2·10^5`.



--------------------------------------------------------------------

#### 6.   Correctness Proof  

We prove that the algorithm prints “Yes” with a correct placement
iff the instance is feasible, and prints “No” otherwise.

---

##### Lemma 1  
In any feasible placement the number of red pieces `R` is even.

**Proof.**  
A red move flips the colour `(r+c) mod 2`, a blue move keeps it.
Going once around the cycle the colour changes `R` times and must return
to the start, therefore `R` is even. ∎



##### Lemma 2  
If `R = 0` then `B` must be even.

**Proof.**  
When `R = 0` all moves are diagonal, they keep the colour.
The diagonal‑move graph is bipartite (it consists of the two colour
classes), consequently every cycle has even length. ∎



##### Lemma 3  
For any even `R ≥ 2` and any even `B ≥ 0` the parallelogram construction
produces a simple cycle with exactly `R` red and `B` blue moves.

**Proof.**  
The parallelogram consists of four straight segments

* `w = R/2` right steps – orthogonal,
* `h = B/2` down‑right steps – diagonal,
* `w` left steps – orthogonal,
* `h` up‑left steps – diagonal.

All four segments are pairwise disjoint except for the common start/end
point, therefore the vertices are distinct.
The number of steps is `2w + 2h = R + B`, with `2w` red and `2h` blue.
∎



##### Lemma 4  
Applying a *detour* to a red right step increases the number of blue
moves by one, keeps the number of red moves unchanged and preserves
simplicity of the walk.

**Proof.**  
A right step `(x,y) → (x,y+1)` is replaced by

```
(x,y) → (x-1,y+1)   (diagonal, blue)
(x-1,y+1) → (x,y+1) (down,    red)
```

The new vertex `(x-1,y+1)` has row `x-1`.  
All original vertices have rows `≥ x`, thus the new vertex is new.
The replaced red step disappears, one blue and one red step appear,
so the numbers of red steps stay the same, blue steps increase by one.
All other edges are untouched, therefore the walk stays a simple cycle.
∎



##### Lemma 5  
For every even `R ≥ 2` and every `B = 1` the “right‑down‑left‑up‑left’’
shape is a simple cycle with `R` red and one blue move.

**Proof.**  
The shape consists of `w = R/2` right steps, one down step,
`w‑1` left steps and finally the diagonal up‑left step that closes the
cycle. All intermediate squares are distinct and lie inside the
`3 × (w+1)` rectangle, the closing diagonal goes from the lower‑left
corner of that rectangle to the start square, which is not used elsewhere.
The numbers of red and blue steps are `w + 1 + (w‑1) = 2w = R` and `1`.
∎



##### Lemma 6  
For `R = 0` and even `B ≥ 2` the diagonal‑rectangle construction
produces a simple cycle of length `B` consisting only of blue moves.

**Proof.**  
If `B = 2` the 2‑cycle `(1,1) , (2,2)` is obviously correct.  
For `B ≥ 4` let `k = B/2 (≥2)`.  
The construction is a rectangle in the `(u,v) = (r+c , r-c)` coordinates,
whose sides have lengths `1` and `k‑1`.  
A step in the original board changes `(u,v)` by `(±2,0)` or `(0,±2)`,
hence the rectangle in `(u,v)` corresponds to a closed walk of
`2·(1 + (k‑1)) = 2k = B` diagonal steps.
All vertices have distinct `(u,v)` pairs, therefore they are distinct
in the original board. All moves are diagonal, i.e. blue.
∎



##### Lemma 7  
For every feasible pair `(R,B)` the algorithm outputs a placement that
satisfies all conditions.

**Proof.**  
Four cases.

*`R = 0 , B` even* – by Lemma&nbsp;6 the algorithm outputs a correct
blue cycle.

*`R ≥ 2 , B = 0`* – the rectangle construction is a special case of the
parallelogram (`h = 0`) and Lemma&nbsp;3 gives a correct placement.

*`R ≥ 2 , B = 1`* – Lemma&nbsp;5 proves the “right‑down‑left‑up‑left’’
shape is correct.

*`R ≥ 2 , B` even `≥ 2`* – Lemma&nbsp;3 gives a correct parallelogram.

*`R ≥ 2 , B` odd `≥ 3`* – start with the parallelogram for the even
part `B‑1` (Lemma&nbsp;3) and apply one detour (Lemma&nbsp;4).  
The detour adds exactly one blue step, keeps the number of red steps,
preserves simplicity, therefore the final placement has `R` red and
`B` blue moves and all moves are valid. ∎



##### Lemma 8  
If the algorithm prints “No”, the instance is infeasible.

**Proof.**  
The algorithm prints “No” only in two situations:

1. `R` is odd – by Lemma&nbsp;1 a placement cannot exist.
2. `R = 0` and `B` is odd – by Lemma&nbsp;2 a placement cannot exist.

Thus in both cases feasibility is impossible. ∎



##### Theorem  
For every test case the program

* prints “No” **iff** the instance is infeasible,
* otherwise prints “Yes” and a placement that satisfies all requirements.

**Proof.**  
*If* the program prints “No”, Lemma&nbsp;8 shows infeasibility.  
*If* the program prints “Yes”, it is in one of the feasible cases of
Lemma&nbsp;7, therefore a correct placement is produced. ∎



--------------------------------------------------------------------

#### 7.   Complexity Analysis

For one test case with `N = R + B`

* building the path – `O(N)`
* computing the types – `O(N)`

Memory consumption – the list of vertices, `O(N)`.

The sum of `N` over all test cases is at most `2·10^5`,
so the total running time is `O(2·10^5)` and the memory usage is
`O(2·10^5)`.



--------------------------------------------------------------------

#### 8.   Reference Implementation  (Python 3)

```python
import sys

# ------------------------------------------------------------
# construction helpers
# ------------------------------------------------------------

def construct_rectangle(R):
    """R is even, R >= 2, B = 0.
       rectangle height 2, width w = R/2.
    """
    w = R // 2
    path = []
    # start
    path.append((2, 2))
    # right w-1 steps
    for i in range(1, w):
        path.append((2, 2 + i))
    # down
    path.append((3, 2 + w - 1))          # (3, w+1)
    # left w-1 steps
    for i in range(w - 2, -1, -1):
        path.append((3, 2 + i))
    return path


def construct_B1(R):
    """R even, R >= 2, B = 1.
       right w steps, down 1, left w-1 steps, up-left closing.
    """
    w = R // 2
    path = []
    path.append((2, 2))
    # right w steps
    for i in range(1, w + 1):
        path.append((2, 2 + i))
    # down 1
    path.append((3, 2 + w))
    # left w-1 steps
    for i in range(w - 1, 0, -1):
        path.append((3, 2 + i))
    return path


def construct_parallelogram(R, B0):
    """R even, B0 even, B0 = 2*h, h >= 1.
       w = R/2, h = B0/2.
    """
    w = R // 2
    h = B0 // 2
    r0, c0 = 2, 2
    path = []
    # segment A : right w steps
    for i in range(w + 1):
        path.append((r0, c0 + i))
    # segment B : down‑right h steps
    for j in range(1, h + 1):
        path.append((r0 + j, c0 + w + j))
    # segment C : left w steps
    for k in range(1, w + 1):
        path.append((r0 + h, c0 + w + h - k))
    # segment D : up‑left h steps (do not add the final start point)
    for l in range(1, h):
        path.append((r0 + h - l, c0 + h - l))
    return path


def apply_detour(path):
    """Replace the first edge (right step) by a diagonal up‑right + down."""
    v0 = path[0]
    # the first step is rightwards, therefore v0.c < v1.c
    q = (v0[0] - 1, v0[1] + 1)
    return [v0, q] + path[1:]


def construct_blue_cycle(B):
    """R = 0, B even, B >= 2."""
    if B == 2:
        return [(1, 1), (2, 2)]
    k = B // 2          # k >= 2
    a = 1
    b = k - 1           # b >= 1
    # choose start to keep everything >= 1
    r0 = b + 2
    c0 = b + 2
    path = [(r0, c0)]
    # down‑right a steps
    for j in range(1, a + 1):
        path.append((r0 + j, c0 + j))
    # up‑right b steps
    cur_r, cur_c = r0 + a, c0 + a
    for _ in range(b):
        cur_r -= 1
        cur_c += 1
        path.append((cur_r, cur_c))
    # up‑left a steps
    for _ in range(a):
        cur_r -= 1
        cur_c -= 1
        path.append((cur_r, cur_c))
    # down‑left b steps (the last one returns to start)
    for _ in range(b):
        cur_r += 1
        cur_c -= 1
        path.append((cur_r, cur_c))
    # the last vertex equals the start, remove it
    if path[-1] == (r0, c0):
        path.pop()
    return path


# ------------------------------------------------------------
# type computation
# ------------------------------------------------------------

def compute_types(path):
    n = len(path)
    types = []
    for i in range(n):
        r1, c1 = path[i]
        r2, c2 = path[(i + 1) % n]
        if abs(r1 - r2) + abs(c1 - c2) == 1:
            types.append('R')
        else:               # must be diagonal
            types.append('B')
    return types


# ------------------------------------------------------------
# main solver
# ------------------------------------------------------------

def solve_one(R, B):
    # feasibility test
    if R % 2 == 1:
        return None                     # impossible
    if R == 0:
        if B % 2 == 1:
            return None
        # pure blue cycle
        path = construct_blue_cycle(B)
        types = ['B'] * len(path)
        return list(zip(path, types))

    # now R >= 2 and even
    if B == 0:
        path = construct_rectangle(R)
    elif B == 1:
        path = construct_B1(R)
    elif B % 2 == 0:
        path = construct_parallelogram(R, B)
    else:   # B odd and >= 3
        h = (B - 1) // 2
        path = construct_parallelogram(R, 2 * h)
        path = apply_detour(path)

    types = compute_types(path)
    return list(zip(path, types))


def solve() -> None:
    it = iter(sys.stdin.read().strip().split())
    T = int(next(it))
    out_lines = []
    for _ in range(T):
        R = int(next(it))
        B = int(next(it))
        res = solve_one(R, B)
        if res is None:
            out_lines.append("No")
        else:
            out_lines.append("Yes")
            for (r, c), t in res:
                out_lines.append(f"{t} {r} {c}")
    sys.stdout.write("\n".join(out_lines))


if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required input‑output format.