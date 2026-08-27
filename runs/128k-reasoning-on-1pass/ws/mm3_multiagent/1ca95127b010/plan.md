**Solution Explanation**

For a string `S` ( `|S| = N` ) we may apply two operations

```
A :  00…0 11…1   →   11…1 00…0
    ^^^^^         ^^^^^
    X zeros       Y ones
```

```
B :  11…1 00…0   →   00…0 11…1
    ^^^^^         ^^^^^
    Y ones        X zeros
```

`X` and `Y` are fixed positive integers.
Both operations only change a block of `X+Y` consecutive characters,
the total number of `0` and of `1` never changes.



--------------------------------------------------------------------

#### 1.   What can move ?

* `X` consecutive `0`’s can move **to the right** across `Y` consecutive `1`’s
  (operation A).  
  The moved `0`‑block stays a block of exactly `X` zeros,
  the `1`‑block stays a block of exactly `Y` ones.

* `Y` consecutive `1`’s can move **to the left** across `X` consecutive `0`’s
  (operation B).

Therefore a block of `X` zeros (or `Y` ones) can be swapped with a neighbour
block of the opposite type – exactly the usual “swap adjacent different
items”.

A block that is **shorter** than `X` (or `Y`) can never be swapped,
because every operation needs a full block of length `X` (or `Y`).

--------------------------------------------------------------------

#### 2.   Decomposition of a string

Look at a maximal run of zeros, length `L`.

```
L = q·X + r ,   0 ≤ r < X
```

* `q` full blocks of `X` zeros – they are *movable*.
* `r` remaining zeros – they are **fixed** (shorter than `X`).

Because a movable block can only leave the run through its **right**
border, the fixed `r` zeros are always the **leftmost** part of the run.

For a run of ones, length `M`

```
M = p·Y + s ,   0 ≤ s < Y
```

* `p` full blocks of `Y` ones – movable,
* `s` remaining ones – fixed, they are the **rightmost** part of the run
  (a movable block leaves the run through its left border).

Consequences
```
zero‑run :  [fixed r zeros] [X‑block] [X‑block] … [X‑block]
one‑run  :  [Y‑block] [Y‑block] … [Y‑block] [fixed s ones]
```

The fixed parts (`r` or `s`) can never be moved.
All movable blocks (`X`‑blocks and `Y`‑blocks) can be permuted arbitrarily:
adjacent blocks of opposite type can be swapped, which is bubble‑sort on the
sequence of blocks.

--------------------------------------------------------------------

#### 3.   What is invariant ?

* the **order** of the fixed parts (`r` and `s`) – they stay where they are,
* inside each interval between two consecutive fixed parts
  the **multiset** of movable blocks is invariant:
  only the order of the blocks can change.

Thus the whole string is uniquely described by

```
fixed parts :   (type, length)   in the order they appear
between them :   number of X‑blocks   and   number of Y‑blocks
```

If two strings have

* the same list of fixed parts, and
* the same numbers of X‑blocks and Y‑blocks in every interval between them,

they can be transformed into each other, otherwise they cannot.

The condition can be checked in one linear scan.



--------------------------------------------------------------------

#### 4.   Algorithm
```
parse(string):
    intervals = [(0,0)]               # (X‑blocks , Y‑blocks)
    fixed = []                         # list of (type , length)
    cur = intervals[0]

    scan maximal runs of equal characters
        if run is zeros (char = '0'):
            r = length % X                # fixed part
            q = length // X               # X‑blocks
            if r > 0:
                fixed.append(('0', r))
                cur = (0,0)
                intervals.append(cur)    # new interval after the fixed part
            cur.Xblocks += q
        else:   # run of ones
            p = length // Y               # Y‑blocks
            s = length % Y                # fixed part (suffix)
            cur.Yblocks += p
            if s > 0:
                fixed.append(('1', s))
                cur = (0,0)
                intervals.append(cur)    # new interval after the fixed part

    return fixed , intervals
```

`fixed` always alternates between a zero‑remainder and a one‑remainder,
the length of `intervals` is `len(fixed)+1`.

Two strings `S` and `T` are equivalent **iff**

* `fixed_S == fixed_T` (as lists, element by element) and
* `intervals_S == intervals_T` (pairwise equal).

If there is **no** movable block at all (`total_blocks == 0`) the
condition still works – the strings consist only of fixed parts, therefore
they must be identical.

The whole procedure is linear, `O(N)`, and uses `O(N)` additional memory.



--------------------------------------------------------------------

#### 5.   Correctness Proof  

We prove that the algorithm prints “Yes” exactly for the pairs of strings
that can be transformed into each other.

---

##### Lemma 1  
In a run of zeros the leftmost `r = length mod X` zeros are fixed,
the remaining `⌊length / X⌋` blocks of `X` zeros are movable.
Analogously, in a run of ones the rightmost `s = length mod Y` ones are
fixed and the preceding `⌊length / Y⌋` blocks of `Y` ones are movable.

**Proof.**  
An operation needs a *suffix* of exactly `X` zeros (or a *prefix* of exactly
`Y` ones).  
If a run contains fewer than `X` zeros it can never be the left part of an
operation – it cannot move.  
If it contains at least `X` zeros, the rightmost `X` zeros form a movable
block, the remaining left part cannot move.  
The same argument holds for ones. ∎



##### Lemma 2  
Two adjacent movable blocks of different type can be swapped,
and after the swap they are still movable blocks of the same sizes.

**Proof.**  
If a movable zero‑block (length `X`) stands immediately left of a movable
one‑block (length `Y`), the pattern `X` zeros `Y` ones is present, therefore
operation A can be applied.
It exchanges the two blocks, afterwards the zero‑block is again a block of
`X` zeros and the one‑block a block of `Y` ones.
The symmetric situation gives operation B. ∎



