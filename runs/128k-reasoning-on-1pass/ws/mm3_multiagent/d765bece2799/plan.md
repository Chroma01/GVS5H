**Solution Explanation**

For every subarray we need the sum of its minimum and its maximum.
Let `len = R-L+1` be the length of the subarray, the condition is `len ≤ k`.

For a fixed element `nums[i]`

* it is the **minimum** of a subarray iff  
  * all elements left of `i` inside the subarray are `> nums[i]`  
    → the left border `L` is after the previous *strictly* smaller element,
  * all elements right of `i` are `≥ nums[i]`  
    → the right border `R` is before the next *smaller‑or‑equal* element,
  * and the length `R-L+1 ≤ k`.

* it is the **maximum** of a subarray analogously, using
  * previous *strictly* greater element,
  * next *greater‑or‑equal* element.

The two cases are completely symmetric, therefore we solve the counting
problem for the minimum and reuse the same code for the maximum.

--------------------------------------------------------------------

#### 1.   Borders of the interval where `i` stays the (leftmost) minimum

```
prevLess[i]      – index of the closest element left of i with value < nums[i]
                   (‑1 if none)
nextLessEq[i]    – index of the closest element right of i with value ≤ nums[i]
                   ( n if none)
```

```
leftChoices  = i - prevLess[i]            # possible positions of L
rightChoices = nextLessEq[i] - i          # possible positions of R
```

All admissible subarrays where `i` is the minimum are pairs `(L,R)` with

```
L ∈ [prevLess[i] + 1 , i]          (a = i-L, 0 ≤ a ≤ leftChoices‑1)
R ∈ [i , nextLessEq[i] - 1]        (b = R‑i, 0 ≤ b ≤ rightChoices‑1)
```

The length condition is

```
a + b ≤ k‑1                (let K = k‑1)
```

--------------------------------------------------------------------

#### 2.   Counting pairs `(a,b)` with the length restriction  

```
A = leftChoices      (number of possible a)
B = rightChoices     (number of possible b)
K = k‑1
```

Only the first `min(A, K+1)` values of `a` can ever appear,
let  

```
A' = min(A, K+1)           # we really iterate a = 0 … A'‑1
```

For a fixed `a` the admissible `b` values are `0 … min(B‑1 , K‑a)`.
The number of such `b` is

```
cnt(a) = min( B , K‑a+1 )
```

The total number of subarrays is

```
Σ_{a=0}^{A'‑1} cnt(a)
```

The sum can be computed in **O(1)** :

*If `B ≥ K+1`* then `cnt(a) = K‑a+1` for all considered `a` and

```
total = A'·(K+1) – A'·(A'‑1)/2
```

*Otherwise* (`B < K+1`) there is a threshold  

```
t = K – (B‑1)                # largest a with cnt(a)=B
```

* `a = 0 … min(A'‑1 , t)`  → `cnt = B`
* the remaining `a`          → `cnt = K‑a+1`

The sum of the second part is a short arithmetic series, leading to a
constant‑time formula (see the code).

--------------------------------------------------------------------

#### 3.   Contribution of one element  

```
cntMin[i] = number_of_pairs( leftChoicesMin , rightChoicesMin )
cntMax[i] = number_of_pairs( leftChoicesMax , rightChoicesMax )
answer    = Σ nums[i] · (cntMin[i] + cntMax[i])
```

`cntMin` uses the borders `prevLess / nextLessEq`,
`cntMax` uses `prevGreater / nextGreaterOrEqual` (strictly greater on the
left, greater‑or‑equal on the right).  
Both are obtained with monotone stacks in **O(n)** time.

--------------------------------------------------------------------

#### 4.   Correctness Proof  

We prove that the algorithm returns exactly the required sum.

---

##### Lemma 1  
For a fixed index `i` a subarray `[L,R]` (with `L ≤ i ≤ R`) has `i` as the
**leftmost minimum** iff  

* `L > prevLess[i]`  (all elements left of `i` inside the subarray are `> nums[i]`),
* `R < nextLessEq[i]` (all elements right of `i` inside the subarray are `≥ nums[i]`).

**Proof.**  
*If* the two inequalities hold, every element left of `i` is larger,
so the minimum of the subarray is at most `nums[i]`; because all those
elements are larger, the minimum equals `nums[i]`.  
If an equal element existed left of `i`, the condition `>` would be false,
so no equal element can be left of `i`; therefore `i` is the leftmost
occurrence of the minimum.  
*Conversely*, if `i` is the leftmost minimum, any element left of `i`
must be `> nums[i]`, otherwise it would be a smaller or equal element
appearing earlier. This implies `L > prevLess[i]`.  
Similarly any element right of `i` must be `≥ nums[i]`; otherwise a
strictly smaller element would exist to the right, contradicting that
`i` is the minimum. Hence `R < nextLessEq[i]`. ∎



##### Lemma 2  
Let  

```
A = i - prevLess[i]      (number of possible L)
B = nextLessEq[i] - i    (number of possible R)
K = k-1
```

The number of subarrays with length ≤ k in which `i` is the leftmost
minimum equals the number of integer pairs `(a,b)` with

```
0 ≤ a ≤ A‑1 ,   0 ≤ b ≤ B‑1 ,   a+b ≤ K .
```

**Proof.**  
`a = i-L` runs from `0` (when `L=i`) to `A‑1` (when `L = prevLess[i]+1`);
`b = R-i` runs from `0` to `B‑1`.  
The length of the subarray is `R-L+1 = a+b+1`.  
The condition `length ≤ k` is exactly `a+b ≤ k‑1 = K`.  
The bijection `(L,R) ↔ (a,b)` proves the claim. ∎



