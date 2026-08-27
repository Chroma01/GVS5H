We need to count subsequences of length 5 where the element at the middle position (index 2 of the subsequence) is the unique mode. Since the subsequence length is fixed at 5, the middle element appears at index 2. For an element $x$ at the middle position to be the unique mode, it must appear at least twice in the subsequence (since if it appears once, no other element can appear more than once, making it not strictly greater than others if others also appear once, but actually, if it appears once and others appear once, there is no unique mode. If it appears twice, others can appear at most once. If it appears 3 times, others can appear at most once. If it appears 4 or 5 times, others appear 0 or 1 times). Specifically, for $x$ to be the unique mode in a size-5 sequence:
1. $x$ must appear at least 2 times.
2. No other element can appear $\ge 2$ times.
3. The middle element must be $x$.

Strategy:
Iterate over each distinct number $x$ present in `nums` to be the candidate for the middle mode.
For a fixed $x$, we choose one instance of $x$ to be the middle element (index 2). Let's say we pick the $i$-th occurrence of $x$ as the middle.
Then we need to choose 2 elements from the occurrences of $x$ that appear *before* index $i$ and 2 elements from the occurrences of $x$ that appear *after* index $i$? No, the order in the subsequence matters for the "middle" definition, but the problem asks for the number of *subsequences*. A subsequence is defined by the indices chosen. If we pick indices $i_1 < i_2 < i_3 < i_4 < i_5$, then the middle element is at $i_3$. The value at $i_3$ must be $x$, and $x$ must be the unique mode.
So, for a fixed value $x$:
We iterate through every occurrence of $x$ in `nums` and treat it as the middle element (the 3rd element of the subsequence).
Let the current index be $mid$. We need to choose 2 indices from the range $[0, mid-1]$ and 2 indices from the range $[mid+1, n-1]$.
However, we must ensure that no other value appears $\ge 2$ times in the chosen 4 elements (2 from left, 2 from right).
Actually, a simpler approach:
Total ways to form a subsequence of length 5 with middle element $x$ (at index $mid$) is: (count of $x$ before $mid$ choose 2) * (count of $x$ after $mid$ choose 2) * (ways to choose 2 non-$x$ from left) * (ways to choose 2 non-$x$ from right)? No, the subsequence must have exactly 5 elements. The middle is $x$. We need 2 more $x$'s and 2 non-$x$'s? Or just $x$ appears $\ge 2$ times total?
If $x$ appears 2 times total (one is middle, one is left or right), then the other 3 elements must be distinct from $x$ and distinct from each other? No.
Condition: $x$ is the unique mode.
Case A: $x$ appears 2 times. Then all other 3 elements must be distinct from $x$ and distinct from each other.
Case B: $x$ appears 3 times. Then the other 2 elements must be distinct from $x$ and distinct from each other.
Case C: $x$ appears 4 times. Then the other 1 element must be distinct from $x$.
Case D: $x$ appears 5 times.

This seems complicated to handle all cases by inclusion-exclusion.
Alternative approach:
Iterate over each distinct number $x$.
For each occurrence of $x$ at index $i$, consider it as the middle element.
We need to choose 2 indices from $0..i-1$ and 2 indices from $i+1..n-1$.
Let $L$ be the set of indices $< i$ and $R$ be the set of indices $> i$.
We choose $l_1, l_2 \in L$ and $r_1, r_2 \in R$.
The multiset of values is $\{nums[l_1], nums[l_2], x, nums[r_1], nums[r_2]\}$.
$x$ is the unique mode if count($x$) > count($y$) for all $y \neq x$.
Since we are iterating $i$ as the specific middle index, we are counting specific subsequences.
Wait, if a subsequence has multiple $x$'s, say 2 $x$'s, and we pick the first $x$ as middle, does that count? Yes, because the subsequence is defined by indices. If the subsequence is $[a, b, x, x, c]$, the middle is $x$. If the subsequence is $[a, x, x, b, c]$, the middle is $x$. These are different subsequences if the indices are different.
So we can simply iterate over every index $i$ where $nums[i] == x$.
For this $i$, we need to choose 2 indices from left and 2 from right such that the resulting multiset has $x$ as unique mode.
Let $cntL$ be the count of $x$ in left, $cntR$ be the count of $x$ in right.
Let $totalL = i$, $totalR = n - 1 - i$.
We need to choose 2 from left and 2 from right.
Total ways to choose 2 from left is $\binom{i}{2}$, from right $\binom{n-1-i}{2}$.
But we have constraints on other numbers.
Actually, it's easier to calculate the total ways to pick 2 from left and 2 from right, then subtract cases where some $y \neq x$ appears $\ge 2$ times.
But $y$ could appear in left, right, or both.
Since $N$ is up to 1000, $O(N^2)$ is acceptable.
Algorithm:
1. Count frequency of each number.
2. Iterate over each distinct number $x$.
3. For each occurrence $i$ of $x$:
   Calculate valid pairs $(l_1, l_2)$ from left and $(r_1, r_2)$ from right.
   This looks like $O(N^2)$ per $i$, total $O(N^3)$, which is $10^9$, too slow.
   
