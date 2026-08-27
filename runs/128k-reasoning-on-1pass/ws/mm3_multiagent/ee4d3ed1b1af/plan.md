**Solution Explanation**

For the pattern  

```
p =  L * M * R                ( exactly two ‘*’ )
```

`*` may match **any** (also empty) sequence of characters.
A substring `s[l … r]` matches `p` iff

* `L` (if not empty) is exactly `s[l … l+|L|-1]`
* `R` (if not empty) is exactly `s[r‑|R|+1 … r]`
* `M` (if not empty) appears somewhere between `L` and `R`

The three parts must appear in the order `L , M , R` (they may touch but they may not
overlap).

The task is to minimise `r‑l+1`.  
All three parts are ordinary strings – we can find all their occurrences in `s`
with a linear‑time string matching algorithm (KMP).

--------------------------------------------------------------------

#### 1.   Splitting the pattern

```
first  = index of the first '*'
second = index of the second '*'

L = p[0 … first‑1]
M = p[first+1 … second‑1]
R = p[second+1 … end]
```

Each part can be empty.

--------------------------------------------------------------------

#### 2.   Occurrences of a part

`kmp(text, pattern)` returns a sorted list `occ` of start positions where
`pattern` occurs in `text`.  
Complexity `O(|text| + |pattern|)`.

```
left  = kmp(s, L)   (empty list if L is empty)
mid   = kmp(s, M)   (empty list if M is empty)
right = kmp(s, R)   (empty list if R is empty)
```

--------------------------------------------------------------------

#### 3.   Solving the different cases  

The answer depends on which parts are empty.

*`M` empty* – the pattern is `L * R`.

```
need: left_start + |L| ≤ right_start
answer = right_start + |R| – left_start
```

Two‑pointer scan over `left` and `right`.

*`M` non‑empty*

| case                         | condition                                 | answer                              |
|------------------------------|-------------------------------------------|-------------------------------------|
| `L` and `R` non‑empty        | left + |L| ≤ mid  and  mid + |M| ≤ right    | `right_start+|R|‑left_start`       |
| only `L` non‑empty (`R`∅)    | left + |L| ≤ mid                           | `mid_start+|M|‑left_start`         |
| only `R` non‑empty (`L`∅)    | mid + |M| ≤ right                          | `right_start+|R|‑mid_start`        |
| only `M` non‑empty            | –                                         | `|M|` (any occurrence of `M`)      |

All three situations are handled by a simple three‑pointer walk:
for each possible start of the *leftmost* part we advance the pointers of the
next part until the first feasible occurrence, compute the length and keep the
minimum.  
If a required part has no occurrence the answer does not exist.

*Both `L` and `R` empty* → pattern is `**` → the empty substring matches → answer `0`.

If no candidate length is found we return `‑1`.

All scans are linear because the three occurrence lists are sorted and each
pointer only moves forward.

--------------------------------------------------------------------

#### 4.   Correctness Proof  

We prove that the algorithm returns exactly the length of the shortest
matching substring.

---

##### Lemma 1  
For every non‑empty part `X ∈ {L,M,R}` the list `occ_X` produced by KMP
contains **all** start positions of `X` in `s` and only those positions.

**Proof.** KMP is a classic exact matching algorithm. It scans `s` once,
maintaining the length of the longest prefix of `X` that matches a suffix of
the already processed part of `s`. Whenever this length becomes `|X|`,
the pattern ends exactly at the current position, i.e. a match starts at
`i‑|X|+1`. The algorithm records this start index.
No other start indices are recorded because a match can only be reported
when the whole pattern has been matched. ∎



##### Lemma 2  
Let `left[i] , mid[j] , right[k]` be the current pointers in the
three‑pointer walk for the case “all three parts non‑empty”.
If the algorithm computes a candidate length  
`len = right[k] + |R| – left[i]` then the substring  
`s[left[i] … right[k]+|R|-1]` satisfies the pattern `L * M * R`.

**Proof.** By construction of the walk  

