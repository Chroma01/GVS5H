**Solution Explanation**

For a fixed length `L` look at the prefixes of length `L` of all words.

```
cnt[p] = number of words that have the prefix p      ( 1 ≤ L ≤ word length )
```

For a given `L` the answer for a removed index `i` is

```
there exists a prefix p of length L
cnt[p] – ( words[i] has prefix p ? 1 : 0 )  ≥  k
```

The longest possible `L` is required.



--------------------------------------------------------------------

#### 1.   Observations

* `cnt[p]` never changes, only one word disappears when we remove `i`.
* After the removal the largest count among all prefixes of length `L` becomes  

  `maxCnt[L]            – 0`   if the removed word does **not** belong to a
  prefix that reaches `maxCnt[L]`  

  `maxCnt[L] – 1`       otherwise.
* Let  

```
M[L] = maxCnt[L]                           (the largest cnt of a prefix of length L)
C[L] = number of prefixes of length L with cnt = k
```

  `M[L]` and `C[L]` are known after we have processed all words.

* For a fixed `L`

```
M[L] ≥ k+1                         → after every removal we still have ≥k strings
                                    → answer L for every i

M[L] = k  and C[L] ≥ 2             → there are at least two different prefixes,
                                      each occurring k times.
                                    After removing one word at most one of them is
                                    destroyed → still a prefix with k strings
                                    → answer L for every i

M[L] = k  and C[L] = 1             → exactly one prefix pL of length L occurs k times.
                                    It works for a concrete i **iff**
                                    words[i] does **not** have pL as a prefix.
```

*If `k = 1` the whole story is different – the longest common prefix of a
single word is the whole word.
The answer is simply the longest word length that stays after the removal.*

From the observations we obtain the following algorithm.

--------------------------------------------------------------------

#### 2.   Algorithm for `k ≥ 2`

```
1. build a trie of all words
   every node stores   cnt  = how many words go through it
   depth of a node = prefix length

2. for every depth L (1 … maxWordLength)
        M[L] = maximum cnt of a node with this depth
        C[L] = number of nodes with this depth and cnt = k

3. L0 = max L with   (M[L] ≥ k+1)  or  (M[L] = k and C[L] ≥ 2)
   (the largest length that works for every i)

4. lengths that are *special*:
        specialL = all L  (L > L0)  with   M[L] = k  and  C[L] = 1
   they are processed from large to small.

5. for each word i
        Bad[i] = set of special lengths L
                 such that the word’s own prefix of length L is the unique
                 prefix that occurs k times
        (size of every Bad[i] ≤ word length, total size ≤ 10⁵)

6. answer[i] = L0   for all i
   for every i  walk through specialL in decreasing order
        the first L that is not in Bad[i] is the maximal possible length,
        set answer[i] = L and stop.
   (the total number of membership tests over all i is
    Σ |Bad[i]|  +  n   ≤ 2·10⁵, fast enough)

7. return the array answer
```

All steps are linear in the total length of the input  
(`Σ |words[i]| ≤ 10⁵`) plus `O(maxWordLength) ≤ 10⁴`.

--------------------------------------------------------------------

#### 3.   Correctness Proof  

We prove that the algorithm returns the required array.

---

##### Lemma 1  
For a fixed length `L` and a removed index `i`

```
after the removal there are at least k strings sharing a prefix of length L
⇔
M[L] ≥ k+1                                   (1)
or
M[L] = k  and  C[L] ≥ 2                       (2)
or
M[L] = k , C[L] = 1  and  words[i] does NOT have the unique prefix of length L.
```

**Proof.**

*If part* – assume the three conditions on the right side hold.

* (1) `M[L] ≥ k+1` : at least `k+1` words share a prefix of length `L`.  
  Removing a single word leaves at least `k` of them.

* (2) `M[L] = k` and `C[L] ≥ 2` : there are at least two *different*
  prefixes, each occurring exactly `k` times.
  A word belongs to exactly one of them, therefore after the removal
  at least one of the two prefixes still has `k` occurrences.