Optimization:
Instead of iterating $i$, let's iterate $x$.
For a fixed $x$, we want to sum over all valid subsequences where $x$ is the middle mode.
A subsequence is valid if:
- It has length 5.
- The element at index 2 is $x$.
- $x$ is the unique mode.
This implies:
- $x$ appears at least 2 times.
- No other value appears $\ge 2$ times.
Let's classify by the number of times $x$ appears: $k \in \{2, 3, 4, 5\}$.
If $x$ appears $k$ times, then the other $5-k$ elements must be distinct from $x$ and distinct from each other.
Also, the middle element must be $x$.
This means in the sorted indices of the subsequence $idx_1 < idx_2 < idx_3 < idx_4 < idx_5$, we must have $nums[idx_3] = x$.
And among the chosen indices, exactly $k$ of them have value $x$.
And no other value appears $\ge 2$ times.

Let's try a different angle.
Iterate over each distinct $x$.
For a fixed $x$, we want to count subsequences where $x$ is the middle mode.
We can iterate over the position of the middle $x$. Let this be index $i$ in `nums`.
Then we need to choose 2 indices from $0..i-1$ and 2 from $i+1..n-1$.
Let the chosen indices be $l_1, l_2$ and $r_1, r_2$.
The condition is: count($x$) in $\{l_1, l_2, r_1, r_2\} \cup \{i\}$ is $> \max_{y \neq x} (\text{count}(y))$.
Let $c_L(y)$ be count of $y$ in left, $c_R(y)$ be count of $y$ in right.
We choose 2 from left, 2 from right.
Let $k_L$ be number of $x$'s chosen from left ($0, 1, 2$).
Let $k_R$ be number of $x$'s chosen from right ($0, 1, 2$).
Total $x$'s = $k_L + k_R + 1$.
Condition: $k_L + k_R + 1 > \max(\text{count of any } y \neq x \text{ in chosen})$.
This means no $y \neq x$ can appear $\ge 2$ times in the chosen 4 elements.
So, we cannot choose 2 indices with same value $y$ from left, nor 2 from right, nor 1 from left and 1 from right with same value $y$.
Actually, if we choose 2 indices from left with value $y$, then count($y$) = 2. Since total $x$ count is at most 5, if $x$ count is 2, then $2 > 2$ is false. So $x$ count must be $> 2$ if any other appears 2 times? No, unique mode means strictly greater.
So if any $y \neq x$ appears 2 times, then $x$ must appear $\ge 3$ times.
If any $y \neq x$ appears 3 times, then $x$ must appear $\ge 4$ times.
If any $y \neq x$ appears 4 times, then $x$ must appear $\ge 5$ times.
But we only choose 4 elements besides the middle. So max count for any $y$ is 4.
Possible scenarios for $x$ count ($K$):
- $K=2$: Then no $y$ can appear $\ge 2$ times. So all 4 other elements must be distinct and not $x$.
- $K=3$: Then no $y$ can appear $\ge 3$ times. So no $y$ appears 3 or 4 times. But since we only pick 4 elements, max count for $y$ is 4. If $y$ appears 3 times, $3 \not< 3$. So no $y$ appears $\ge 3$ times.
- $K=4$: No $y$ appears $\ge 4$ times.
- $K=5$: No $y$ appears $\ge 5$ times (impossible anyway).