* `left[i] + |L| ≤ mid[j]`  (otherwise `j` would have been advanced),
* `mid[j] + |M| ≤ right[k]` (otherwise `k` would have been advanced).

Consequently

```
L      = s[left[i] … left[i]+|L|-1]
M      = s[mid[j]  … mid[j] +|M|-1]
R      = s[right[k] … right[k]+|R|-1]
```

and the three intervals appear in the order `L , M , R` with possible
gaps (matched by the two `*`).  Therefore the whole substring matches the
pattern, and its length is exactly `right[k]+|R|‑left[i]`. ∎



##### Lemma 3  
For the case “all three parts non‑empty” the algorithm examines **every**
triple of occurrences `(l,m,r)` that satisfies the order constraints.

**Proof.**  
The left pointer iterates over `left` in increasing order.
For a fixed `l` the algorithm moves `mid` forward until the first `m` with
`m ≥ l+|L|`; this is precisely the smallest `m` that can follow `l`.
All later `m` would give a longer substring, thus they are irrelevant for
minimality and can be skipped – they are examined later when a larger `l`
is processed.

For that chosen `m` the right pointer is moved to the first `r` with
`r ≥ m+|M|`.  Any `r` smaller would violate the order, any larger `r`
produces a longer candidate.  Hence every feasible triple is visited
exactly once (in the order of increasing `l`). ∎



##### Lemma 4  
When the algorithm terminates, `ans` equals the minimum length of a
matching substring for the processed case.

**Proof.**  
*Upper bound*: by Lemma&nbsp;2 every candidate length inserted into `ans`
is the length of a valid matching substring, therefore `ans` never exceeds
the optimum.

*Lower bound*: by Lemma&nbsp;3 every valid matching substring corresponds to
some triple `(l,m,r)` that will be examined by the three‑pointer walk,
and its length will be considered as a candidate.
Consequently the optimum length is among the candidates and `ans` is at most
the optimum.  Hence `ans` equals the optimum. ∎



##### Lemma 5  
The algorithm handles correctly the special cases where some of the parts
are empty.

**Proof.**  
If `M` is empty the pattern reduces to `L * R`.  
The two‑pointer scan uses the necessary condition `left+|L| ≤ right` and
computes the exact length `right+|R|‑left`.  By the same argument as in
Lemma&nbsp;4 the minimum of those lengths is the optimum.

If exactly one of `L` or `R` is empty, the same reasoning applies after
re‑interpreting the missing part as “no restriction on the start/end”.
The answer formula (`mid+|M|‑left` or `right+|R|‑mid`) is precisely the
length of the shortest substring that satisfies the remaining two parts in
the required order.  The algorithm computes exactly that value.

If both `L` and `R` are empty, the empty substring matches and the algorithm
returns `0`. ∎



##### Lemma 6  
If the algorithm returns `‑1` then no substring of `s` matches `p`.

**Proof.**  
`‑1` is returned only when, for the processed case, the required list of
occurrences (left, middle or right) is empty or when the three‑pointer walk
finds no feasible triple.  
In each situation at least one of the mandatory parts (L, M or R) does not
occur in the required order, therefore a matching substring cannot exist. ∎



##### Theorem  
`shortestMatchingSubstring` returns

* the length of the shortest substring of `s` that matches `p`,
* `0` when the empty substring matches,
* `‑1` when no substring matches.

**Proof.**  
All possible combinations of empty / non‑empty parts are covered by the
case analysis.  
For each combination Lemma&nbsp;4 (or Lemma&nbsp;5 for the degenerate cases)
shows that the algorithm finds the minimum possible length.
Lemma&nbsp;6 guarantees that `‑1` is returned exactly when no match exists.
Therefore the returned value satisfies the specification. ∎



--------------------------------------------------------------------

#### 5.   Complexity Analysis  

Let `n = |s|`, `m = |p|` ( `m ≤ 10⁵` ).

* Splitting the pattern – `O(m)`.
* Three KMP runs – each `O(n + length_of_part)`.  
  Sum of part lengths is `m`, so total `O(n + m)`.
