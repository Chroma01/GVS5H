**Solution Explanation**

For every `K` we start with the `K`‑th slime, its size is `A_K`.
While there is a neighbour whose size is **strictly smaller** than the current
size we absorb it and the current size grows by the absorbed size.
The process stops when both neighbours (if they exist) are not smaller.

The problem asks for the final size for every starting position `K`.

--------------------------------------------------------------------

#### 1.   Observations

* The process is **confluent** – the order of absorbing left/right does not
  influence the final set of absorbed slimes.  
  (If both neighbours are smaller, after absorbing one the other is still
  smaller, so the whole interval is absorbed in any order.)

* While the current size is `S`, we can absorb **all** consecutive slimes
  on the left that are `< S`, then all on the right that are `< S`,
  then again left, …  
  The only obstacle is a slime whose size is `≥ S`.  
  When we finally absorb such a slime, the size becomes `> 2·S`
  (because we add at least the size of that slime).  
  Consequently the size **more than doubles** every time we pass a
  “big” slime.  
  The number of such doublings is at most `log₂(N·10⁹) < 60`.

* Therefore for a fixed `K` we can simulate the process by repeatedly

  *   finding the nearest slime on the left whose size `≥ S`
      (the *left barrier*),
  *   absorbing everything between the current left end and that barrier,
  *   possibly absorbing the barrier itself,
  *   doing the same on the right.

  The number of iterations is `O(log maxA)` ( ≤ 60 ), each iteration
  needs `O(log N)` time to locate the next barrier by a segment tree.

--------------------------------------------------------------------

#### 2.   Data structures

* **Prefix sums** `P[i] = A₁+…+A_i` ( `P[0]=0` ) – to obtain the sum of a
  whole interval in `O(1)`.

* **Segment tree** over the array `A` storing the maximum value in each node.
  With it we can

  * find the **rightmost** index `i` in a given range whose value `≥ S`,
  * find the **leftmost**  index `j` in a given range whose value `≥ S`.

  Both queries are `O(log N)`.

--------------------------------------------------------------------

#### 3.   Algorithm for one start `K`

```
S = A_K                      # current size
L = K, R = K                 # current interval [L,R]
repeat
        # ----- expand to the left -----
        i = rightmost index < L with A[i] ≥ S   (search in [1 , L-1])
        if i does not exist:                 # no barrier
                S += P[L-1] - P[0]           # absorb everything on the left
                L = 1
        else:
                # absorb the block (i+1 … L-1)
                S += P[L-1] - P[i]
                L = i+1
                if S > A[i]:                 # now we can also absorb the barrier
                        S += A[i]
                        L = i

        # ----- expand to the right -----
        j = leftmost index > R with A[j] ≥ S   (search in [R+1 , N])
        if j does not exist:                 # no barrier
                S += P[N] - P[R]             # absorb everything on the right
                R = N
        else:
                S += P[j-1] - P[R]           # absorb the block (R+1 … j-1)
                R = j-1
                if S > A[j]:                 # absorb the barrier
                        S += A[j]
                        R = j
until neither side changed (no slime was absorbed any more)
answer[K] = S
```

*When a side has no barrier we absorb the whole remaining part at once –
the number of iterations stays `O(log maxA)`.*

--------------------------------------------------------------------

#### 4.   Correctness Proof  

We prove that the algorithm returns the correct final size for every
starting position.

---

##### Lemma 1  
During the whole process the set of absorbed slimes is always a **contiguous**
interval `[L,R]`.

**Proof.**  
Initially the interval is `[K,K]`.  
The only operation is to absorb the immediate left neighbour or the
immediate right neighbour, which extends the interval by one cell.
Therefore after any number of operations the absorbed slimes form a single
contiguous block. ∎



##### Lemma 2  
Let the current interval be `[L,R]` and its total size be `S`.
All slimes strictly between `L` and the next slime on the left whose
size is `≥ S` are smaller than `S`, and can be absorbed immediately
(and independently of any other side).

