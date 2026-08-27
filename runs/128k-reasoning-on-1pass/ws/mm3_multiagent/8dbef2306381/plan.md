**Solution Explanation**

For every square `x` we can move to `x+i` (`A ≤ i ≤ B`) if the destination is not
a bad square.
All bad squares are given as `M` disjoint intervals  
`(L₁,R₁) , … , (L_M,R_M)`.  
`N ≤ 10¹²` but `M ≤ 2·10⁴` and `A,B ≤ 20`.

The whole line is split into

```
safe interval 0 : [ 1 , L1-1 ]
bad  interval 0 : [ L1 , R1 ]
safe interval 1 : [ R1+1 , L2-1 ]
bad  interval 1 : [ L2 , R2 ]
                …
safe interval M : [ RM+1 , N ]
```

Only forward moves are allowed, therefore we can treat the walk from the
leftmost safe square to the rightmost one.



--------------------------------------------------------------------

#### 1.   A DP for one safe step  

For a *safe* square we only have to know which of the last `B` squares are
reachable – all older information is irrelevant.
A state is a bit mask of length `B`

```
bit i (0 ≤ i < B)  = 1  ⇔  current square – i is reachable
```

`cur_mask` is the state **after** the already processed square `pos`.

The next square is also safe, therefore

```
new_reachable =  (cur_mask >> (A-1))  has a 1 in its lowest (B-A+1) bits
new_mask      = ((cur_mask << 1) & all_bits)  |  new_reachable
```

`all_bits = (1<<B)-1`.  
The operation is completely deterministic – a functional graph on at most
`2^B ( ≤ 1 048 576 )` vertices.

--------------------------------------------------------------------

#### 2.   Bad squares  

A bad square can never be reached, consequently

```
new_reachable = 0
new_mask      = (cur_mask << 1) & all_bits          (the LSB becomes 0)
```

Processing a whole block of `len` consecutive bad squares is just a left
shift by `len`.  
If `len ≥ B` the shift pushes every bit out, the mask becomes `0`.

--------------------------------------------------------------------

#### 3.   Jumping many safe steps at once  

The transition for a safe square is a **function** `f(mask)`.
`f` can be composed with itself.
With binary lifting we can apply `2^k` steps in one table lookup.

```
nxt[0][mask] = f(mask)                     (one step)
nxt[k][mask] = nxt[k-1][ nxt[k-1][mask] ]   (2^k steps)
```

`B ≤ 20  →  at most 1 048 576 states`.  
`log₂(N) ≤ 40`, therefore we need only 40 tables.
The total memory is  
`40 · 2^B · 4 bytes  ≤ 160 MiB` – easily inside usual limits.

Applying `t` safe steps (`t ≤ N`) :

```
while t>0:
        if t&1:   cur_mask = nxt[bit][cur_mask]
        t >>= 1
        bit += 1
```

Only `O(log t)` operations (`≤ 40`).

--------------------------------------------------------------------

#### 4.   Whole walk  

```
cur_pos  = 1                     # already processed square 1
cur_mask = 1                     # only square 1 is reachable (bit 0 = 1)

process the intervals in order
    safe interval [L,R] :
        steps = R - cur_pos          # how many new safe squares
        cur_mask = apply_safe_steps(cur_mask, steps)
        cur_pos  = R
        if cur_mask == 0 and cur_pos != N :   # no reachable square any more
                answer = "No"
                stop

    bad interval [L,R] (length = R-L+1) :
        if length >= B :   cur_mask = 0
        else               cur_mask = (cur_mask << length) & all_bits
        cur_pos = R
        if cur_mask == 0 and cur_pos != N :
                answer = "No"
                stop
```

If the loop finishes, `cur_pos == N`.  
`cur_mask & 1` tells whether the last square `N` is reachable.

The whole algorithm works in  

```
O( (M+1) · log N )   ≤   2·10⁴ · 40   steps
```

plus the pre‑computation of the transition tables  
`O( 2^B · log N )   ≤   4·10⁷` elementary operations – well within the limits.



--------------------------------------------------------------------

#### 5.   Correctness Proof  

We prove that the algorithm prints “Yes” iff square `N` can be reached.

