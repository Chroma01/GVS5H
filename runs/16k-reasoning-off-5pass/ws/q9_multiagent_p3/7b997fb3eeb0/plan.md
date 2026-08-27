The problem asks for the maximum number of pairs $(a, b)$ from a sorted subarray $A[L \dots R]$ such that $a \le b/2$. Since the array is sorted, a greedy strategy works: to maximize pairs, we should try to pair the smallest available element with the smallest possible larger element that satisfies the condition. However, simply pairing the global minimum with the next valid element might not be optimal if it "wastes" a small number that could have been used to satisfy a larger number later. Actually, the standard greedy approach for this specific "at most half" condition on a sorted array is to iterate from the largest element downwards. For the current largest element $b$, if there exists a smallest available $a$ such that $a \le b/2$, we pair them. If not, $b$ cannot be part of any pair as the bottom element (since all other available $a$'s are even larger or equal to the current smallest, and if the smallest doesn't work, none do). Wait, let's re-evaluate.
Correct Greedy Logic: To maximize $K$, we want to use the largest possible elements as the base ($b$) because they are easier to satisfy the $a \le b/2$ condition for a wider range of $a$. For a chosen base $b$, we should pair it with the smallest available $a$ that satisfies the condition to save larger $a$'s for potentially smaller bases? No, actually, the optimal strategy is: Iterate from the largest element in the range down to the smallest. Maintain a pointer to the smallest available element. If the current largest element $b$ satisfies $b \ge 2 \times (\text{smallest available})$, then we pair them (increment count, move smallest pointer up). If not ($b < 2 \times \text{smallest}$), then this $b$ cannot be paired with the smallest, and since the array is sorted, it cannot be paired with any other available element either (as they are all $\ge$ smallest). Thus, this $b$ is discarded. We move to the next largest.
This greedy approach can be simulated efficiently using two pointers for a static range, but since we have $Q$ queries on different ranges, we need a data structure. We can use a Segment Tree where each node stores the result of the greedy simulation for that range. Merging two nodes (left child $L$, right child $R$) involves simulating the process: the "smallest available" from the combined set is the minimum of the two leftmost availables, and we process from the rightmost availables.
Actually, the state needed to merge is just the number of pairs formed and the index of the "smallest available" element relative to the start of the range. But the "smallest available" index depends on how many were consumed from the left side.
Let's refine the merge logic. A node covering $[l, r]$ needs to return: `(pairs_formed, index_of_first_unused)`.
When merging `left` and `right`:
1. Start with `pairs = left.pairs`, `unused_idx = left.index`.
2. We have a "cursor" for the smallest available element in the `left` part.
3. We need to simulate the greedy process on the `right` part using the available elements from `left` (starting at `unused_idx`) and the elements in `right` (all of them).
Wait, the greedy strategy processes from the *largest* element downwards.
So, for a range $[L, R]$, we look at $A[R]$. Can it pair with $A[L]$? If $A[R] \ge 2*A[L]$, yes. Then we look at $A[R-1]$ and $A[L+1]$, etc.
If $A[R] < 2*A[L]$, then $A[R]$ cannot pair with $A[L]$. Can it pair with $A[L+1]$? No, because $A[L+1] \ge A[L]$. So $A[R]$ is useless. We discard $A[R]$ and try $A[R-1]$ with $A[L]$.
So the state for a segment tree node covering $[l, r]$ should be: `(count, next_start_index)`.
`count`: number of pairs formed within $[l, r]$.
`next_start_index`: the index of the first element in $[l, r]$ that was NOT used as the top element (the smallest available for the base).
When merging `left` (covering $[l, mid]$) and `right` (covering $[mid+1, r]$):
The elements available to be "tops" (small $a$) are those in `left` starting from `left.next_start_index` AND all elements in `right`? No.
The greedy strategy scans from the largest element ($r$) down to $l$.
The "tops" are picked from the smallest available.
Initially, the smallest available is $l$.
We check $A[r]$ against $A[l]$.
If match: pair them. Smallest available becomes $l+1$. Next largest is $r-1$.
If no match: $A[r]$ is discarded. Next largest is $r-1$. Smallest available is still $l$.
This process continues.
Notice that the "smallest available" only moves forward (increases index). The "largest available" only moves backward (decreases index).
In the merge of `left` and `right`:
The `right` part provides the large elements. The `left` part provides the small elements.
However, the `left` part also has its own internal pairs formed.
Let's define the function `solve(l, r)` which returns `(pairs, min_unused_index)`.
To compute `solve(l, r)`:
We know `solve(l, mid)` returns `(p1, i1)` and `solve(mid+1, r)` returns `(p2, i2)`.
The total pairs will be `p1 + p2 + extra`.
The `extra` pairs come from pairing elements from the "unused" part of `left` (starting at `i1`) with elements from the "unused" part of `right`?
Actually, the greedy strategy on $[l, r]$ is:
Iterate $k$ from $r$ down to $l$. Let current base be $A[k]$.
Find smallest unused $A[j]$ ($j \ge l$).
If $A[k] \ge 2*A[j]$, pair them, mark $j$ used, count++, $k$--.
Else, $k$--.
The crucial observation: The elements in `right` (indices $mid+1 \dots r$) are all larger than or equal to elements in `left` ($l \dots mid$).
The greedy scan starts at $r$. It will try to pair $A[r]$ with the smallest available in $[l, r]$.
The smallest available in $[l, r]$ is either the first unused in `left` (index `i1`) OR if `left` is fully consumed, the first unused in `right` (index `i2`).
But wait, if `left` is fully consumed, that means all elements in `left` were used as tops.
So, the algorithm for merging:
1. Start with `curr_l = left.next_start_index`, `curr_r = right.end_index` (which is `r`).
2. We have `left.pairs` and `right.pairs` already counted internally? No, the internal pairs in `left` and `right` were formed using elements strictly within those ranges.
   Wait, the definition of `solve(l, r)` is the max pairs using ONLY elements in $[l, r]$.
   If we split into $[l, mid]$ and $[mid+1, r]$, the pairs formed entirely within $[l, mid]$ are `left.pairs`. The pairs formed entirely within $[mid+1, r]$ are `right.pairs`.
   Can we form NEW pairs by taking a base from $[mid+1, r]$ and a top from $[l, mid]$?
   Yes. And since all elements in $[mid+1, r]$ are $\ge$ all in $[l, mid]$, the greedy strategy will prioritize using the largest from $[mid+1, r]$ as bases.
   The tops will be taken from the smallest available in $[l, mid]$ first.
   So, we take the `left` range's unused elements (starting at `left.next_start_index`) and the `right` range's elements.
   Actually, the `right` range's internal pairs are already optimal for the subset. But if we bring in tops from `left`, we might break the optimality of `right`'s internal pairs?
   No. The problem is finding the global max for $[l, r]$.
   The standard solution for this problem (often seen in competitive programming) is:
   The state is `(count, min_index)`.
   Merge `(c1, i1)` and `(c2, i2)` where `i1` is the first unused index in left, `i2` is first unused in right.
   Actually, `i2` is not needed because the right side is processed from the right end.
   Let's reconsider the merge logic carefully.
   We have a set of numbers $S = S_L \cup S_R$. $S_L < S_R$ (element-wise).
   We want to maximize pairs.
   Strategy: Take largest from $S_R$ (say $x$). Try to pair with smallest from $S_L$ (say $y$).
   If $x \ge 2y$, pair them. Remove $y$. Try next largest from $S_R$ (or same if we didn't consume it? No, we consume one base per pair).
   Actually, we consume one base ($x$) and one top ($y$).
   If $x < 2y$, then $x$ cannot pair with $y$. Since $y$ is the smallest in $S_L$, $x$ cannot pair with any in $S_L$. Can $x$ pair with something in $S_R$?
   If $x$ pairs with something in $S_R$, that something must be smaller than $x$. But we are processing from largest to smallest. If $x$ is the current largest, any other candidate in $S_R$ is smaller.
   However, the greedy choice property holds: if the largest element cannot pair with the smallest, it cannot pair with anyone. So it is discarded.
   So the algorithm is:
   1. Start with `ptr_L = i1` (first unused in left).
   2. Iterate `k` from `r` down to `mid+1` (elements of right).
      Let `base = A[k]`.
      If `ptr_L <= mid` and `A[ptr_L] <= base / 2`:
         Pair them. `ptr_L++`. `extra_pairs++`.
      Else:
         `base` is discarded.
   3. Total pairs = `left.pairs + right.pairs + extra_pairs`.
   4. The new `min_unused_index` is `ptr_L`.
   
   Is it possible that we should have used an element from `right` as a top?
   Suppose we have $S_L = \{10\}$, $S_R = \{20, 30\}$.
   Left internal: 0 pairs. Right internal: 0 pairs (20, 30 -> 30 >= 2*20? No).
   Merge:
   Base 30. Top 10. $30 \ge 20$. Pair (30, 10).
   Base 20. No tops left.
   Total 1.
   What if we paired 20 and 10? Then 30 is left. Total 1. Same.
   What if $S_L = \{10, 100\}$, $S_R = \{200, 300\}$.
   Left internal: 0. Right internal: 0.
   Merge:
   Base 300, Top 10 -> Pair.
   Base 200, Top 100 -> Pair.
   Total 2.
   Seems correct. The elements in $S_R$ are always larger, so they make better bases. The elements in $S_L$ are smaller, so they make better tops. We should greedily match the largest available base from $S_R$ with the smallest available top from $S_L$.
   What if $S_L$ runs out? Then we stop.
   What if $S_R$ runs out? Then we stop.
   So the merge logic is:
   `new_pairs = left.pairs + right.pairs`
   `curr = left.next_start_index`
   `for k from right.end_index down to right.start_index:`
       `if curr <= left.end_index and A[curr] * 2 <= A[k]:`
           `new_pairs += 1`
           `curr += 1`
   `new_next_start = curr`
   
   This looks $O(N)$ per merge, leading to $O(N^2)$ total. Too slow.
   We need $O(1)$ or $O(\log N)$ merge.
   Observation: The loop runs as long as `curr` is valid and condition holds.
   The condition is `A[curr] * 2 <= A[k]`.
   Since `A` is sorted, `A[curr]` increases as `curr` increases. `A[k]` decreases as `k` decreases.
   The condition `A[curr] * 2 <= A[k]` is monotonic?
   As `curr` increases, LHS increases. As `k` decreases, RHS decreases.
   So the condition becomes harder to satisfy.
   We are matching the sequence of bases from $S_R$ (largest to smallest) with the sequence of tops from $S_L$ (smallest to largest).
   We stop when either we run out of tops or the condition fails.
   This is equivalent to finding the longest prefix of $S_L$ (starting from `left.next_start_index`) that can be matched with a suffix of $S_R$ (starting from `right.end_index` downwards).
   Specifically, we want to find the largest `cnt` such that for all $j \in [0, cnt-1]$, `A[left.next_start_index + j] * 2 <= A[right.end_index - j]`.
   Wait, is it strictly alternating?
   Yes, because we take the largest base, then the next largest, etc., and pair with the smallest top, then next smallest, etc.
   So we need to find the largest `k` such that `A[left.next_start_index + i] * 2 <= A[right.end_index - i]` for all $0 \le i < k$.
   This is equivalent to `max_{0<=i<k} (A[left.next_start_index + i] * 2) <= min_{0<=i<k} (A[right.end_index - i])`.
   Actually, since both sequences are sorted, we just need to check the "tightest" constraints?
   No, we need the condition to hold for ALL pairs.
   So we need `A[left.next_start_index + i] * 2 <= A[right.end_index - i]` for all $i < k$.
   This implies `A[left.next_start_index + i] * 2 <= A[right.end_index - i]`.
   Since LHS is increasing and RHS is decreasing, the condition is most likely to fail at the largest $i$.
   So we just need to find the largest $k$ such that `A[left.next_start_index + k - 1] * 2 <= A[right.end_index - (k - 1)]`.
   Wait, if it holds for $k-1$, does it hold for $0 \dots k-2$?
   LHS at $i$ is smaller than LHS at $i+1$. RHS at $i$ is larger than RHS at $i+1$.
   So if `A[L+i]*2 <= A[R-i]`, then for any $j < i$, `A[L+j]*2 <= A[L+i]*2 <= A[R-i] <= A[R-j]`.
   Yes! The condition is monotonic. We just need to find the largest $k$ such that `A[left.next_start_index + k - 1] * 2 <= A[right.end_index - (k - 1)]`.
   This can be solved with binary search on $k$.
   Range of $k$: $0$ to $\min(\text{len}(S_L), \text{len}(S_R))$.
   So merge is $O(\log N)$. Total time $O(N \log N)$.
   Query is $O(\log N \cdot \log N)$ or $O(\log N)$ with fractional cascading?
   Standard segment tree query combines $O(\log N)$ nodes. Each merge is $O(\log N)$. Total $O(Q \log^2 N)$.
   With $N, Q = 2 \cdot 10^5$, $\log^2 N \approx 324$, operations $\approx 6 \cdot 10^7$, which is acceptable for 2 seconds in Python if optimized, or definitely in C++. In Python, might be tight.
   Can we optimize the query?
   The query combines nodes from top to bottom. The order matters?
   The merge operation is associative?
   Let $f(A, B)$ be the merge of range $A$ and range $B$.
   Is $f(f(A, B), C) == f(A, f(B, C))$?
   The logic depends on the split point.
   If we have ranges $[1, 2], [3, 4], [5, 6]$.
   $f([1,2], [3,4])$ merges them. Then merge with $[5,6]$.
   This corresponds to processing bases from $[3,4]$ then $[5,6]$?
   No, the merge logic assumes the left part is strictly smaller than the right part.
   In a segment tree, the left child covers $[l, mid]$ and right child $[mid+1, r]$. All elements in left are $\le$ all in right.
   So the merge logic is valid for any node.
   For a query $[L, R]$, we decompose it into $O(\log N)$ canonical nodes.
   We must process them in order from left to right (smallest to largest) to maintain the invariant that the accumulated "left" part is smaller than the "right" part being added.
   So we collect the nodes, sort them by their starting index (they are naturally sorted if we traverse the tree correctly), and merge sequentially.
   Complexity: $O(Q \log^2 N)$.
   
   Implementation details:
   - Build segment tree. Each node stores `(pairs, next_start_index)`.
   - `next_start_index` is relative to the node's start? Or absolute index? Absolute is easier for the binary search condition `A[idx]`.
   - Actually, storing absolute indices is fine.
   - Binary search range for $k$: low=0, high=min(len_left, len_right).
   - Check function: `A[left_start + k - 1] * 2 <= A[right_end - (k - 1)]`.
   - Be careful with indices.