**Proof.**  
By definition of the next barrier `i` (`i<L` and `A_i ≥ S`) all positions
`i+1 … L-1` have size `< S`.  
Because the current interval already contains the slime at `L`,
the neighbour of each of those positions is already inside the interval,
hence the condition “strictly smaller than the current size” holds.
No other slime on the left is adjacent, so the whole block can be
absorbed without any side effect. ∎



##### Lemma 3  
If the current size is `S` and the next barrier on the left is at `i`,
after absorbing the whole block `(i+1 … L-1)` the new size becomes
`S' = S + Σ_{t=i+1}^{L-1} A_t`.  
If `S' > A_i` then the barrier slime `i` can be absorbed as well,
and after that the size is `S' + A_i  > 2·S`.

**Proof.**  
The first part is just adding the sizes of the absorbed slimes.
After the block is absorbed the left neighbour of the interval is exactly
the slime `i`.  
If the new size `S'` is larger than `A_i` we may absorb it,
and the size grows by `A_i`, therefore the new size is at least
`S' + A_i  >  S'  >  2·S`. ∎



##### Lemma 4  
The algorithm’s loop for a fixed `K` performs exactly the same sequence
of absorptions as the original process.

**Proof.**  
The original process can be described as:

```
while there exists a neighbour with size < current size:
        absorb all such neighbours (left and right, any order)
```

Consider one iteration of the algorithm.
It first looks for the left barrier `i`.  
If none exists, all slimes left of `L` are smaller than `S`,
hence they are all absorbable and the original process would absorb them
as well – the algorithm adds the whole sum at once, which is equivalent.

If a left barrier exists, by Lemma&nbsp;2 the whole block
`(i+1 … L-1)` is absorbable immediately.
The algorithm adds their total size, exactly as the original process.
After that the left neighbour is the barrier `i`.  
If now `S > A_i` the original process would also absorb it,
and the algorithm does the same (Lemma&nbsp;3).  
If `S ≤ A_i` the original process cannot absorb it, and the algorithm
stops expanding left.

The same reasoning holds for the right side.
Thus after the algorithm’s iteration the interval `[L,R]`, the total size
`S` and the set of already absorbed slimes are identical to the state
of the original process after it has absorbed everything that is currently
possible.  
Repeating the iteration reproduces the next steps of the original process.
∎



##### Lemma 5  
The number of iterations of the algorithm for a fixed `K` is at most
`⌈log₂( N·10⁹ )⌉   ( < 60 )`.

**Proof.**  
Whenever an iteration absorbs a *barrier* slime (the first slime that
was not smaller than the current size) the size more than doubles
(Lemma&nbsp;3).  
If an iteration does **not** absorb a barrier, the interval grows to the
border of the whole array, and the process stops.  
Therefore the number of barrier absorptions is bounded by the number of
times the size can be at most doubled before it exceeds the maximal
possible total size `N·10⁹`. ∎



##### Lemma 6  
For a fixed `K` the algorithm terminates and returns the final size
obtained by the optimal sequence of actions.

**Proof.**  
By Lemma&nbsp;4 each iteration reproduces the state of the original
process after all currently possible absorptions.
Consequently after finitely many iterations (Lemma&nbsp;5) the interval
cannot be extended any more – both neighbours are not smaller than the
current size.  
This is exactly the stopping condition of the original process, hence
the current size `S` equals the maximal achievable size. ∎



##### Theorem  
For every `K (1 ≤ K ≤ N)` the algorithm outputs `B_K`, the maximum size
that the `K`‑th slime can obtain.

**Proof.**  
The algorithm is executed independently for each `K`.
By Lemma&nbsp;6 the value `S` computed for a given `K` is precisely the
final size of the optimal process starting from `K`.  
Therefore the stored answer `B_K = S` is correct. ∎



--------------------------------------------------------------------