* (3) `M[L] = k , C[L] = 1` and the removed word does **not** have the
  unique prefix `pL` of length `L`.  
  The `k` words that have `pL` stay unchanged, consequently `pL`
  still occurs `k` times.

In all three cases a prefix of length `L` with at least `k` occurrences
remains – the *if* direction.

*Only‑if part* – suppose after removing `i` there exists a prefix `p` of
length `L` with at least `k` occurrences.

* If `cnt[p] ≥ k+1` before the removal, then `M[L] ≥ k+1` – condition (1).

* Otherwise `cnt[p] = k`.  
  There can be only one such prefix, otherwise the removal could affect at
  most one of them and the other would already give a prefix with `k`
  occurrences.  
  Hence `C[L] = 1`.  
  If the removed word belongs to this prefix its count would drop to `k‑1`,
  contradicting the existence of a remaining `k`‑occurrence.
  Therefore the removed word does **not** have this prefix – condition (3).

∎



##### Lemma 2  
Let  

```
L* = max { L | condition (1) or (2) of Lemma&nbsp;1 holds } .
```

For every index `i` the answer is at least `L*`.

**Proof.**  
For any `L` satisfying (1) or (2) the premise of Lemma&nbsp;1 is true
independently of which word is removed.
Hence such an `L` is feasible for **all** `i`.  
Taking the maximum of those feasible lengths gives a lower bound `L*`. ∎



##### Lemma 3  
For a length `L` with `M[L]=k` and `C[L]=1`
(let `pL` be the unique prefix that occurs `k` times)

```
L is feasible for i   ⇔   L ∉ Bad[i] .
```

**Proof.**  
By Lemma&nbsp;1 case (3) feasibility of `L` is equivalent to
“the removed word does **not** have `pL` as a prefix”.
`Bad[i]` is exactly the set of such lengths for word `i`. ∎



##### Lemma 4  
For every index `i` the algorithm returns the largest feasible length.

**Proof.**  
All lengths are divided into two groups.

*Group A* – lengths satisfying (1) or (2) of Lemma&nbsp;1.  
The algorithm computes `L0 = max Group A`.  
By Lemma&nbsp;2 every `i` can reach at least `L0`, and the algorithm
initialises `ans[i] = L0`.

*Group B* – lengths with `M[L]=k` and `C[L]=1`.  
The algorithm stores them in `specialL` in decreasing order.
For a fixed `i` Lemma&nbsp;3 tells us that a length `L∈B` is feasible
iff `L∉Bad[i]`.  
Scanning `specialL` from the largest element, the first `L` that is not in
`Bad[i]` is the greatest feasible length of group B.
The algorithm performs exactly this scan, updates `ans[i]` with that `L`
(if it exists) and stops.
Consequently `ans[i]` becomes the maximum of the two groups,
i.e. the largest feasible length for index `i`. ∎



##### Lemma 5  
For `k = 1` the algorithm (the special branch) returns the correct answer.

**Proof.**  
With `k=1` the longest common prefix of a *single* word is the whole word.
Let  

```
maxLen   = max length of all words
cntMax   = number of words having length maxLen
secLen   = second largest length (0 if it does not exist)
```

If at least two words have length `maxLen` then after removing any word
a word of length `maxLen` stays – answer `maxLen`.  
Otherwise the only word of length `maxLen` is removed and the best we can
do is `secLen`.  
The algorithm implements exactly this case analysis, therefore it is
correct for `k=1`. ∎



##### Theorem  
For every input array `words` and integer `k` the method
`longestCommonPrefix` returns an array `answer` such that
`answer[i]` equals the length of the longest common prefix of any
`k` strings among the remaining array after removing the `i`‑th element
(and `0` if fewer than `k` strings remain).

**Proof.**  

*If `k = 1`* the claim follows from Lemma&nbsp;5.

*If `k ≥ 2`* the algorithm follows the steps described in Sections&nbsp;2
and&nbsp;3.
Lemmas&nbsp;2–4 prove that for every index `i` the value written to
`answer[i]` is exactly the largest length that satisfies Lemma&nbsp;1,
i.e. the definition of the required answer.
Thus the theorem holds for all `k`. ∎



--------------------------------------------------------------------