This suggests we can iterate $x$, then iterate $i$ (middle index).
For fixed $x, i$:
We need to choose 2 from left, 2 from right.
Let $S_L$ be the multiset of values in left, $S_R$ in right.
We need to choose subsets $A \subset S_L, |A|=2$ and $B \subset S_R, |B|=2$ such that:
Let $K = (\text{count of } x \text{ in } A) + (\text{count of } x \text{ in } B) + 1$.
Let $M = \max_{y \neq x} (\text{count of } y \text{ in } A \cup B)$.
We need $K > M$.

Since $N$ is small (1000), maybe we can precompute for each $x$ and each $i$:
- Count of $x$ in left ($cL$), count in right ($cR$).
- Total ways to pick 2 from left: $\binom{i}{2}$.
- Total ways to pick 2 from right: $\binom{n-1-i}{2}$.
But we need to exclude invalid configurations.
Invalid configurations are those where some $y \neq x$ appears $\ge 2$ times.
Since we pick only 2 from left and 2 from right, the only way a $y$ appears $\ge 2$ times is:
1. $y$ appears 2 times in left (and 0 or 1 in right).
2. $y$ appears 2 times in right (and 0 or 1 in left).
3. $y$ appears 1 time in left and 1 time in right.

Let's use inclusion-exclusion or direct counting.
For fixed $x, i$:
Total ways = $\binom{i}{2} \times \binom{n-1-i}{2}$.
Subtract cases where some $y \neq x$ violates the condition.
But multiple $y$'s could violate.
Given the constraints and the nature of the problem, maybe the number of distinct elements is small? No, up to 1000.
However, note that if we pick 2 from left, they could be same or different.
Let's restructure:
Iterate $x$.
Iterate $i$ where $nums[i] == x$.
Calculate $cL = i - (\text{count of } x \text{ in } 0..i-1)$. Wait, $cL$ is count of $x$ in left.
Let $cntL = \text{count of } x \text{ in } nums[0:i]$.
Let $cntR = \text{count of } x \text{ in } nums[i+1:n]$.
We need to choose 2 from left, 2 from right.
Let $k_L$ be number of $x$'s chosen from left ($0 \le k_L \le \min(2, cntL)$).
Let $k_R$ be number of $x$'s chosen from right ($0 \le k_R \le \min(2, cntR)$).
Total $x$'s $K = k_L + k_R + 1$.
We need to choose $2-k_L$ non-$x$ from left and $2-k_R$ non-$x$ from right.
Let $nonL = i - cntL$, $nonR = (n-1-i) - cntR$.
Number of ways to choose non-$x$ from left: $\binom{nonL}{2-k_L}$.
Number of ways to choose non-$x$ from right: $\binom{nonR}{2-k_R}$.
Now, for the chosen non-$x$ elements, we must ensure no $y \neq x$ appears $\ge 2$ times.
The chosen non-$x$ elements are a set of size $(2-k_L) + (2-k_R)$.
Let $S = (2-k_L) + (2-k_R)$.
If $S=0$ (i.e., $k_L=2, k_R=2$, $K=5$), condition holds.
If $S=1$, condition holds (max count 1).
If $S=2$, we need the two elements to be distinct.
If $S=3$, we need no element to appear $\ge 2$ times.
If $S=4$, we need no element to appear $\ge 2$ times.

This looks like we need to count ways to pick specific counts.
Given $N=1000$, $O(N^2)$ is fine.
We can precompute for each $x$:
- List of indices.
- For each $i$ in indices:
  - $cntL, cntR$.
  - $nonL, nonR$.
  - We need to sum over $k_L, k_R$ the product of combinations, multiplied by the probability that the non-$x$ parts are valid.
  - Validity depends on the specific values in left and right.
  - This seems hard to do efficiently for each $i$.