##### Lemma 3  
Inside any maximal interval delimited by two fixed parts (or by the ends of
the string) the multiset of movable blocks can be permuted arbitrarily.

**Proof.**  
All blocks inside the interval are either `X`‑blocks (zeros) or `Y`‑blocks
(ones) and they appear in alternating order because runs alternate.
By Lemma&nbsp;2 any two neighbouring blocks of different type can be swapped,
hence the usual bubble‑sort works and any permutation of the blocks can be
realised. ∎



##### Lemma 4  
Fixed parts never change their relative order.

**Proof.**  
A fixed part is shorter than `X` (zero‑remainder) or `Y` (one‑remainder);
any operation needs a full block of length `X` or `Y`,
therefore it never involves a fixed part.
Consequently a fixed part can never cross another fixed part or a movable
block, and its position stays unchanged. ∎



##### Lemma 5  
Two strings `S` and `T` are transformable into each other **iff**

* the sequences of fixed parts are identical, and
* for each interval between two consecutive fixed parts the numbers of
  `X`‑blocks and `Y`‑blocks are identical.

**Proof.**  
*Only‑if* part.  
During any sequence of operations a fixed part never moves (Lemma&nbsp;4) and
the total number of movable blocks of each type never changes,
therefore both conditions must hold for the final string as well.

*If* part.  
Assume the conditions hold.
Starting from `S` we look at the first interval (before the first fixed
part). Inside this interval we have the same multiset of blocks as the
corresponding interval of `T`. By Lemma&nbsp;3 we can reorder the blocks of
`S` into the exact order they appear in `T`.  
After that the first fixed part of `S` already equals the first fixed part
of `T`; we continue with the next interval, and so on.
Thus we can transform `S` step by step into `T`. ∎



##### Lemma 6  
`parse` returns exactly the data described in Lemma&nbsp;5.

**Proof.**  
The scan processes a run of zeros:

* `r = length % X` is added as a fixed part **before** the interval,
  exactly the leftmost fixed zeros (Lemma&nbsp;1);
* `q = length // X` `X`‑blocks are added to the current interval.

For a run of ones:

* `p = length // Y` `Y`‑blocks are added to the current interval;
* `s = length % Y` is added as a fixed part **after** the interval,
  the rightmost fixed ones (Lemma&nbsp;1).

Whenever a fixed part is added a new interval is started,
therefore intervals are precisely the maximal parts between two consecutive
fixed parts (or the ends of the string). ∎



##### Lemma 7  
The algorithm outputs “Yes” exactly when the conditions of Lemma&nbsp;5 hold.

**Proof.**  
The algorithm parses both strings, obtaining the lists `fixed` and
`intervals` for each (Lemma&nbsp;6).
It checks equality of the two `fixed` lists and equality of the two
`interval` lists element by element.
These checks are precisely the conditions of Lemma&nbsp;5. ∎



##### Theorem  
The program prints “Yes” iff the given string `S` can be turned into `T`
by repeatedly applying the allowed operations.

**Proof.**  
*If the program prints “Yes”* – by Lemma&nbsp;7 the conditions of
Lemma&nbsp;5 hold, and by Lemma&nbsp;5 the strings are transformable.

*If `S` can be transformed into `T`* – Lemma&nbsp;5 tells us that the
conditions of Lemma&nbsp;5 are true, consequently the two parsed
representations are equal (Lemma&nbsp;7) and the program prints “Yes”.

Thus the output is correct. ∎



--------------------------------------------------------------------

#### 6.   Complexity Analysis

`parse` scans the string once, all operations are `O(1)`.

```
time   :  O(N)      ( N ≤ 5·10⁵ )
memory :  O(N)      (lists of fixed parts and intervals)
```

Both limits satisfy the constraints.



--------------------------------------------------------------------

#### 7.   Reference Implementation  (Python 3)

```python
import sys

def parse_string(s, X, Y):
    """return (fixed_parts, intervals)
       fixed_parts : list of (type, length)   type = 0 for '0', 1 for '1'
       intervals   : list of (cnt_Xblocks, cnt_Yblocks)
    """
    n = len(s)
    fixed = []               # list of (type, length)
    intervals = []           # list of [cntX, cntY]
    cur = [0, 0]
    intervals.append(cur)

    i = 0
    while i < n:
        j = i
        while j < n and s[j] == s[i]:
            j += 1
        length = j - i
        if s[i] == '0':                     # run of zeros
            r = length % X
            q = length // X
            if r > 0:                       # fixed part (prefix)
                fixed.append((0, r))
                cur = [0, 0]
                intervals.append(cur)
            cur[0] += q                     # X‑blocks
        else:                               # run of ones
            p = length // Y
            s_rem = length % Y
            cur[1] += p                     # Y‑blocks
            if s_rem > 0:                   # fixed part (suffix)
                fixed.append((1, s_rem))
                cur = [0, 0]
                intervals.append(cur)
        i = j

    # the last interval (maybe empty) is already stored
    return fixed, intervals


def solve() -> None:
    it = iter(sys.stdin.read().split())
    N = int(next(it))
    X = int(next(it))
    Y = int(next(it))
    S = next(it).strip()
    T = next(it).strip()

    fixedS, intS = parse_string(S, X, Y)
    fixedT, intT = parse_string(T, X, Y)

    # compare fixed parts
    if len(fixedS) != len(fixedT):
        print("No")
        return
    for a, b in zip(fixedS, fixedT):
        if a != b:
            print("No")
            return

    # compare intervals (same length because fixed parts have same length)
    if len(intS) != len(intT):
        print("No")
        return
    for a, b in zip(intS, intT):
        if a[0] != b[0] or a[1] != b[1]:
            print("No")
            return

    print("Yes")


if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required input‑output format.