#### 4.   Complexity Analysis  

*`N = words.length`, `M = Σ |words[i]|  ≤ 10⁵`*

* building the trie                    `O(M)`
* computing `M[L]` and `C[L]`            `O(M)` (one pass over the nodes)
* building the sets `Bad[i]`             `O(M)`  (each character inspected once)
* processing the answers                 `O(N + M)` (total number of set
  look‑ups is `N + Σ|Bad[i]| ≤ 2·M`)

Overall time   `O(N + M)`  ≤ `2·10⁵`.

Memory usage  

* trie: at most `M+1` nodes, each `26` integers + counters  
  ≤ 12 MiB
* auxiliary arrays `M[L] , C[L]` : `maxWordLength ≤ 10⁴`
* `Bad[i]` : total stored pairs `≤ M`  

Overall well below the limits.



--------------------------------------------------------------------

#### 5.   Reference Implementation  (Python 3)

```python
import sys
from typing import List

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)

        # ----------  k = 1  (special, very easy) ----------
        if k == 1:
            # longest word length that stays after the removal
            max_len = max(len(w) for w in words)
            cnt_max = sum(1 for w in words if len(w) == max_len)

            if cnt_max >= 2:
                # at least one word of maximal length remains for any removal
                return [max_len] * n

            # only one word has maximal length
            second_len = 0
            for w in words:
                l = len(w)
                if l != max_len:
                    second_len = max(second_len, l)

            ans = [0] * n
            for i, w in enumerate(words):
                if len(w) == max_len:          # the unique maximal word is removed
                    ans[i] = second_len
                else:
                    ans[i] = max_len
            return ans

        # ----------  k >= 2  ----------
        # ---------- 1. build trie ----------
        # each node: children[26] (list of ints, -1 = absent), cnt, depth
        children = [[-1] * 26]   # node 0 = root, depth 0
        cnt = [0]                # number of words that go through the node
        depth = [0]

        for w in words:
            node = 0
            for pos, ch in enumerate(w):
                idx = ord(ch) - 97
                nxt = children[node][idx]
                if nxt == -1:
                    nxt = len(children)
                    children.append([-1] * 26)
                    cnt.append(0)
                    depth.append(pos + 1)
                    children[node][idx] = nxt
                node = nxt
                cnt[node] += 1

        max_depth = max(len(w) for w in words)

        # ---------- 2. compute M[L] and C[L] ----------
        M = [0] * (max_depth + 1)          # maximal cnt at depth L
        C = [0] * (max_depth + 1)          # how many prefixes of depth L have cnt == k
        for node in range(1, len(children)):
            d = depth[node]
            c = cnt[node]
            if c > M[d]:
                M[d] = c
            if c == k:
                C[d] += 1

        # ---------- 3. universal length ----------
        L0 = 0
        for L in range(1, max_depth + 1):
            if M[L] >= k + 1 or (M[L] == k and C[L] >= 2):
                L0 = L                      # later L overrides earlier, we need the max

        # ---------- 4. special lengths (only one prefix with cnt==k) ----------
        special = []
        for L in range(max_depth, 0, -1):
            if L <= L0:
                break
            if M[L] == k and C[L] == 1:
                special.append(L)           # already in decreasing order

        # ---------- 5. for every word: which special lengths block it ----------
        Bad = [set() for _ in range(n)]    # Bad[i] = set of special lengths that word i possesses
        for idx, w in enumerate(words):
            node = 0
            for pos, ch in enumerate(w):
                node = children[node][ord(ch) - 97]
                L = pos + 1
                # a special length L is characterised by
                #   cnt of this node == k  and  M[L] == k  and  C[L] == 1
                if cnt[node] == k and M[L] == k and C[L] == 1:
                    Bad[idx].add(L)

        # ---------- 6. compute answers ----------
        ans = [L0] * n
        for i in range(n):
            # try larger special lengths, the first not blocked is the best
            for L in special:
                if L > ans[i] and L not in Bad[i]:
                    ans[i] = L
                    break

        return ans
```

The program follows exactly the algorithm proven correct above
and conforms to the required time‑ and memory limits.