* All scans over the occurrence lists are linear in the sum of their
  lengths, which is `O(n)`.

Overall time   `O(n + m)`.  
Memory usage   `O(n)` for the three occurrence lists (at most `n` starts
each) plus the KMP auxiliary arrays, well within the limits.

--------------------------------------------------------------------

#### 6.   Reference Implementation  (Python 3)

```python
import sys
from typing import List

class Solution:
    # ---------- KMP search ----------
    @staticmethod
    def _kmp_occurrences(text: str, pat: str) -> List[int]:
        """return list of start indices where pat occurs in text (pat non‑empty)"""
        if not pat:
            return []                     # should not be called with empty pat
        m = len(pat)
        # prefix function for pat
        pi = [0] * m
        for i in range(1, m):
            j = pi[i - 1]
            while j > 0 and pat[i] != pat[j]:
                j = pi[j - 1]
            if pat[i] == pat[j]:
                j += 1
            pi[i] = j

        res = []
        j = 0
        for i, ch in enumerate(text):
            while j > 0 and ch != pat[j]:
                j = pi[j - 1]
            if ch == pat[j]:
                j += 1
            if j == m:
                res.append(i - m + 1)     # start of the match
                j = pi[j - 1]             # allow overlapping matches
        return res

    # ---------- main method ----------
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        n = len(s)

        # split pattern into three parts
        first = p.find('*')
        second = p.find('*', first + 1)   # exactly two '*' are guaranteed
        L = p[:first]
        M = p[first + 1:second]
        R = p[second + 1:]

        # trivial case "**"
        if not L and not R:
            return 0

        # occurrences of each non‑empty part
        left  = self._kmp_occurrences(s, L) if L else []
        mid   = self._kmp_occurrences(s, M) if M else []
        right = self._kmp_occurrences(s, R) if R else []

        INF = n + 1
        ans = INF

        # ---------- M is empty ----------
        if not M:
            if L and R:                         # pattern L*R
                i = j = 0
                while i < len(left) and j < len(right):
                    l_start = left[i]
                    # move right pointer until it is far enough
                    while j < len(right) and right[j] < l_start + len(L):
                        j += 1
                    if j == len(right):
                        break
                    r_start = right[j]
                    ans = min(ans, (r_start + len(R)) - l_start)
                    i += 1
            elif L:                              # pattern L**
                if left:
                    ans = min(ans, len(L))
            elif R:                              # pattern **R
                if right:
                    ans = min(ans, len(R))
            # both empty already handled earlier
            return ans if ans <= n else -1

        # ---------- M is non‑empty ----------
        if L and R:          # all three parts present
            i = j = k = 0
            while i < len(left):
                l_start = left[i]
                # first mid after L
                while j < len(mid) and mid[j] < l_start + len(L):
                    j += 1
                if j == len(mid):
                    break
                m_start = mid[j]
                # first right after M
                while k < len(right) and right[k] < m_start + len(M):
                    k += 1
                if k == len(right):
                    break
                r_start = right[k]
                ans = min(ans, (r_start + len(R)) - l_start)
                i += 1
        elif L:               # only L and M (R empty)
            i = j = 0
            while i < len(left) and j < len(mid):
                l_start = left[i]
                while j < len(mid) and mid[j] < l_start + len(L):
                    j += 1
                if j == len(mid):
                    break
                m_start = mid[j]
                ans = min(ans, (m_start + len(M)) - l_start)
                i += 1
        elif R:               # only M and R (L empty)
            i = j = 0
            while i < len(mid) and j < len(right):
                m_start = mid[i]
                while j < len(right) and right[j] < m_start + len(M):
                    j += 1
                if j == len(right):
                    break
                r_start = right[j]
                ans = min(ans, (r_start + len(R)) - m_start)
                i += 1
        else:                 # only M (L and R empty)
            if mid:
                ans = min(ans, len(M))

        return ans if ans <= n else -1
```

The program follows exactly the algorithm proven correct above
and conforms to the required `O(|s| + |p|)` time bound.