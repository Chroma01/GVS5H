**Solution Explanation**

For a sequence `A[1 … N]` we may repeatedly delete two *adjacent* numbers.
If the deleted numbers are `x , y` we obtain a score `|x‑y|`.
The process stops when at most one number is left.

--------------------------------------------------------------------

#### 1.   From the process to a pairing of positions  

During the whole process every original element is deleted exactly once,
except possibly one element when `N` is odd.
Think of the moment when two elements `A[i] , A[j]` are deleted.
All elements between them have already been removed, therefore the
pair `(i , j)` is a **non‑crossing** pair of positions:
no two pairs intersect, they are either disjoint or one is completely
inside the other.

Consequently the whole operation is equivalent to

*choose a non‑crossing perfect matching of the positions*  
(and leave one position unmatched if `N` is odd).

For a chosen matching the total score is simply the sum of
`|A[i]‑A[j]|` over all its pairs.

--------------------------------------------------------------------

#### 2.   Reformulation with signs  

For a pair `{i , j}` let the larger value be called **+** and the
smaller **–**.  
If the pair contributes `|A[i]‑A[j]|` we may write

```
contribution = (+ value) – (– value)
```

Hence for the whole matching

```
total score = Σ ( sign[p] · A[p] )                (1)
```

where `sign[p] = +1` if `A[p]` is the larger element of its pair,
`sign[p] = –1` otherwise.
All `sign[p]` are `+1` or `–1` and the number of `+1` equals the number
of `–1` (or differs by one when `N` is odd – the remaining element has
sign `0`).  
The only restriction is this balance of signs.

--------------------------------------------------------------------

#### 3.   Which sign assignment gives the maximum?  

Equation (1) shows that we only have to choose the signs, the matching
itself can be built afterwards (see the next section).  
For a fixed multiset of signs the value (1) is maximised by putting
`+1` on the *largest* numbers and `–1` on the *smallest* numbers
(the classic rearrangement inequality).

Let  

```
K = ⌊N/2⌋                (number of pairs)
```

*   choose the `K` largest numbers → sign `+1`
*   choose the `K` smallest numbers → sign `–1`
*   (if N is odd) the remaining middle number is the survivor (sign `0`)

Then the maximal possible total score is

```
answer = (sum of K largest) – (sum of K smallest)          (2)
```

--------------------------------------------------------------------

#### 4.   Can this sign assignment be realised?  

Yes.  
We only have to show that any sequence containing `K` pluses and `K`
minuses (plus one neutral element) can be reduced to empty by repeatedly
deleting an *adjacent* plus‑minus pair.

*Lemma* – In a non‑empty sequence with equal numbers of `+` and `–`
there is always an adjacent pair of opposite signs.

*Proof.*  
If the first two signs were equal, the whole sequence would consist of
that sign only, contradicting the equal counts. ∎

**Construction**  
Repeatedly locate an adjacent `+ –` (or `– +`) and delete it.
The numbers of `+` and `–` stay equal, therefore the lemma guarantees
that we can continue until nothing is left.
Thus we obtain a sequence of operations where every deletion pairs a `+`
with a `–`.  
Because the larger value of the pair is the `+` and the smaller the `–`,
the contribution of that operation is exactly the difference of the two
values. Summing over all operations gives (2).

Hence the bound (2) is attainable and therefore optimal.

--------------------------------------------------------------------

#### 5.   Algorithm  

* sort the array `A`
* let `K = N // 2`
* `small = sum of the first K elements`
* `large = sum of the last  K elements`
* answer = `large – small`

--------------------------------------------------------------------

#### 6.   Correctness Proof  

We prove that the algorithm outputs the maximum possible total score.

---

##### Lemma 1  
For any sequence of `+` and `–` with equal cardinalities there exists a
sequence of adjacent deletions that removes all elements, each deletion
pairing a `+` with a `–`.

*Proof.* By the Lemma of Section&nbsp;4 an adjacent opposite pair always
exists; deleting it preserves the equality of the two counts.
Induction on the length of the sequence gives the claim. ∎

---

##### Lemma 2  
Let `K = ⌊N/2⌋`.  
The value `S = (sum of K largest A) – (sum of K smallest A)` is the
maximum possible value of `Σ sign[p]·A[p]` under the constraints
`sign[p]∈{+1,−1,0}` and the numbers of `+1` and `–1` are equal
(their common count is `K`).

*Proof.*  
For any feasible sign vector, reorder the terms of the sum in decreasing
order of `A[p]`. The contribution of each term is either `+A[p]` or
`‑A[p]`. By the rearrangement inequality the sum is maximised when the
largest `K` numbers receive `+1` and the smallest `K` receive `‑1`. ∎

---

##### Lemma 3  
The score `S` from Lemma&nbsp;2 can be achieved by a legal sequence of
operations.

*Proof.*  
Assign `+1` to the `K` largest values and `‑1` to the `K` smallest
values (the remaining element, if any, is neutral).  
By Lemma&nbsp;1 there is a sequence of adjacent deletions that pairs each
`+` with a `–`. In every such pair the larger element is the `+`,
the smaller the `–`, therefore the added score equals
`(+ value) – (– value)`. Summing over all pairs yields exactly `S`. ∎

---

##### Lemma 4  
The algorithm outputs `S`.

*Proof.*  
The algorithm sorts `A`, sums the first `K` elements (`small`) and the
last `K` elements (`large`) and returns `large – small`.  
After sorting the first `K` elements are the `K` smallest, the last
`K` elements are the `K` largest, hence the returned value equals `S`. ∎

---

##### Theorem  
The algorithm always prints the maximum possible total score.

*Proof.*  
Let `OPT` be the optimal achievable total score.
From Lemma&nbsp;2 any feasible sign assignment yields a total score at
most `S`. Because the process can realise any such sign assignment
(Lemmas&nbsp;1 and&nbsp;3), the optimum `OPT` cannot exceed `S`.  
Lemma&nbsp;4 shows that the algorithm outputs `S`.  
Therefore `OPT = S` and the algorithm is optimal. ∎



--------------------------------------------------------------------

#### 7.   Complexity Analysis  

*Sorting* `A` : `O(N log N)`  
*Summations* : `O(N)` (or `O(1)` after sorting)  

Memory consumption: the array `A` (`O(N)`).

Both limits easily satisfy `N ≤ 3·10⁵`.

--------------------------------------------------------------------

#### 8.   Reference Implementation  (Python 3)

```python
import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    a = [int(next(it)) for _ in range(n)]

    a.sort()
    k = n // 2                     # number of pairs
    # sum of k smallest and k largest
    sum_small = sum(a[:k])
    sum_large = sum(a[-k:]) if k > 0 else 0

    ans = sum_large - sum_small
    sys.stdout.write(str(ans))

if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required input‑output format.