Alternative:
Since $N$ is small, maybe we can iterate over all pairs of indices $(i, j)$ with $i < j$ and treat them as the two $x$'s?
No, the middle is fixed.
Let's go back to: Iterate $x$. Iterate $i$ (middle).
For fixed $x, i$, we need to choose 2 from left, 2 from right.
Let $L$ be the list of values in $0..i-1$, $R$ in $i+1..n-1$.
We need to choose $l_1, l_2 \in L$ and $r_1, r_2 \in R$.
Condition: No $y \neq x$ appears $\ge 2$ times in $\{l_1, l_2, r_1, r_2\}$.
This is equivalent to: The multiset $\{l_1, l_2, r_1, r_2\}$ has no duplicates for any $y \neq x$.
This means:
- $l_1 \neq l_2$ (if $l_1=l_2=y$, then count($y$)=2).
- $r_1 \neq r_2$.
- $l_1 \neq r_1$ and $l_1 \neq r_2$ and $l_2 \neq r_1$ and $l_2 \neq r_2$.
Wait, if $l_1 = l_2 = y$, then count($y$)=2. If $x$ count is 2, then $2 > 2$ false. So if $x$ count is 2, we cannot have any duplicate $y$.
If $x$ count is 3, we can have one $y$ with count 2? No, $3 > 2$ is true. So if $x$ count is 3, we can have one pair of $y$'s.
If $x$ count is 4, we can have one pair of $y$'s? Yes. Can we have two pairs? No, only 4 slots. If two pairs, $y$ and $z$, then $x$ count must be $>2$, which is true. But we only have 4 slots. If we have two pairs, then $x$ count is 1? No, $x$ is the middle.
Let's re-evaluate based on $K$ (count of $x$).
$K = k_L + k_R + 1$.
$k_L \in \{0, 1, 2\}$, $k_R \in \{0, 1, 2\}$.
$K \in \{1, 2, 3, 4, 5\}$. But $K \ge 2$ for unique mode.
So $k_L + k_R \ge 1$.
Cases:
1. $K=2$ ($k_L+k_R=1$): No $y \neq x$ can appear $\ge 2$ times.
   So $l_1, l_2$ must be distinct and not equal to any $r$. Also $r_1, r_2$ distinct.
   Actually, if $K=2$, we have 1 $x$ from left/right and 1 non-$x$ from left/right? No.
   If $k_L=1, k_R=0$: We pick 1 $x$ from left, 1 non-$x$ from left. And 2 non-$x$ from right.
   Total non-$x$: 3. They must be distinct.
2. $K=3$ ($k_L+k_R=2$): No $y \neq x$ can appear $\ge 3$ times.
   Since we pick 4 non-$x$ slots? No, total 4 slots. $x$ takes $k_L+k_R$ of them? No, $x$ takes $k_L$ from left, $k_R$ from right.
   The non-$x$ slots are $2-k_L$ from left and $2-k_R$ from right.
   Total non-$x$ count = $4 - (k_L+k_R) = 4 - (K-1) = 5-K$.
   If $K=3$, non-$x$ count = 2. These 2 must not be the same value.
   If $K=4$, non-$x$ count = 1. Always valid.
   If $K=5$, non-$x$ count = 0. Always valid.

So:
- If $K=5$ ($k_L=2, k_R=2$): Any choice of 2 from left (which are $x$) and 2 from right (which are $x$) works.
  Ways: $\binom{cntL}{2} \times \binom{cntR}{2}$.
- If $K=4$ ($k_L+k_R=3$): One of $k_L, k_R$ is 2, other is 1.
  Non-$x$ count = 1. Always valid.
  Ways:
  - $k_L=2, k_R=1$: $\binom{cntL}{2} \times \binom{cntR}{1} \times \binom{nonR}{1}$.
  - $k_L=1, k_R=2$: $\binom{cntL}{1} \times \binom{nonL}{1} \times \binom{cntR}{2}$.