---

##### Lemma 1  
For a safe square the recurrence  

```
new_mask = ((old_mask << 1) & all_bits) |
           (  ((old_mask >> (A-1)) & ((1<<(B-A+1))-1)) != 0 )
```

exactly describes the set of reachable squares after the move.

**Proof.**  
`old_mask` contains the reachability of the last `B` squares before the new
square `x+1`.  
A square `x+1` is reachable iff there exists a previous reachable square
`x+1-i` with `A ≤ i ≤ B`, i.e. a reachable square whose distance from the
new one is between `A` and `B`.  
In the mask these are precisely the bits with indices `A-1 … B-1`.  
`((old_mask >> (A-1)) & … ) != 0` is true exactly when one of those bits
is `1`.  The left shift moves every old bit one step forward, the new
bit (`0` or `1`) is inserted as the new least‑significant bit.
∎



##### Lemma 2  
Processing `len` consecutive bad squares changes the mask to  

```
 (old_mask << len) & all_bits      (if len < B)
 0                                  (if len ≥ B)
```

**Proof.**  
For one bad square the transition is `new_mask = (old_mask << 1) & all_bits`
(the new LSB is forced to `0`).  
Applying it `len` times is a left shift by `len`.  
If `len ≥ B` all bits are shifted out, the result is `0`. ∎



##### Lemma 3  
For every integer `t ≥ 0` the function `apply_safe_steps(mask, t)` returns
the state after exactly `t` safe steps starting from `mask`.

**Proof.**  
`nxt[0][mask] = f(mask)` is the state after one safe step
(Lemma&nbsp;1).  
`nxt[k][mask] = nxt[k‑1][ nxt[k‑1][mask] ]` composes two functions of
`2^{k-1}` steps, therefore it represents `2^k` steps.
Binary lifting writes `t` as a sum of distinct powers of two;
the algorithm follows the corresponding pre‑computed powers,
which is exactly the functional composition of `t` applications of `f`. ∎



##### Lemma 4  
During the execution `cur_mask` always equals the set of reachable squares
among the last `B` positions **ending at** `cur_pos`.

**Proof by induction over the processed interval length.**

*Base.*  
Before the loop we have processed only square 1.
`cur_mask = 1` (binary `…0001`) – only square 1 (distance 0) is reachable.
Induction hypothesis holds.

*Step – safe interval.*  
Let the interval have length `steps = R-cur_pos`.  
`apply_safe_steps` (Lemma&nbsp;3) returns the state after exactly `steps`
safe moves, i.e. after processing all squares of the interval.
Thus the invariant holds for the new `cur_pos = R`.

*Step – bad interval.*  
By Lemma&nbsp;2 the transformation performed on the mask is exactly the
effect of moving over all bad squares of the interval.
Consequently the new mask again describes the reachable squares among the
last `B` positions (now ending at the new `cur_pos`).

Thus the invariant is preserved. ∎



##### Lemma 5  
If after processing a bad interval the mask becomes `0`, then no later
square can be reached.

**Proof.**  
`0` means that none of the last `B` squares is reachable.
Any future move can only start from a reachable square,
hence it is impossible to reach any square further to the right. ∎



##### Lemma 6  
When the algorithm finishes, `cur_mask & 1 = 1`  **iff** square `N` is
reachable.

**Proof.**  
At the end `cur_pos = N`.  
By Lemma&nbsp;4 bit 0 of `cur_mask` is `1` exactly when the square `N`
belongs to the reachable set of the last `B` positions, i.e. when it is
reachable. ∎



##### Lemma 7  
If the algorithm prints “No” then `N` is not reachable.

**Proof.**  
The algorithm prints “No” only in two situations

* after a safe or a bad interval the mask became `0` while `cur_pos < N`.  
  By Lemma&nbsp;5 no later square can be reached, in particular `N`.

* after the whole walk `cur_mask & 1 = 0`.  
  By Lemma&nbsp;6 square `N` is not reachable. ∎



##### Lemma 8  
If the algorithm prints “Yes” then `N` is reachable.