##### Lemma 3  
The function `count_pairs(A,B)` implemented in the solution returns the
number of pairs described in Lemma&nbsp;2.

**Proof.**  
Only `a ≤ K` can ever satisfy `a+b ≤ K`; therefore at most the first
`A' = min(A, K+1)` values of `a` are relevant.  
For a fixed `a` the admissible `b` are `0 … min(B‑1, K‑a)`, i.e.  
`cnt(a) = min( B , K‑a+1 )`.  
The function computes exactly  

```
Σ_{a=0}^{A'‑1} min( B , K‑a+1 )
```

by a case distinction on whether `B ≥ K+1` (then the minimum is the
second argument) or not (then a threshold `t = K-(B-1)` separates the
constant part from a decreasing arithmetic series).  The algebraic
formulas used are direct evaluations of that sum, hence the returned
value equals the required number of pairs. ∎



##### Lemma 4  
`cntMin[i]` (resp. `cntMax[i]`) computed by the algorithm equals the
number of subarrays of length ≤ k whose minimum (resp. maximum) is the
element at position `i`.

**Proof.**  
For the minimum we use `prevLess` and `nextLessEq`; by Lemma&nbsp;1 these
borders describe exactly the subarrays where `i` is the leftmost
minimum.  Lemma&nbsp;2 translates the geometric condition to the
combinatorial pair counting, and Lemma&nbsp;3 shows that the program
counts those pairs.  The same reasoning holds for the maximum using
`prevGreater` and `nextGreaterOrEqual`. ∎



##### Lemma 5  
The algorithm’s final sum

```
 Σ_i nums[i]·(cntMin[i] + cntMax[i])
```

equals the sum of `(minimum + maximum)` over **all** subarrays with
length ≤ k.

**Proof.**  
Consider any subarray `S`.  
Its minimum is some element `i_min`; by Lemma&nbsp;4 the subarray `S`
contributes `1` to `cntMin[i_min]`.  
Analogously it contributes `1` to `cntMax[i_max]`.  
Therefore `nums[i_min]` is added once in the first term and
`nums[i_max]` once in the second term, which is exactly
`min(S) + max(S)`.  
Summation over all subarrays yields the required total. ∎



##### Theorem  
`minMaxSubarraySum` returns the sum of the minimum and maximum elements
of every subarray of `nums` whose length is at most `k`.

**Proof.**  
By Lemma&nbsp;4 each `cntMin[i]` (resp. `cntMax[i]`) is the exact number
of admissible subarrays where `i` is the minimum (resp. maximum).  
Lemma&nbsp;5 shows that adding `nums[i]` multiplied by those counts for
all `i` produces precisely the desired total.  The algorithm computes
exactly this expression, therefore it is correct. ∎



--------------------------------------------------------------------

#### 5.   Complexity Analysis  

*Four monotone‑stack passes* – each `O(n)` time, `O(n)` extra memory.  
*Final loop* – `O(n)` time, `O(1)` extra memory.  

```
Time   :  O(n)        ( ≤ 8·10⁴ operations )
Memory :  O(n)        ( four integer arrays of length n )
```

Both limits easily satisfy the constraints.

--------------------------------------------------------------------

#### 6.   Reference Implementation  (Python 3)

```python
from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        limit = k - 1                     # maximal allowed a+b

        # ---------- previous strictly smaller (for minimum) ----------
        prev_less = [-1] * n
        st = []
        for i in range(n):
            while st and nums[st[-1]] > nums[i]:
                st.pop()
            prev_less[i] = st[-1] if st else -1
            st.append(i)

        # ---------- next smaller-or-equal (for minimum) ----------
        next_le = [n] * n
        st = []
        for i in range(n - 1, -1, -1):
            while st and nums[st[-1]] > nums[i]:
                st.pop()
            next_le[i] = st[-1] if st else n
            st.append(i)

        # ---------- previous strictly greater (for maximum) ----------
        prev_greater = [-1] * n
        st = []
        for i in range(n):
            while st and nums[st[-1]] <= nums[i]:
                st.pop()
            prev_greater[i] = st[-1] if st else -1
            st.append(i)

        # ---------- next greater-or-equal (for maximum) ----------
        next_ge = [n] * n
        st = []
        for i in range(n - 1, -1, -1):
            while st and nums[st[-1]] < nums[i]:
                st.pop()
            next_ge[i] = st[-1] if st else n
            st.append(i)

        # ----- helper: count (a,b) with a in [0,A-1], b in [0,B-1], a+b <= limit -----
        def count_pairs(A: int, B: int) -> int:
            # only the first limit+1 values of a can be used
            A_prime = A if A <= limit + 1 else limit + 1
            if B >= limit + 1:
                # min(B, limit-a+1) = limit-a+1 for all a
                return A_prime * (limit + 1) - (A_prime * (A_prime - 1)) // 2
            else:
                t = limit - (B - 1)                # largest a with cnt(a)=B
                region1_len = t + 1                # number of a with cnt(a)=B
                if region1_len >= A_prime:
                    return A_prime * B
                else:
                    total = region1_len * B
                    rem = A_prime - region1_len    # remaining a values
                    # sum of a from region1_len to A_prime-1
                    sum_a = (region1_len + (A_prime - 1)) * rem // 2
                    total += rem * (limit + 1) - sum_a
                    return total

        ans = 0
        for i in range(n):
            left_min = i - prev_less[i]
            right_min = next_le[i] - i
            left_max = i - prev_greater[i]
            right_max = next_ge[i] - i

            cnt_min = count_pairs(left_min, right_min)
            cnt_max = count_pairs(left_max, right_max)

            ans += nums[i] * (cnt_min + cnt_max)

        return ans
```

The program follows exactly the algorithm proven correct above and
conforms to the required `O(n)` time and `O(n)` memory limits.