- If $K=3$ ($k_L+k_R=2$):
  Subcases:
  - $k_L=2, k_R=0$: Non-$x$ count = 2. Must be distinct.
    Ways: $\binom{cntL}{2} \times \binom{nonR}{2}$ minus cases where the 2 from right are same.
    Actually, we choose 2 from right. They must be distinct and not equal to each other.
    Wait, the condition is "no $y \neq x$ appears $\ge 2$ times".
    If we choose 2 from right, and they are same ($y, y$), then count($y$)=2. Since $K=3$, $3 > 2$ is true. So this is ALLOWED?
    Re-read: "unique mode". Mode is the element with max frequency. Unique mode means only one element has max frequency.
    If $x$ appears 3 times, and $y$ appears 2 times, max freq is 3 (for $x$). Unique mode is $x$. Correct.
    So if $K=3$, we can have one pair of $y$'s.
    The only forbidden case is if some $y$ appears $\ge 3$ times.
    Since we only pick 2 from right and 0 from left (for this subcase), max count for any $y$ is 2. So always valid.
  - $k_L=1, k_R=1$: Non-$x$ count = 2. One from left, one from right.
    Forbidden if $l_1 = r_1$ (or $r_2$).
    So we need $l_1 \neq r_1$ and $l_1 \neq r_2$ and $l_2 \neq r_1$ and $l_2 \neq r_2$.
    Actually, we pick 1 non-$x$ from left ($l$) and 1 non-$x$ from right ($r$).
    We need $l \neq r$.
  - $k_L=0, k_R=2$: Symmetric to $k_L=2, k_R=0$.
- If $K=2$ ($k_L+k_R=1$):
  Subcases:
  - $k_L=1, k_R=0$: Non-$x$ count = 3. (1 from left, 2 from right).
    Forbidden if any $y$ appears $\ge 2$ times.
    So the 2 from right must be distinct from each other, and distinct from the 1 from left.
    Also, the 2 from right must not be equal to each other.
    And the 1 from left must not equal the 2 from right.
  - $k_L=0, k_R=1$: Symmetric.

This is getting complex. Given $N=1000$, maybe we can just iterate $x$, then iterate $i$, and for each $i$, compute the valid combinations by iterating over possible counts of non-$x$?
Actually, the constraints on non-$x$ are only about duplicates.
For a fixed $x, i$:
We can precompute the number of ways to choose $k$ non-$x$ elements from left such that no duplicates exist? No, we need to combine with right.
Maybe simpler:
For fixed $x, i$:
Total ways = $\sum_{k_L, k_R} (\text{ways to choose } k_L \text{ x's from left}) \times (\text{ways to choose } 2-k_L \text{ non-x from left}) \times (\text{ways to choose } k_R \text{ x's from right}) \times (\text{ways to choose } 2-k_R \text{ non-x from right})$.
But we need to subtract cases where some $y \neq x$ appears $\ge 2$ times.
Since we only pick 2 from left and 2 from right, the only way a $y$ appears $\ge 2$ times is:
1. $y$ appears 2 times in left.
2. $y$ appears 2 times in right.
3. $y$ appears 1 time in left and 1 time in right.

Let $Ways(L, k, \text{distinct})$ be the number of ways to choose $k$ elements from left such that no two are equal.
But we also need to ensure no overlap with right.
This suggests we can't easily separate.

Given the time limit and complexity, maybe there's a simpler observation.
The problem is from a contest (likely LeetCode 3085 or similar).
The intended solution is likely $O(N^2)$ or $O(N \log N)$.
Iterate $x$.
For each $x$, we want to count subsequences.
Let's use the property that $N$ is small.
We can iterate over all pairs of indices $(i, j)$ with $i < j$ and consider them as the two $x$'s? No, middle is fixed.
Let's stick to iterating $x$ and $i$ (middle).
For fixed $x, i$:
Let $L$ be the list of values in $0..i-1$, $R$ in $i+1..n-1$.
We need to choose 2 from $L$, 2 from $R$.
Let $cntL$ be count of $x$ in $L$, $cntR$ in $R$.
Let $nonL = i - cntL$, $nonR = (n-1-i) - cntR$.
We iterate $k_L \in [0, \min(2, cntL)]$, $k_R \in [0, \min(2, cntR)]$.
If $k_L + k_R + 1 < 2$, continue.
Let $remL = 2 - k_L$, $remR = 2 - k_R$.
We need to choose $remL$ from $nonL$ and $remR$ from $nonR$.
Let $S$ be the multiset of these choices.
We need to check if any $y \neq x$ appears $\ge 2$ times in $S \cup \{x\}$.
Actually, since $x$ is the middle, and we are counting specific subsequences, we just need to ensure that in the final multiset of 5 elements, $x$ is the unique mode.
This means:
- Count($x$) > Count($y$) for all $y \neq x$.
Since Count($x$) = $k_L + k_R + 1$.
And max Count($y$) in the chosen non-$x$ elements must be $< k_L + k_R + 1$.
Since we only choose 4 non-$x$ elements max, the max count for any $y$ is at most 4.
If $k_L + k_R + 1 \ge 3$, then max count for $y$ can be 2 (since $2 < 3$).
If $k_L + k_R + 1 = 2$, then max count for $y$ must be 1.
So:
- If $K \ge 3$: Always valid? No, if $K=3$, max count for $y$ can be 2. $3 > 2$ ok. If $K=3$, can we have $y$ with count 3? No, only 4 slots for non-$x$. So max count for $y$ is 2. So for $K \ge 3$, any choice of non-$x$ is valid?
  Wait, if $K=3$, non-$x$ count is 2. Max count for $y$ is 2. $3 > 2$ ok.
  If $K=4$, non-$x$ count is 1. Max count 1. $4 > 1$ ok.
  If $K=5$, non-$x$ count is 0. Ok.
  So for $K \ge 3$, all combinations are valid.