**Proof.**  
The algorithm prints “Yes” only when the whole walk is processed and
`cur_mask & 1 = 1`.  
By Lemma&nbsp;6 this is equivalent to `N` being reachable. ∎



##### Theorem  
The program outputs “Yes” **iff** it is possible to reach square `N`
from square 1 by the allowed moves.

**Proof.**  
*If* the program outputs “Yes”, Lemma&nbsp;8 gives reachability.  
*Only if* the program outputs “No”, Lemma&nbsp;7 shows that `N` cannot be
reached. ∎



--------------------------------------------------------------------

#### 6.   Complexity Analysis  

*Pre‑computation* (`B ≤ 20`)

```
states  = 2^B  ≤ 1 048 576
levels  = ⌈log₂ N⌉ ≤ 40
time    :  O( states · levels )   ≤ 4·10⁷ elementary operations
memory  :  O( states · levels )   ≤ 160 MiB   (array of unsigned int)
```

*Processing the intervals* (`M ≤ 2·10⁴`)

```
time per safe interval :  O(log N)   (binary lifting)
time per bad  interval :  O(1)       (simple shift)
total time              :  O( (M+1)·log N ) ≤ 8·10⁵
memory for intervals    :  O(M)
```

Both time and memory easily satisfy the limits.



--------------------------------------------------------------------

#### 7.   Reference Implementation  (Python 3)

```python
import sys
from array import array

def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    it = iter(data)
    N = next(it)
    M = next(it)
    A = next(it)
    B = next(it)

    bad = [(next(it), next(it)) for _ in range(M)]

    # ----- build the alternating list of safe / bad intervals -----
    intervals = []                # each element: ('safe', L, R) or ('bad', L, R)
    prev_end = 0
    for L, R in bad:
        safe_start = prev_end + 1
        safe_end = L - 1
        if safe_start <= safe_end:
            intervals.append(('safe', safe_start, safe_end))
        intervals.append(('bad', L, R))
        prev_end = R
    # final safe part
    safe_start = prev_end + 1
    safe_end = N
    if safe_start <= safe_end:
        intervals.append(('safe', safe_start, safe_end))

    # ----- pre‑compute the transition tables (binary lifting) -----
    ALL_BITS = (1 << B) - 1
    RANGE_MASK = (1 << (B - A + 1)) - 1          # bits (A‑1)…(B‑1)

    # one safe step
    def trans_good(mask: int) -> int:
        # new reachable if any of the bits A-1 … B-1 is set
        new_bit = 1 if ((mask >> (A - 1)) & RANGE_MASK) else 0
        return ((mask << 1) & ALL_BITS) | new_bit

    LOG = (N).bit_length()          # ≤ 40
    nxt = []                        # nxt[k][mask] = state after 2^k safe steps

    # level 0
    nxt0 = array('I', (trans_good(m) for m in range(1 << B)))
    nxt.append(nxt0)

    # higher levels
    for k in range(1, LOG):
        prev = nxt[-1]
        cur = array('I', [0]) * (1 << B)
        p = prev
        for m in range(1 << B):
            cur[m] = p[p[m]]
        nxt.append(cur)

    # apply t safe steps using binary lifting
    def apply_good_steps(state: int, steps: int) -> int:
        bit = 0
        while steps:
            if steps & 1:
                state = nxt[bit][state]
            steps >>= 1
            bit += 1
        return state

    # ----- walk through the intervals -----
    cur_pos = 1               # already processed square 1
    cur_mask = 1              # only square 1 is reachable (bit0 = 1)

    for typ, L, R in intervals:
        if typ == 'safe':
            steps = R - cur_pos
            if steps > 0:
                cur_mask = apply_good_steps(cur_mask, steps)
                cur_pos = R
                if cur_mask == 0 and cur_pos != N:
                    print('No')
                    return
        else:  # bad interval
            length = R - L + 1
            if length >= B:
                cur_mask = 0
            else:
                cur_mask = (cur_mask << length) & ALL_BITS
            cur_pos = R
            if cur_mask == 0 and cur_pos != N:
                print('No')
                return

    # after the loop cur_pos == N
    print('Yes' if (cur_mask & 1) else 'No')


if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required input and output format.