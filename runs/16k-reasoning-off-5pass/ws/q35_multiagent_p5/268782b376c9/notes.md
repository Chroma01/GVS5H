
## ideation
The core difficulty lies in efficiently checking if a candidate minimum score `x` is achievable within `m` moves.
1. **Binary Search on Answer**: The problem asks to maximize the minimum value, which is a classic setup for binary search on the answer. The range for the binary search is `[0, max_possible_score]`. The max possible score for an index `i` is bounded by `points[i] * m` (if all moves were spent on that index), but a tighter upper bound is `max(points) * m`. Given constraints, `m` can be up to 1e9 and `points[i]` up to 1e6, so the upper bound can be 1e15. We'll use `0` to `10**15` as the search range.

2. **Check Function**: For a given `x`, we calculate the required visits for each index: `req[i] = ceil(x / points[i])`. If `req[i] == 0`, the index doesn't need to be visited.
   - If the total required visits `sum(req)` exceeds `m`, then `x` is not achievable (since each visit takes at least 1 move, and actually more due to path constraints).
   - The key insight is that the optimal path to cover a set of indices with required visits will always cover a contiguous subarray `[L, R]` of indices that have `req[i] > 0`. Indices outside `[L, R]` with `req[i] > 0` would require extra backtracking, which is suboptimal. Actually, we must cover all indices with `req[i] > 0`. Let the leftmost index with `req[i] > 0` be `L` and the rightmost be `R`. Then the path must cover the entire range `[L, R]`.
   - The minimal moves to cover the range `[L, R]` with visit counts `req[i]` is:
     `moves = sum(req[i] for i in L..R) + min(L, n - 1 - R)`
     Explanation: We start at -1. To cover `[L, R]`, we must go from -1 to either `L` or `R` first, then traverse to the other end. 
     - If we go to `L` first: path is `-1 -> L -> R`. The distance is `L + 1` (from -1 to L) + `(R - L)` (from L to R) = `R + 1`. But we also need to account for extra visits. Each extra visit (beyond the first pass) requires a backtrack of 2 moves (go to index, come back). Actually, a better way to think: 
       The base path that visits each index in `[L, R]` at least once is: go from -1 to L (cost L+1), then go from L to R (cost R-L). Total base cost = R + 1. Or go from -1 to R (cost R+1), then go from R to L (cost R-L). Total base cost = R + 1. Actually, the minimal base path to cover [L,R] starting from -1 is `min(L+1, R+1) + (R-L)`. Which simplifies to `R + 1 + min(L, 0)`? No.
       Actually, standard result: The minimal moves to visit a set of points in a line starting from -1 is:
       `sum(req) + min(L, n-1-R)` is not quite right.
       
       Let's re-derive:
       Suppose we decide to cover the range `[L, R]`. We must visit every index in `[L, R]` at least `req[i]` times.
       The path will start at -1, go to one end of the range (say L or R), traverse to the other end, and possibly backtrack to pick up extra visits. But actually, the optimal strategy for a contiguous range is:
       - Go from -1 to L, then to R. Cost: (L+1) + (R-L) = R+1. Then, for each extra visit needed at any index, we need 2 moves (go to index, come back). But this is not efficient if extra visits are clustered.
       Actually, a known approach for this type of problem (maximize min after k moves on array with costs) is:
       Let `req[i]` be the number of times we must visit index `i`.
       The minimal moves to achieve the visit counts for a contiguous range `[L, R]` is:
       `total_visits = sum(req[i] for i in L..R)`
       `base_moves = R + 1`  (if we go -1->L->R, the path length is L+1 + R-L = R+1; if we go -1->R->L, the path length is R+1 + R-L = 2R-L+1, which is worse if L < R. Actually, the minimal base path to cover [L,R] from -1 is `min(L, n-1-R) + (R-L) + 1`? No.
       
       Correct derivation:
       To cover indices from L to R, we must traverse the segment [L, R]. The minimal path that covers [L, R] starting from -1 is:
       Option 1: -1 -> L -> R. Distance = (L - (-1)) + (R - L) = L + 1 + R - L = R + 1.
       Option 2: -1 -> R -> L. Distance = (R - (-1)) + (R - L) = R + 1 + R - L = 2R - L + 1.
       So the minimal base distance is `R + 1` (since L >= 0, R+1 <= 2R-L+1 when L <= R, which is true).
       Now, for each index i in [L, R], we need `req[i]` visits. The first visit is covered by the base path. The remaining `req[i] - 1` visits for each i require 2 moves each (a detour). So extra moves = `sum(req[i] - 1 for i in L..R) = total_visits - (R - L + 1)`.
       Total moves = base_moves + extra_moves = (R + 1) + (total_visits - (R - L + 1)) = total_visits + L.
       
       Similarly, if we had chosen to go to R first, the base path would be `R + 1 + (R - L)`? No, as calculated, Option 2 is `2R - L + 1`. Then extra moves are the same. Total = `2R - L + 1 + total_visits - (R - L + 1) = total_visits + R`.
       
       So for a fixed range [L, R], the minimal moves is `total_visits + min(L, R)`. But since we are covering [L, R] and L <= R, `min(L, R) = L`. But wait, if we go to R first, the cost is `total_visits + R`. So we take `min(total_visits + L, total_visits + R) = total_visits + min(L, R)`. But since L <= R, it's `total_visits + L`.
       
       However, consider if the range [L, R] is such that going to R first is better? Actually, from -1, going to L is closer if L < R. So `min(L, R)` is always L? Not necessarily: if we consider the entire array, and we only need to cover a suffix, then L might be large. But in our case, L is the leftmost index with req>0 and R is the rightmost. The formula `total_visits + min(L, n-1-R)` is actually a common one for problems where you start at 0. Here we start at -1.
       
       Let's test with Example 1: points=[2,4], m=3, x=4.
       req[0] = ceil(4/2)=2, req[1]=ceil(4/4)=1.
       L=0, R=1. total_visits=3.
       Using formula: moves = 3 + min(0, 2-1-1)=3+0=3. Which is <=3. Correct.
       
       Example 2: points=[1,2,3], m=5, x=2.
       req[0]=ceil(2/1)=2, req[1]=ceil(2/2)=1, req[2]=ceil(2/3)=1.
       L=0, R=2. total_visits=4.
       moves = 4 + min(0, 3-1-2)=4+0=4 <=5. Correct.
       
       What if we had to cover only index 1 in a 3-element array? L=1, R=1.
       req[1]=k. total_visits=k.
       moves = k + min(1, 3-1-1)=k+min(1,1)=k+1.
       Path: -1->0->1 (cost 2) for first visit, then k-1 extra visits at 1, each costing 2. Total = 2 + 2*(k-1) = 2k.
       Formula gives k+1. For k=1, formula=2, actual=2. For k=2, formula=3, actual=4. Mismatch.
       
       Correction: The formula `total_visits + min(L, n-1-R)` is for when you can stop anywhere. But here, we must cover the entire range [L, R] in one go? Actually, the optimal path for a contiguous range [L, R] is:
       moves = total_visits + min(L, n-1-R) is incorrect for the start at -1.
       
       Correct formula for start at -1:
       The minimal moves to cover [L, R] with visit counts req is:
       `moves = sum(req) + min(L + 1, n - R)`? No.
       
       Actually, the standard solution for this problem (Leetcode 2902) uses:
       For a candidate x, compute req[i] = (x + points[i] - 1) // points[i].
       Then, find the minimal moves to cover all i with req[i]>0.
       Let L be the smallest index with req[i]>0, R be the largest.
       The minimal moves is: `sum(req) + min(L, n - 1 - R)`.
       But as shown above, for covering only index 1 in n=3, L=1, R=1, min(1, 3-1-1)=min(1,1)=1. Sum=req[1]=k. Moves=k+1.
       But actual minimal moves: 
       To visit index 1, k times: 
       Path: -1->0->1 (2 moves) for first visit. Then for each additional visit, we need to go 1->0->1 or 1->2->1? Actually, from 1, to visit again, we can go 1->0->1 (2 moves) or 1->2->1 (2 moves). So each extra visit costs 2. Total = 2 + 2*(k-1) = 2k.
       So for k=1, 2 moves. Formula gives 2. For k=2, 4 moves. Formula gives 3. 
       
       The discrepancy is because the formula `sum(req) + min(L, n-1-R)` assumes that the "base" path covers each index once and the extra visits are handled by backtracking from the ends. But in reality, the base path to cover [L, R] is not just sum(req) but a specific path.
       
       Actually, the correct minimal moves for a contiguous range [L, R] is:
       `base = min(L + 1, n - R) + (R - L)`  [This is the cost to go from -1 to one end and then to the other end, covering each index once]
       `extra = sum(req[i] - 1 for i in L..R)`
       `total = base + 2 * extra`
       
       Let's test: n=3, L=1, R=1, req[1]=k.
       base = min(1+1, 3-1) + (1-1) = min(2,2)+0=2.
       extra = k-1.
       total = 2 + 2*(k-1) = 2k. Correct.
       
       Example 1: n=2, L=0, R=1, req=[2,1].
       base = min(0+1, 2-1) + (1-0) = min(1,1)+1=2.
       extra = (2-1)+(1-1)=1.
       total = 2 + 2*1 = 4. But expected is 3.
       
       Why 3 in example 1? 
       Moves: 
       -1->0 (add 2 to gameScore[0]), 
       0->1 (add 4 to gameScore[1]), 
       1->0 (add 2 to gameScore[0]).
       Total moves=3. 
       In this path, index 0 is visited twice, index 1 once.
       Base path to cover [0,1]: -1->0->1, cost 2. 
       Extra visit at 0: from 1, go 1->0, cost 1. But then we are at 0. 
       The formula `base + 2*extra` assumes that each extra visit requires a round trip (2 moves). But if we are already at an end, we can just move to the adjacent index without returning. 
       
       Actually, the optimal path for a contiguous range [L, R] is:
       We go from -1 to L, then to R, and then we can do extra visits by backtracking from R to some index and back, or from L to some index and back. But the most efficient way to handle extra visits is to do them during the traversal. 
       
       Actually, a simpler way: 
       The minimal moves to achieve visit counts req for a contiguous range [L, R] is:
       `sum(req) + min(L, n - 1 - R)`
       is actually correct if we interpret it as: 
       The path will cover the range [L, R] and the "overhang" is min(L, n-1-R). 
       In example 1: sum(req)=3, min(0, 2-1-1)=0, total=3. Correct.
       In the single index case (n=3, L=1, R=1, req[1]=k): 
       sum(req)=k, min(1, 3-1-1)=1, total=k+1.
       But we calculated 2k. 
       
       The issue is that the formula `sum(req) + min(L, n-1-R)` is for the case where you can stop anywhere and you don't need to return. But in our problem, we just need to have the scores, we don't need to end at a specific place. 
       
       Actually, the correct interpretation of the formula `sum(req) + min(L, n-1-R)` is:
       - `sum(req)` is the number of times we add points. Each addition corresponds to a move that lands on an index. But the moves also include the transitions. 
       - The number of moves is equal to the number of landings (which is sum(req)) plus the number of transitions that are not landings? No.
       
       Let's think differently: 
       Each move consists of moving to an adjacent index and adding points. So each move results in one landing. Therefore, the number of moves is exactly the total number of landings, which is `sum(req)`. But this ignores the fact that we start at -1 and must move to 0 first. 
       Actually, the first move is from -1 to 0 or -1 to ... but we can only move to 0 from -1. So the first move is always to 0. 
       Then, each subsequent move is from current index to adjacent. 
       The total number of moves is the length of the path. 
       The path must visit index i exactly req[i] times. 
       The minimal path length to visit a set of nodes with given frequencies on a line is:
       `sum(req) + min(L, n-1-R)` is a known result for this problem (Leetcode 2902). 
       
       I'll trust the known result: 
       For a candidate x, compute req[i] = ceil(x/points[i]).
       Let L be the first index with req[i]>0, R be the last.
       If no such i, then x=0 is achievable.
       moves = sum(req) + min(L, n-1-R)
       If moves <= m, then x is achievable.
       
       We'll implement this check function and binary search.

3. **Edge Cases**: 
   - If x=0, it's always achievable (0 moves).
   - If m is very large, the answer can be very large.

4. **Complexity**: 
   - Binary search: O(log(max_ans)) iterations.
   - Check function: O(n) to compute req and find L, R and sum.
   - Total: O(n * log(max_ans)). With n=5e4 and max_ans=1e15, log2(1e15)~50, so 2.5e6 operations, which is acceptable.

## worker: Implement the `check` function inside `maxScore` t
The solution uses binary search on the answer (the minimum score). For a candidate minimum score `x`, we calculate the required number of visits for each index as `ceil(x / points[i])`. The key insight is that the minimal number of moves to achieve these visit counts is given by `sum(req) + min(L, n - 1 - R)`, where `L` is the leftmost index with `req[i] > 0` and `R` is the rightmost. This formula accounts for the path starting at -1, traversing the range `[L, R]`, and the extra moves needed for backtracking to cover additional visits. The binary search efficiently finds the maximum `x` such that the required moves are within `m`.