- If $K=2$: non-$x$ count is 3. We need max count for $y$ to be 1.
  So no $y$ can appear 2 or 3 times.
  This means:
  - The 2 from right must be distinct.
  - The 1 from left must be distinct from the 2 from right.
  - Also, if we choose 2 from left and 0 from right (not possible for $K=2$ since $k_L+k_R=1$), wait.
  For $K=2$, $k_L+k_R=1$.
  Case 1: $k_L=1, k_R=0$. $remL=1, remR=2$.
    We choose 1 from left, 2 from right.
    Condition: The 2 from right must be distinct, and the 1 from left must not equal the 2 from right.
  Case 2: $k_L=0, k_R=1$. $remL=2, remR=1$.
    Symmetric.

So the algorithm:
1. Precompute counts of each number.
2. Initialize ans = 0.
3. For each distinct $x$:
   For each index $i$ where $nums[i] == x$:
     $cntL = \text{count of } x \text{ in } 0..i-1$.
     $cntR = \text{count of } x \text{ in } i+1..n-1$.
     $nonL = i - cntL$.
     $nonR = (n-1-i) - cntR$.
     
     # Case K=5 (kL=2, kR=2)
     if $cntL \ge 2$ and $cntR \ge 2$:
       ans += $\binom{cntL}{2} \times \binom{cntR}{2}$
     
     # Case K=4 (kL+kR=3)
     # kL=2, kR=1
     if $cntL \ge 2$ and $cntR \ge 1$:
       ways = $\binom{cntL}{2} \times \binom{cntR}{1} \times \binom{nonR}{1}$
       ans += ways
     # kL=1, kR=2
     if $cntL \ge 1$ and $cntR \ge 2$:
       ways = $\binom{cntL}{1} \times \binom{nonL}{1} \times \binom{cntR}{2}$
       ans += ways
       
     # Case K=3 (kL+kR=2)
     # kL=2, kR=0
     if $cntL \ge 2$ and $cntR \ge 0$:
       # remL=0, remR=2. Choose 2 from right. Always valid (max count 2 < 3).
       ways = $\binom{cntL}{2} \times \binom{nonR}{2}$
       ans += ways
     # kL=0, kR=2
     if $cntL \ge 0$ and $cntR \ge 2$:
       ways = $\binom{cntL}{0} \times \binom{nonL}{2} \times \binom{cntR}{2}$
       ans += ways
     # kL=1, kR=1
     if $cntL \ge 1$ and $cntR \ge 1$:
       # remL=1, remR=1. Choose 1 from left, 1 from right.
       # Must be distinct.
       # Total ways = nonL * nonR - (ways where left_val == right_val)
       # Count pairs (l, r) with l != r.
       # Sum over all distinct values v: count(v in nonL) * count(v in nonR) is the number of pairs with l=r=v.
       # So valid = nonL * nonR - sum(count(v in nonL) * count(v in nonR)) for v != x.
       # We can precompute this sum.
       total_pairs = nonL * nonR
       overlap = 0
       for v in distinct_values:
         if v == x: continue
         cL_v = count of v in 0..i-1
         cR_v = count of v in i+1..n-1
         overlap += cL_v * cR_v
       ways = total_pairs - overlap
       ans += ways * $\binom{cntL}{1} \times \binom{cntR}{1}$
       
     # Case K=2 (kL+kR=1)
     # kL=1, kR=0
     if $cntL \ge 1$ and $cntR \ge 0$:
       # remL=1, remR=2. Choose 1 from left, 2 from right.
       # Condition: 2 from right distinct, and left != both right.
       # Ways to choose 2 distinct from right: $\binom{nonR}{2}$.
       # For each pair (r1, r2), we need left != r1 and left != r2.
       # This is equivalent to: total ways to choose 1 from left (nonL) minus those equal to r1 or r2.
       # Sum over all pairs (r1, r2) distinct: (nonL - count(r1) - count(r2) + count(r1==r2? no))
       # Actually, simpler:
       # Total ways = sum over all pairs (r1, r2) distinct in right: (nonL - count(r1) - count(r2) + 1 if r1==r2? no, r1!=r2)
       # = sum (nonL - count(r1) - count(r2))
       # = $\binom{nonR}{2} \times nonL - \sum_{pairs} (count(r1) + count(r2))$
       # = $\binom{nonR}{2} \times nonL - \sum_{v} count(v) \times (\text{number of pairs containing v})$
       # Number of pairs containing v in right: (nonR - 1) * (count(v in right) - 1)? No.
       # Number of pairs in right containing a specific value v:
       # If we fix one element to be v, we need to choose another from the remaining nonR-1 elements.
       # But we are choosing 2 distinct elements.
       # Number of pairs containing at least one v:
       # If we choose v and w (w != v): count(v) * (nonR - count(v)).
       # Sum over v: count(v) * (nonR - count(v)).
       # But this counts pairs with two v's? No, we choose distinct.
       # Actually, for each pair (r1, r2), we subtract count(r1) + count(r2).
       # Sum over all pairs: $\sum_{r1 \neq r2} (count(r1) + count(r2)) = \sum_{v} count(v) \times (\text{number of pairs containing v})$.
       # Number of pairs containing v: (nonR - 1) * (count(v) - 1)? No.
       # We choose 2 distinct indices. One of them has value v.
       # Number of ways to choose the other index: nonR - 1.
       # But we must ensure the other index does not have value v? No, if it has value v, then r1=v, r2=v, but we require distinct indices with distinct values?
       # No, the condition is "2 from right distinct" means distinct values? No, distinct indices with distinct values?
       # "No y appears >= 2 times". If we choose 2 indices with same value v, then count(v)=2.
       # For K=2, we need count(y) <= 1. So we cannot choose 2 indices with same value.
       # So we must choose 2 indices with distinct values.
       # So the pair (r1, r2) must have r1 != r2 (values).
       # So we are choosing 2 distinct values from right.
       # Number of ways to choose 2 distinct values from right: $\binom{nonR}{2}$? No, that's if all non-x are distinct.
       # We need to choose 2 indices with distinct values.
       # Total ways to choose 2 indices from right: $\binom{nonR}{2}$.
       # Subtract ways where both have same value: $\sum_v \binom{count(v)}{2}$.
       # Let $validR = \binom{nonR}{2} - \sum_v \binom{count(v)}{2}$.
       # For each such pair (v1, v2), we need left != v1 and left != v2.
       # Number of valid left choices: nonL - count(v1) - count(v2).
       # Sum over all valid pairs (v1, v2): (nonL - count(v1) - count(v2)).
       # = validR * nonL - \sum_{v1, v2 distinct} (count(v1) + count(v2)).
       # Sum_{v1, v2 distinct} count(v1) = \sum_{v1} count(v1) * (number of v2 != v1) = \sum count(v1) * (nonR - count(v1)).
       # So term = validR * nonL - \sum_v count(v) * (nonR - count(v)).
       # This is for kL=1, kR=0.
       
       # Similarly for kL=0, kR=1.

This is $O(N^2)$ if we precompute counts.
Given the constraints and the complexity, this should pass.