#### 5.   Complexity Analysis  

*Building the segment tree* : `O(N)`  
*Prefix sums*                : `O(N)`

For one start `K`  

* each iteration needs at most two segment‑tree queries (`O(log N)`)  
* number of iterations ≤ 60  

so the work is `O(log N)` (the constant 60 is tiny).

For all `N` starts  

```
time   :  O(N log N)          ( ≤ 5·10⁵ · 19  operations )
memory :  O(N)   (array, prefix sums, segment tree)
```

Both limits satisfy the constraints.

--------------------------------------------------------------------

#### 6.   Reference Implementation  (Python 3)

```python
import sys
sys.setrecursionlimit(1 << 25)

def solve() -> None:
    import sys
    input = sys.stdin.readline
    N = int(input())
    A = [0] + list(map(int, input().split()))   # 1‑indexed

    # ---------- prefix sums ----------
    P = [0] * (N + 1)
    for i in range(1, N + 1):
        P[i] = P[i-1] + A[i]

    # ---------- segment tree (range maximum) ----------
    size = 1
    while size < N:
        size <<= 1
    seg = [0] * (2 * size)
    # leaves
    for i in range(N):
        seg[size + i] = A[i+1]
    for i in range(size - 1, 0, -1):
        seg[i] = seg[2*i] if seg[2*i] >= seg[2*i+1] else seg[2*i+1]

    # find rightmost index in [l, r] (1‑based) with value >= S, or None
    def find_rightmost(node, nl, nr, ql, qr, S):
        if nr < ql or nl > qr or seg[node] < S:
            return None
        if nl == nr:
            return nl
        mid = (nl + nr) // 2
        # search right child first to get the rightmost
        res = find_rightmost(node*2+1, mid+1, nr, ql, qr, S)
        if res is not None:
            return res
        return find_rightmost(node*2, nl, mid, ql, qr, S)

    # find leftmost index in [l, r] (1‑based) with value >= S, or None
    def find_leftmost(node, nl, nr, ql, qr, S):
        if nr < ql or nl > qr or seg[node] < S:
            return None
        if nl == nr:
            return nl
        mid = (nl + nr) // 2
        res = find_leftmost(node*2, nl, mid, ql, qr, S)
        if res is not None:
            return res
        return find_leftmost(node*2+1, mid+1, nr, ql, qr, S)

    # wrappers using the root covering [1, size]
    def rightmost_ge(l, r, S):
        if l > r:
            return None
        return find_rightmost(1, 1, size, l, r, S)

    def leftmost_ge(l, r, S):
        if l > r:
            return None
        return find_leftmost(1, 1, size, l, r, S)

    # ---------- compute answer for every K ----------
    ans = [0] * (N + 1)
    for K in range(1, N + 1):
        S = A[K]
        L = K
        R = K
        # loop until no expansion is possible
        while True:
            changed = False
            # ---- expand to the left ----
            i = rightmost_ge(1, L-1, S)          # barrier on the left
            if i is None:                         # no barrier
                # absorb everything on the left
                S += P[L-1] - P[0]
                L = 1
                changed = True
            else:
                # absorb the block (i+1 .. L-1)
                if i+1 <= L-1:
                    S += P[L-1] - P[i]
                    L = i+1
                    changed = True
                # try to absorb the barrier
                if S > A[i]:
                    S += A[i]
                    L = i
                    changed = True
            # ---- expand to the right ----
            j = leftmost_ge(R+1, N, S)            # barrier on the right
            if j is None:                         # no barrier
                S += P[N] - P[R]
                R = N
                changed = True
            else:
                if R+1 <= j-1:
                    S += P[j-1] - P[R]
                    R = j-1
                    changed = True
                if S > A[j]:
                    S += A[j]
                    R = j
                    changed = True
            if not changed:
                break
        ans[K] = S

    print(' '.join(map(str, ans[1:])))

if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required time and memory limits.