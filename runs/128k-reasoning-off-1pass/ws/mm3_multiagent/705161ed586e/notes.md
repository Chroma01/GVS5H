
## ideation
**Core difficulty:**  
We must transform a string into a “good” string (every character appears in runs of length ≥ 3) by repeatedly changing a character to its immediate predecessor or successor in the alphabet. Each change costs 1. We need the minimum cost, and among all minimal-cost solutions, the lexicographically smallest result. If no good string is reachable, return "".

**Key observations:**
- Allowed character changes are only ±1 in the alphabet, so any character `c` can be reached from the original character `o` only if `|c - o|` ≤ something, but we can just consider all 26 letters as possible targets at each position, because the cost is just the absolute difference in alphabet index. (Moving further than necessary is suboptimal but may be needed for lexicographic minimality when costs tie? We must still consider all 26 to be safe, but we can prune.)
- The “good” condition is a local property on runs: each maximal block of equal characters must have length at least 3. So we can formulate this as a DP where we decide the character at each position, and we must ensure that when we finish a run, its length is at least 3.
- Lexicographic ordering matters: when two solutions have the same minimal cost, we must pick the smaller string. This means we need to store the actual string (or a representation) for each DP state, not just the cost.

**State design:**  
`dp[i][c][k]` = the best (minimum cost, then lexicographically smallest string) for the prefix of length `i` (i.e., after processing positions `0..i-1`), where the last character is `c`, and the current run of `c` has length `k` (k = 1, 2, or ≥3, but we can cap at 3). For k ≥ 3 we just treat it as "≥3" because extending a long run doesn't change anything.

**Transitions:**  
To compute `dp[i+1][c'][k']` from `dp[i][c][k]`:
- We can either continue the run: if `c' == c`, then `k' = min(k+1, 3)`, cost added = `|orig[i] - c'|`.
- Or start a new run: if `c' != c`, then we require that the previous run `k` was ≥ 3 (otherwise invalid), and `k' = 1`, cost added = `|orig[i] - c'|`.

**Initial state:**  
`dp[0]` is empty; for the first character we can start with any `c` and run length 1.

**Result:**  
After processing all `n` characters, we look at all states with run length ≥ 3, and pick the one with minimum cost; if tie, lexicographically smallest string. If no such state exists, return "".

**Complexity:**  
- States: `n * 26 * 3`.
- Transitions per state: 26 (for each possible next character).
- Total: O(26² * n) ≈ 3.4e7 for n=5e4, which is acceptable in Python with optimizations (e.g., using arrays instead of strings for the path, or only considering reachable characters). Actually 3.4e7 might be tight in Python, but we can optimize: we only need to consider characters that are within a small range of the original character because the cost is the absolute difference. Since we want lexicographically smallest, we might need to consider all 26, but we can prune: for a given position, any target character `c` with cost larger than the minimum possible for that position is dominated unless it helps with future runs. However, to be safe, we keep all 26 and rely on the tie-breaking to pick the lexicographically smallest. But we can also observe that the cost of moving to a far character is high, and it can only be optimal if we have a long run of that character later. But implementing that is complex; the 26²·n solution is simpler and should pass within time limits if optimized.

**Optimization:**  
- Use lists of size 26*3 for each position, storing (cost, parent_pointer, char). We can store the actual string only for the final answer, or store a backpointer and reconstruct.
- But for lexicographic tie-breaking, we can store the string directly if we keep only the best for each state. Since n=5e4 and 26*3=78 states, storing strings of length up to 5e4 for each is memory-heavy: 78 * 5e4 * ~50 bytes ≈ 195 MB, which is too much.
- Better: store backpointers and character, and at the end reconstruct the string for the chosen best state. But we need to compare lexicographic order during DP to break ties among equal costs. To compare lexicographically, we can store the string up to the current position, but that's too big. Alternative: we can delay lexicographic comparison to the end by noting that among equal costs, the lexicographically smallest string is the one that at the first differing position has the smaller character. This can be encoded as a tuple of characters, but we can store a "hash" or "representative". However, the simplest correct approach is to keep the actual string for each state, because 78 * 5e4 = 3.9 million characters, which is about 4 MB, plus overhead, maybe 20-30 MB. Actually 5e4 * 78 = 3.9e6, each character is 1 byte, so ~4 MB. But Python strings have overhead: each string object takes about 49 bytes + characters. So 78 * 5e4 = 3.9 million strings? No, we have 78 states per position, so total states across all positions: n * 78 = 3.9 million states. Each state would hold a string of length i, which is huge memory. So we cannot store full strings for all states.

**Better approach for lexicographic tie-breaking:**  
We can use a "rolling hash" or just store the string only for the best candidates? But we need to compare any two states at the same i. Since n is 5e4, we can store the string for each state, but we can use a trick: store the string as a bytearray or list of characters, and share suffixes? Actually, we can store the character and a backpointer to the previous state. Then for two states with the same cost, to decide which is lexicographically smaller, we need to compare their strings. We could compare them by walking back the linked list, but that's O(n) per comparison, too slow.

**Alternative:** Since the alphabet is small (26), we can use the fact that the DP cost is additive and the transition only depends on the last character and run length. The lexicographic order is determined by the sequence of characters. We can break ties by preferring smaller characters at each position. That is, if we process positions from left to right, and when costs are equal, we keep the state that has the smaller character at the current position? No, lexicographic order is determined by the whole string, not just the current character. For example, "ab" vs "aa": they differ at position 1, "aa" is smaller. So if at some position we have a tie in cost, we cannot just compare the current character; we need to know the entire prefix. However, we can use a suffix array or something? Actually, we can use a trick: since we process left to right, and we only care about the minimal cost, we can keep for each state the actual string, but we can store it as a reference to a previous string plus one character. But we still need to compare strings. Wait, we can use a "trie" of suffixes? Not needed.

**Practical solution:** Use a DP where for each state we store the cost and the string, but we can use Python's small integers and store the string as a list of characters (or a bytearray) and use memoization? But memory is the issue. Let's calculate: n=5e4, 26*3=78 states per position. If we store a string of length i for each state, total memory is sum_{i=1}^n (78 * i) = 78 * n(n+1)/2 ≈ 78 * 1.25e9 = 9.75e10 characters, impossible. So we cannot store all strings.

We need a way to compare strings without storing them fully. One idea: use a suffix comparison method, but we need to do it many times.

**Better idea:** Since the transition only depends on the last character and run length, the DP graph is a DAG. The lexicographically smallest string among those with minimum cost is the lexicographically smallest path in the DAG. This is equivalent to: after finding the minimum cost, we can do a second pass to find the lexicographically smallest string with that cost. Or we can incorporate lexicographic order into the DP by using a custom comparison: when costs are equal, we compare the strings, but we can do that by maintaining a "hash" or by storing the string in a compressed way. However, we can note that the number of states is small (78), so we can store for each state the entire string, but we can do it for only the current layer and next layer? No, we need all layers for the final reconstruction. But we can do DP with only storing the string for the current position, and keep backpointers. Then for tie-breaking, we need to compare two strings. We can compare two strings by walking back from the end to the first differing character. Since the maximum length is 5e4, and we might do this many times, it could be slow. But we can optimize: we can store for each state not only the cost but also a "rank" or "hash" that allows comparison. For example, we can store a tuple of (cost, string) but we can't store string. Alternatively, we can use a "suffix array" style: since the alphabet is small, we can store the string as a list of characters and use a rolling hash to compare quickly, but that might be overkill and still need to store the string? Actually, we can store a hash of the string, but that doesn't give total order.

**Wait, is lexicographic tie-breaking even needed?** Yes, the problem asks for it. But maybe we can argue that the optimal string can be found by a greedy approach? Not obviously, because the cost of changing to a smaller character might be higher now but allow cheaper changes later? But cost is linear and independent per position, so there is no future cost saving. The total cost is sum of absolute differences. The "good" condition couples adjacent positions. So it's a shortest path problem in a graph where edge weight is the cost to change the character. The graph is: nodes are (position, char, run_length). Edges: from (i, c, k) to (i+1, c', k') with weight |orig[i] - c'|, valid if (c'==c and k'=min(k+1,3)) or (c'!=c and k>=3 and k'=1). We want the shortest path from start to any node at i=n with run_length>=3. Lexicographic smallest among those.

**Tie-breaking in shortest path:** We can use a modified Dijkstra/BFS since all edge weights are non-negative integers (0 to 25). But we have 5e4 * 78 = 3.9e6 nodes, edges are 26 per node, so ~1e8 edges, too many for Dijkstra. But we can use DP because the graph is a DAG (edges only go forward). So we can do DP in order of position. For each position i, we compute the best cost and string for each (c, k). To compare strings, we can store the string explicitly for each node, but we can use a trick: we only need to store the string for the current position, and we can keep an array of strings for all states at all positions? That's too big.

**Observation:** The number of states is small: 26*3=78. For each position i, we have 78 states. Instead of storing the string for each state, we can store a backpointer (previous state) and a character. Then to compare two strings, we can walk back from the end to the first differing character. The maximum length of a string is 5e4. The number of comparisons we do: at each position, for each next character, we might compare the resulting string with the current best for that target state. That's 26*78 = ~2000 comparisons per position. Each comparison might take O(n) in the worst case, leading to O(n^2) = 2.5e9, too slow.

**We need a way to compare strings faster.** We can use a "suffix array" or "rolling hash" with binary search, but we need a total order. Since the alphabet is small, we can use a "double hashing" to compare strings in O(log n) time after O(n) preprocessing. But the preprocessing for each state is too much.

**Alternative:** Since the DP is over a small number of states, we can store the actual string for each state, but we can do it in a compact way: use a bytearray for the string, and store for each state a reference to the bytearray and an offset? But each state has a different string. However, we can use a "persistent data structure" or "rope" but that's complex.

**Wait, maybe the problem constraints allow O(n * 26) states and we can store the string as a Python string for each state if we only store it for the current layer and next layer?** No, because at the end we need the full string for the best state. We can keep backpointers and then reconstruct at the end. For the reconstruction, we only need one string. So during DP, we can keep for each state: cost, and a backpointer (which could be a tuple of (prev_state_index, char)). We also need to know the full string for tie-breaking. But we can avoid tie-breaking during DP by noting that if we always keep the lexicographically smallest string for a given cost, we can use a custom comparator that, when costs are equal, compares the strings. But we can compare the strings by walking back the linked list until we find a difference. The length of the walk is at most n. But we can do this efficiently by maintaining for each state a "hash" of the string, and also a "length". But we need total order, not just equality. We can use a "rolling hash" and store the hash, but that doesn't give total order. However, we can use a "string representation" like a tuple of (length, hash, maybe a sample), but that might not be sufficient for total order.

**Another idea:** Since the cost is the sum of absolute differences, and the "good" condition only cares about run lengths, we can think of this as a labeling problem. The lexicographically smallest string with minimum cost can be found by first finding the minimum cost, and then doing a greedy construction: at each position, choose the smallest possible character that can lead to a solution with the overall minimum cost. This is a standard approach in such problems: compute the minimum cost DP (just the cost), then reconstruct the lexicographically smallest string by iterating from left to right, at each position trying characters from 'a' to 'z', and checking if it's possible to achieve the global minimum cost from that choice. But checking "possible" requires another DP from right to left, or we can use the DP cost we already computed. Specifically, we can compute `dp[i][c][k]` = min cost to complete the suffix from i to end, given that at position i we start with character c and run length k. Then during reconstruction, at position i, we try each character c' in alphabetical order, and for each we check if there exists a state (c', k') at i such that the total cost (dp[i][c'][k'] + cost_to_reach_this_state) equals the global minimum. But we also need to know the run length of the previous character to compute the transition. Actually, we need to know the state at position i: (prev_char, prev_k) and we choose current_char. So we need to know dp[i][current_char][current_k] for all possible k. We can compute forward DP for the minimum cost to reach each state at position i, and backward DP for the minimum cost from each state at position i to the end. Then the total cost for a path is the sum. But we need to combine them. This is like a standard DP with lexicographic reconstruction: compute the minimal cost, then for each position, determine the character that allows the minimal cost, choosing the smallest character that works.

But we also need to ensure the "good" condition: runs must be at least 3. In the backward DP, we need to incorporate the run length condition. This is doable but a bit involved.

**Let's design the backward DP:**  
Let `back[i][c][k]` = minimum cost to transform the suffix from i to n-1 into a good string, given that at position i we are about to place a character c, and the run length of c at position i is k (k=1,2,3+). But we need to be careful: the state at i includes the character at i. The transition: from state (i, c, k), we choose the character at position i (which is c) with cost |orig[i] - c|. Then we go to state (i+1, c', k') as before. This is exactly the same as forward DP but starting from i. So we can compute `back[i][c][k]` for i from n down to 0, with base case at i=n: if we have finished, the state is "done", and the cost is 0 if the last run length k >= 3, else infinity. Actually, at i=n, we are past the last character, so we need to check that the run length of the last character is at least 3. So for any state at i=n, the cost is 0 if k>=3, else infinity. For i < n, we have:
`back[i][c][k] = |orig[i] - c| + min over c', k' of back[i+1][c'][k']` subject to valid transitions: (c'==c and k' = min(k+1,3)) or (c'!=c and k>=3 and k'=1).
This is exactly the same recurrence as forward DP but in reverse. The only difference is that at the start (i=0), we have no previous character, so we can start with any c and k=1. So the global minimum cost is `min_{c,k} back[0][c][k]` with the condition that k=1 (since no previous run). Actually, at i=0, we start with a new run, so k must be 1. So the global min cost is `min_c back[0][c][1]`.

**Reconstruction:** Once we have the global min cost, we can reconstruct the string from left to right. At position i, we know the previous character prev_c and previous run length prev_k. We want to choose the current character c (from 'a' to 'z') such that:
- The transition is valid: either c == prev_c and new_k = min(prev_k+1, 3), or c != prev_c and prev_k >= 3 and new_k = 1.
- The total cost (forward_cost to reach this state + |orig[i] - c| + back[i+1][new_c, new_k]) equals the global min cost. But we don't have forward_cost stored. However, we can use the fact that the global min cost is the min over all paths. We can just check if there exists a completion from the state (i+1, new_c, new_k) with the remaining cost. But we need to know the forward cost to ensure that the path is actually part of a globally optimal path. This is a common issue: the state at i might be reachable with a cost that is not minimal for that state, but the combination might be globally optimal. For example, a state (c,k) at i might have a higher forward cost than the minimum for that state, but the transition to the next character might be forced, and the backward cost from there is low, making the total exactly the global min. In standard DP, if we keep only the minimum cost for each state, we might miss such paths. However, in this problem, the forward cost to a state is independent of future choices? No, the forward cost to a state is exactly the sum of |orig[j] - chosen_char[j]| for j=0..i-1. The backward cost is for j=i..n-1. The total cost is the sum. If we keep only the minimum forward cost for each state, then when we are at position i and we want to check if choosing c at i is part of a globally optimal path, we need to consider the minimum forward cost to reach (c, k) at i. But if the global optimal path uses a forward cost to (c,k) that is not the minimum for that state, then our check would fail. However, can that happen? Suppose there is a globally optimal path that reaches state (c,k) at i with forward cost F, but the minimum forward cost to (c,k) is F' < F. Then the backward cost from (c,k) to the end in that globally optimal path is B, so total = F + B = global_min. Since F' < F, then F' + B < global_min, contradicting that global_min is the minimum over all paths. Therefore, for any globally optimal path, the forward cost to each state it visits must be the minimum forward cost for that state. Similarly, the backward cost from that state must be the minimum backward cost. So it is safe to use only the minimum costs. Thus, we can compute forward DP to get the minimum cost to reach each state at each position, and backward DP to get the minimum cost from each state to the end. Then for reconstruction, we maintain the current state (prev_c, prev_k). At position i, we try characters c in alphabetical order. For each c, we determine the new run length new_k (if c == prev_c, new_k = min(prev_k+1, 3); else if prev_k >= 3, new_k = 1; else invalid). We check if forward_cost[i][c][new_k] + |orig[i] - c| + back[i+1][c][new_k] == global_min. If so, we choose c, update prev_c = c, prev_k = new_k, and continue. But we need forward_cost[i][c][new_k]. We have that from forward DP.

Wait, at position i, the state is (c, new_k) where c is the character we place at i, and new_k is the run length of c at i (after placing it). The forward cost to this state is the minimum cost to reach (c, new_k) at i. The backward cost from the next state (at i+1) with the appropriate transition. So the total cost if we choose c at i is: forward_cost[i][c][new_k] + back[i+1][next_c][next_k], where next_c and next_k are determined by the transition to the next character. But wait, back[i+1][next_c][next_k] is the cost from i+1 to end given that at i+1 we have character next_c and run length next_k. But the transition from i to i+1 depends on c (current) and next_c. So we need to iterate over possible next_c? That complicates things because we need to consider the entire future. Actually, the backward cost from (c, new_k) at i to the end is exactly the value back[i][c][new_k]. But back[i][c][new_k] is defined as the cost from i to end, which includes the cost of placing c at i. So if we want to check if choosing c at i is part of a globally optimal path, we need to check if there exists a state (c, new_k) at i such that forward_cost[i][c][new_k] + (back[i][c][new_k] - |orig[i] - c|) + |orig[i] - c| = forward_cost[i][c][new_k] + back[i][c][new_k] - |orig[i] - c|? That doesn't simplify. Actually, the total cost of a path that uses state (c, new_k) at i is forward_cost[i][c][new_k] + (back[i][c][new_k] - cost_to_place_c_at_i) + cost_to_place_c_at_i = forward_cost[i][c][new_k] + back[i][c][new_k] - |orig[i] - c| + |orig[i] - c| = forward_cost[i][c][new_k] + back[i][c][new_k]. But wait, back[i][c][new_k] includes the cost of placing c at i. So if we use forward_cost to reach (c, new_k) and then back from (c, new_k), we double count the cost of c at i. The correct way: The total cost of a path that goes through state (c, new_k) at i is the cost to reach i-1 (previous state) + cost to place c at i + cost from i+1 to end given the next state. That is not simply forward_cost + back. The standard way to combine forward and backward DP for reconstruction is to note that if we have the minimum cost to reach the start, and the minimum cost from each state to the end, then for any state, the minimum total cost through that state is forward_cost + backward_cost_from_state - cost_of_state? Actually, the state at i is defined after placing the character at i. The cost of the state is the cost of the prefix up to i. The backward cost from that state is the cost of the suffix from i+1 to end. So the total cost through that state is forward_cost[i][c][k] + back[i+1][c'][k'] where (c',k') is the next state. But we don't know the next state. So we need to consider transitions. This suggests that using forward and backward DP separately might not be enough to determine the exact character without considering the next state. However, we can compute the DP value for the state at i: the minimum cost to complete the string from i to end, given that we start with a new run of character c at i (with run length 1). But that's not exactly what we need because the run length at i depends on the previous character. So the state must include the run length.

**Let's re-define the DP precisely:**

We want the minimum cost to transform the entire string. Let's define dp[i][c][k] as the minimum cost to transform the prefix up to i-1 (i.e., positions 0..i-1) into a good string, such that at position i-1 (the last processed) we have character c and the run length of c at the end is k (k=1,2,3). This is the forward DP. The recurrence:
dp[i+1][c][1] = min over (prev_c, prev_k) with prev_k >= 3 and prev_c != c of (dp[i][prev_c][prev_k] + |orig[i] - c|)   [start a new run]
dp[i+1][c][min(k+1,3)] = min over (prev_c, prev_k) with prev_c == c of (dp[i][c][prev_k] + |orig[i] - c|)   [continue run]
For i=0, we start with no previous character, so we can only start new runs: dp[1][c][1] = |orig[0] - c| for all c.
At the end, we want min over c, k>=3 of dp[n][c][k]. This gives the minimum cost.

Now, to reconstruct the lexicographically smallest string with this minimum cost, we can do the following: we have the dp values. We can start at i=0 with no previous character (we need to choose the first character). We want to choose the smallest possible character c1 such that there exists a path with total cost = global_min. This is equivalent to: we need to know, for each possible first character c1, what is the minimum cost to complete the string from that point. But the first character's run length is 1. So the total cost if we start with c1 is: |orig[0] - c1| + (min cost to complete the suffix from position 1, given that the previous character was c1 and run length 1). Let's define a backward DP: let back[i][c][k] be the minimum cost to transform the suffix from i to n-1, given that at position i-1 (the character before i) we have character c and run length k. But that's not quite right because the character at i-1 is already determined. Actually, we want the cost from i onward, given the state of the run ending at i-1. That is exactly the same as the forward DP but starting from i. So we can compute back[i][c][k] = minimum cost to transform positions i..n-1, given that before position i, the run of c has length k (so at position i we are about to continue or start a new run). The recurrence for back is the same as forward but in reverse. For i = n, we are past the end: if the run length k >= 3, then cost = 0, else cost = infinity.
For i < n:
back[i][c][k] = |orig[i] - c| + min over c', k' of back[i+1][c'][k'] with valid transitions from (c,k) to (c',k').

Now, the total cost if we start with character c at position 0 and run length 1 is: |orig[0] - c| + back[1][c][1]. (Because after placing c at 0, we are at position 1 with previous character c and run length 1). So the global min cost is min_c (|orig[0] - c| + back[1][c][1]).

For reconstruction, at position i, we know the previous character prev_c and previous run length prev_k. We want to choose the current character c. The cost so far to reach this state (i.e., to have placed characters 0..i-1) is some value, but we can use the backward DP to see if choosing c can lead to the global min. Specifically, if we choose c at position i, then the run length new_k is: if c == prev_c, new_k = min(prev_k+1, 3); else if prev_k >= 3, new_k = 1; else this choice is invalid. The remaining cost from position i+1 is back[i+1][c][new_k]. So the total cost if we choose c at i, given that we have reached the state (prev_c, prev_k) at position i with some forward cost, is: forward_cost_to_prev_state + |orig[i] - c| + back[i+1][c][new_k]. But we don't know forward_cost_to_prev_state. However, we can maintain it as we go. But we can also use the fact that the global min cost is fixed. At each step, we can try characters c in order, and for each, compute the hypothetical total cost if we were to take the optimal forward path to (prev_c, prev_k) and then choose c. But that requires knowing the forward cost. Alternatively, we can use the dp values from the forward DP to know the minimum cost to reach each state. But then we need to combine.

**Simpler reconstruction method:** After computing the forward DP dp[i][c][k], we can start from the end. We know the global min cost. At position i, we want to determine the character at i. We can look at the state (c, k) at i that is part of some optimal path. We can find such a state by backtracking: start from any state (c, k) at position n that achieves the global min cost. Then for i from n-1 down to 0, we determine the character at i by looking at the transitions that lead to the state at i+1. But we need to know the character at i. Actually, we can backtrack: at position i+1, we have a state (c_{i+1}, k_{i+1}) that is on an optimal path. We want to find the state at i, (c_i, k_i), such that the transition is valid and dp[i][c_i][k_i] + |orig[i] - c_{i+1}| = dp[i+1][c_{i+1}][k_{i+1}]. But wait, dp[i][c_i][k_i] is the cost to reach i-1? No, dp is defined at positions. dp[i][c][k] is the min cost for prefix up to i-1 ending with c,k. So dp[i+1][c_{i+1}][k_{i+1}] is the cost for prefix up to i ending with c_{i+1},k_{i+1}. That cost equals dp[i][c_i][k_i] + |orig[i] - c_{i+1}| for some valid (c_i, k_i). So if we know dp[i+1][c_{i+1}][k_{i+1}], we can try all possible previous states (c_i, k_i) and see which one satisfies the equation. But there might be multiple. We want the lexicographically smallest overall string, so we want the smallest c_i? Not necessarily, because a smaller c_i might lead to a larger c_{i+1} later. We need to consider the entire string. This suggests backtracking from the end with the requirement of minimal cost and then choosing the smallest string among those. But we can do a forward reconstruction with the help of backward DP.

**Let's design a clean reconstruction using forward and backward DP:**

1. Compute forward DP: `f[i][c][k]` = min cost for prefix 0..i-1 ending with c, k. (i from 0 to n, with f[0] not defined, we can set f[0][*][*] = infinity, and we start with f[1][c][1] = |orig[0] - c|).
2. Compute backward DP: `b[i][c][k]` = min cost for suffix i..n-1 given that before i, the run of c has length k. (i from 0 to n, with b[n][c][k] = 0 if k>=3 else inf, and for i from n-1 down to 0: b[i][c][k] = |orig[i] - c| + min over c',k' of b[i+1][c'][k'] with valid transition from (c,k) to (c',k')). Note: in the backward DP, the state (c,k) refers to the character at position i-1? Actually, we need to be consistent. Let's define: `b[i][c][k]` = min cost to transform positions i..n-1 into a good string, given that the character at position i-1 is c and the run length of c ending at i-1 is k. This means that at position i, we are to place a character. The transition: from state (i, c, k) we choose the character at i, say c', with cost |orig[i] - c'|, and then we go to state (i+1, c', k') where k' is determined: if c' == c, then k' = min(k+1, 3); else if k >= 3, then k' = 1; else invalid. So b[i][c][k] = min_{c'} (|orig[i] - c'| + b[i+1][c'][k']).

3. The global minimum cost is: `min_c ( |orig[0] - c| + b[1][c][1] )` because we start with no previous character, so we effectively have a "previous" state with no run. But we can also define a dummy state. Alternatively, we can set the initial previous character to be different from any c, with run length 0, and define that starting a new run is always allowed. But it's easier to just compute the min over first character directly: for each c, the cost is f[1][c][1] + b[1][c][1]? Wait, f[1][c][1] is the cost to place c at position 0 and have run length 1. b[1][c][1] is the cost to complete the suffix from position 1 given that the previous character is c with run length 1. So the total cost is f[1][c][1] + b[1][c][1] - but wait, b[1][c][1] includes the cost of placing the character at position 1? Yes, b[1][c][1] is the cost from position 1 onward, so it includes the cost of position 1. So the total cost is f[1][c][1] + b[1][c][1] - but f[1][c][1] is just the cost at position 0, and b[1][c][1] is the cost from 1 onward. So the sum is the total cost. But note that b[1][c][1] is defined as the cost from position 1 given previous state (c,1). So the total cost for choosing first character c is: cost_at_0 = |orig[0]-c|, and then b[1][c][1]. So the global min is min_c (|orig[0]-c| + b[1][c][1]). This matches because f[1][c][1] = |orig[0]-c|.

4. Now for reconstruction: we want to build the string from left to right. We maintain the current state (prev_c, prev_k) before position i. Initially, there is no previous character, so we can think of prev_c as something that allows any c, and prev_k = 0, and we define that we can start a new run for any c. To simplify, we can just start at i=0: we try characters c in alphabetical order. For each c, we check if |orig[0]-c| + b[1][c][1] == global_min. The first such c is the first character. Then we set prev_c = c, prev_k = 1, and i=1.
For i from 1 to n-1: we try characters c in alphabetical order. We need to check if the transition from (prev_c, prev_k) to (c, new_k) is valid, and if the total cost can equal the global min. The remaining cost if we choose c at i is b[i+1][c][new_k] (if i+1 <= n, else 0). But we also need to account for the cost of the choices made so far. However, we are constructing the string greedily: we assume that the prefix we have built so far is part of some optimal path. We need to verify that the cost of the prefix we have built (which we can compute as we go) plus the cost of the new character plus the backward cost from the new state equals the global min. But we don't store the forward cost of our constructed prefix. We can instead use the fact that if we always choose the smallest character that allows the global min to be achieved, we need to check if there exists a completion. That is exactly: given prev_c, prev_k, and the global min, we want to choose c such that there exists a path from (c, new_k) at i to the end with cost = global_min - (cost of prefix up to i-1) - |orig[i]-c|. But we don't know the cost of the prefix. However, we can compute the cost of the prefix as we go, because we know the costs of the characters we chose. So we can maintain `current_cost` as the sum of |orig[j] - chosen[j]| for j=0..i-1. Then at position i, we try c, compute new_k, and check if current_cost + |orig[i]-c| + b[i+1][c][new_k] == global_min. If so, we choose c, update current_cost += |orig[i]-c|, update prev_c = c, prev_k = new_k, and continue. This works because b[i+1][c][new_k] is the minimum cost to complete the suffix from i+1 given that at position i we have c and run length new_k. But wait: b[i+1][c][new_k] is the cost from position i+1 onward given that the previous character (at i) is c with run length new_k. So the total cost if we choose c at i is exactly current_cost + |orig[i]-c| + b[i+1][c][new_k]. So this check is correct.

We need to be careful: at the last position i = n-1, after choosing the character, we need to ensure that the run length is at least 3. But the backward DP b[n][c][k] is defined as 0 if k>=3 else inf. So if we reach i = n-1, we choose c, and we check current_cost + |orig[n-1]-c| + b[n][c][new_k] == global_min. Since b[n][c][new_k] is 0 only if new_k>=3, this enforces the condition.

**So the algorithm is:**
- Compute backward DP `b[i][c][k]` for i from n down to 0. Actually, we need b[i][c][k] for i from 0 to n. We can compute an array `dp` of size (n+1) x 26 x 3. Initialize dp[n][c][k] = 0 if k==3 else inf. For i from n-1 down to 0:
  For each c in 0..25, for each k in 1..3:
    dp[i][c][k] = |orig[i] - c| + min over c' in 0..25, k' in 1..3 of dp[i+1][c'][k'] such that the transition from (c,k) to (c',k') is valid.
    Valid transitions:
      - If c' == c: k' = min(k+1, 3)
      - If c' != c: k' = 1, and we require k == 3.
- Then compute global_min = min over c in 0..25 of (|orig[0] - c| + dp[1][c][1]). (Here dp[1][c][1] is the cost from position 1 onward given previous char c and run length 1.)
- If global_min is infinity, return "".
- Otherwise, reconstruct:
  Initialize current_cost = 0, prev_c = None, prev_k = 0 (but we handle the first character specially).
  For i in 0..n-1:
    Try c from 0 to 25:
      If i == 0: new_k = 1, no transition constraints (we can start any run).
      Else: 
        if c == prev_c: new_k = min(prev_k+1, 3)
        elif prev_k == 3: new_k = 1
        else: continue (invalid)
      Compute next_cost = dp[i+1][c][new_k] if i+1 <= n else 0. (But dp is defined for i from 0 to n, so for i=n, dp[n] is base case.)
      If current_cost + |orig[i] - c| + next_cost == global_min:
        choose c, append to result, update current_cost += |orig[i] - c|, prev_c = c, prev_k = new_k, break.
  Return result.

**Complexity:** O(n * 26 * 26 * 3) for the DP? Actually, for each i, c, k, we iterate over all c' and k' to find the min. That's 26*26*3 = 2028 operations per i. For n=5e4, that's about 1e8 operations, which might be slow in Python. We need to optimize.

**Optimization of the transition:** For a fixed c, k, the next character c' can be c (continue run) or any c' != c (start new run, but only if k==3). So:
- If we continue: only one option: c' = c, k' = min(k+1,3). Cost = dp[i+1][c][min(k+1,3)].
- If we start new: we need k==3. Then for all c' != c, k' = 1. The min over c' != c of dp[i+1][c'][1]. So we can precompute for each i+1: min1[i+1] = min over all c of dp[i+1][c][1], and min1_excluding[c] = min over c' != c of dp[i+1][c'][1]. Then the start new cost is min1_excluding[c].
So for each i, c, k, the transition cost is:
  cost_continue = dp[i+1][c][min(k+1,3)]   (always valid, but note: if we continue, we are extending the run, which is always allowed regardless of k? Yes, we can always continue a run, even if k=1 or 2. The "good" condition only applies when we finish a run. So continuing a run is always valid.)
  cost_new = min1_excluding[c] if k==3 else infinity.
Then dp[i][c][k] = |orig[i] - c| + min(cost_continue, cost_new).

This reduces the transition to O(1) per state, so total O(n * 26 * 3) for the DP, which is O(n) essentially. We also need to compute min1_excluding[c] for each i+1. That can be done by finding the minimum and second minimum of dp[i+1][c'][1] over c'. So for each i+1, we can compute the smallest and second smallest values and which character they correspond to. Then for each c, min1_excluding[c] = min1 if c != argmin, else second_min. This is O(26) per i, so overall O(n*26). Very efficient.

**Let's refine the backward DP:**
We have dp[i][c][k] for i from 0 to n. We fill from i=n down to 0.
At i=n: dp[n][c][k] = 0 if k==3 else infinity.
For i from n-1 down to 0:
  For each c:
    For k=1,2,3:
      cont = dp[i+1][c][min(k+1,3)]
      new = infinity
      if k == 3:
        new = min1_excluding[c]   (precomputed from dp[i+1][*][1])
      dp[i][c][k] = |orig[i] - c| + min(cont, new)

We need to precompute for each i+1: the minimum and second minimum of dp[i+1][c][1] over c. Let's denote:
  best1 = min over c of dp[i+1][c][1]
  best2 = second min
  argmin = the c achieving best1
Then for a given c, min1_excluding[c] = best1 if c != argmin else best2.

So for each i, we can compute these in O(26) by iterating over c.

**Reconstruction:**
We need global_min = min over c of (|orig[0] - c| + dp[1][c][1]). Note that dp[1][c][1] is the cost from position 1 onward given previous char c and run length 1. This is exactly the value we need.
Then we reconstruct as described.

**Edge cases:** n < 3? The problem says n >= 1. If n < 3, can we have a good caption? A good caption requires every character to appear in groups of at least 3. If n=1 or 2, it's impossible unless n=0, but n>=1. So for n<3, we need to check if there is any good caption. Actually, if n=1, a good caption would be a string of length 1 with a character that appears in a group of at least 3, but the group is only length 1, so not good. So n=1 is impossible. Similarly n=2 is impossible. But wait, what if n=3? A good caption could be "aaa" if we can change all to 'a'. So for n<3, we should return "" if impossible. But our DP will automatically handle it: for n=1, the final state requires k=3, but after one character, k can only be 1. So dp[1][c][1] will be something, but dp[0]? Actually, our DP at i=0: we compute dp[0][c][k]. But for n=1, we have i=0 only. We need to check if there is a path from start to a state at i=1 with k=3. But the start is not a state in our dp. We defined global_min as min_c (|orig[0]-c| + dp[1][c][1]). For n=1, dp[1][c][1] is the base case: dp[1][c][1] = 0 if 1>=3? No, at i=1 (which is n), we have dp[1][c][k] = 0 if k==3 else inf. So dp[1][c][1] = inf. So global_min = min_c (|orig[0]-c| + inf) = inf. So we return "". For n=2, similar: at i=1, we compute dp[1][c][k] from dp[2]. dp[2][c][k] = 0 if k==3 else inf. So for n=2, we need to reach i=2 with k>=3. At i=1, the only possible run lengths are 1 or 2 (if we continue). Then at i=2, we can only have run length 1 or 2 or 3 if we continue. But to have k=3 at i=2, we need to have the same character for all three positions. So it's possible if we change both to the same character. Our DP will capture that. So for n=2, global_min might be finite. So we should run the DP and see.

**Let's test with small examples:**

Example 1: "cdcd" (n=4)
orig: [2,3,2,3] (0-indexed: a=0)
Backward DP:
i=4: dp[4][c][3]=0, others inf.
i=3: orig[3]=3.
  For each c, k:
    cont = dp[4][c][min(k+1,3)]
    new = inf unless k==3, then min1_excluding[c] from dp[4][*][1] which is all inf, so new=inf.
    So dp[3][c][k] = |3-c| + cont.
    cont: if k=1: min(1+1,3)=2 -> dp[4][c][2]=inf. k=2: min(2+1,3)=3 -> dp[4][c][3]=0. k=3: min(3+1,3)=3 -> dp[4][c][3]=0.
    So:
      k=1: dp[3][c][1] = |3-c| + inf = inf.
      k=2: dp[3][c][2] = |3-c| + 0 = |3-c|.
      k=3: dp[3][c][3] = |3-c| + 0 = |3-c|.
i=2: orig[2]=2.
  First compute for i=3: min1 and min2 of dp[3][c][1]? But dp[3][c][1] are all inf. So best1=inf, best2=inf. So min1_excluding[c] = inf.
  For each c, k:
    cont = dp[3][c][min(k+1,3)]
    new = inf unless k==3, then inf.
    So dp[2][c][k] = |2-c| + cont.
    cont:
      k=1: min(2,3)=2 -> dp[3][c][2] = |3-c|
      k=2: min(3,3)=3 -> dp[3][c][3] = |3-c|
      k=3: min(4,3)=3 -> dp[3][c][3] = |3-c|
    So:
      k=1: |2-c| + |3-c|
      k=2: |2-c| + |3-c|
      k=3: |2-c| + |3-c|
i=1: orig[1]=3.
  Compute for i=2: min1 and min2 of dp[2][c][1] = |2-c| + |3-c|.
    Let's compute for c=0..25:
    c=0: 2+3=5
    c=1: 1+2=3
    c=2: 0+1=1
    c=3: 1+0=1
    c=4: 2+1=3
    c=5: 3+2=5
    ...
    So min1=1 (c=2 or 3), best2=1 as well (c=3 or 2). Actually, there are ties. We need to be careful with ties. min1_excluding[c] should be the minimum over c' != c. If there are multiple with the same value, we need to pick the second smallest distinct value? Actually, if best1=1, and there are two c's with value 1, then for c=2, the min over c' != 2 is min(1 (c=3), 3 (c=1)) = 1. For c=3, similarly 1. So we can compute by taking the minimum and second minimum, but with ties, the second minimum might equal the minimum if there are multiple. So we need to compute: if c is not the unique argmin, then min1_excluding[c] = best1. If c is the unique argmin, then min1_excluding[c] = best2. If there are multiple argmins, then for any c that is one of the argmins, the min over c' != c is still best1 (since there is another c' with the same value). So we can handle this by: for each c, if c is the only argmin, use best2; else use best1.
    In our case, best1=1, and the argmin is not unique (both 2 and 3 have 1). So for c=2, min1_excluding[2] = best1 = 1. For c=3, min1_excluding[3] = 1. For others, min1_excluding[c] = best1 = 1 if best1 is the overall min, but wait, for c not in the argmin set, the min over c' != c could be best1 if the argmin is not c. So actually, for any c, min1_excluding[c] is the minimum of dp[i+1][c'][1] over c' != c. If the global minimum is achieved by some set S, then for c in S, the min over c' != c is still the global minimum (since there is another c' in S). For c not in S, the min is also the global minimum (since S is non-empty). So in fact, if the global minimum is achieved by at least two characters, then min1_excluding[c] = global_min for all c. If it's unique, then for that c, min1_excluding[c] = second min, and for others, it's global_min.
    So we need to know if the argmin is unique. We can compute: find the minimum value, count how many c achieve it. If count > 1, then for all c, min1_excluding[c] = min. If count == 1, then for the argmin c, min1_excluding[c] = second min; for others, min1_excluding[c] = min.
  In our case, for i=2, min1=1, count=2, so min1_excluding[c] = 1 for all c.
  Now for i=1, orig[1]=3.
    For each c, k:
      cont = dp[2][c][min(k+1,3)]
      new = min1_excluding[c] if k==3 else inf.
      dp[1][c][k] = |3-c| + min(cont, new)
      cont:
        k=1: dp[2][c][2] = |2-c| + |3-c|
        k=2: dp[2][c][3] = |2-c| + |3-c|
        k=3: dp[2][c][3] = |2-c| + |3-c|
      So:
        k=1: |3-c| + (|2-c| + |3-c|) = 2|3-c| + |2-c|
        k=2: same: 2|3-c| + |2-c|
        k=3: min( 2|3-c| + |2-c|, 1 )   [since new=1]
i=0: orig[0]=2.
  Compute for i=1: min1 and min2 of dp[1][c][1] = 2|3-c| + |2-c|.
    c=0: 2*3+2=8
    c=1: 2*2+1=5
    c=2: 2*1+0=2
    c=3: 2*0+1=1
    c=4: 2*1+2=4
    c=5: 2*2+3=7
    c=6: 2*3+4=10
    ...
    min1=1 (c=3), min2=2 (c=2). count=1.
  So for c=3, min1_excluding[3] = min2 = 2. For others, min1_excluding[c] = 1.
  Now for i=0, orig[0]=2.
    For each c, k:
      cont = dp[1][c][min(k+1,3)]
      new = min1_excluding[c] if k==3 else inf.
      dp[0][c][k] = |2-c| + min(cont, new)
      cont:
        k=1: dp[1][c][2] = 2|3-c| + |2-c|
        k=2: dp[1][c][3] = min( 2|3-c| + |2-c|, min1_excluding[c] )   (since from k=2, cont goes to k'=3, and new is not applicable for k=2? Wait, for k=2, new is only if k==3, so new is inf. So cont = dp[1][c][3] which is already min(cont_from_k2, new_for_k2) but k=2 has no new. Actually, careful: cont is always dp[i+1][c][min(k+1,3)]. So for k=2, cont = dp[1][c][3]. And dp[1][c][3] itself is computed as |3-c| + min( dp[2][c][3], new_for_k=3 ). So it's already the min of continuing and starting new. So at i=0, we don't need to consider new separately for k=2 because dp[1][c][3] already includes the option of starting new at i=1. So actually, the recurrence dp[i][c][k] = |orig[i]-c| + min( dp[i+1][c][min(k+1,3)], (min1_excluding[c] if k==3 else inf) ) is correct and covers all cases. So we can use that.
    So for i=0:
      k=1: cont = dp[1][c][2] = 2|3-c| + |2-c|. new = inf. So dp[0][c][1] = |2-c| + 2|3-c| + |2-c| = 2|2-c| + 2|3-c|.
      k=2: cont = dp[1][c][3] = min( 2|3-c| + |2-c|, min1_excluding[c] ). So dp[0][c][2] = |2-c| + min( 2|3-c| + |2-c|, min1_excluding[c] ).
      k=3: cont = dp[1][c][3] (same as k=2 cont). new = min1_excluding[c]. So dp[0][c][3] = |2-c| + min( 2|3-c| + |2-c|, min1_excluding[c], min1_excluding[c] ) = |2-c| + min( 2|3-c| + |2-c|, min1_excluding[c] ).
  Then global_min = min_c ( |orig[0]-c| + dp[1][c][1] ) = min_c ( |2-c| + (2|3-c| + |2-c|) ) = min_c ( 2|2-c| + 2|3-c| ). This is the cost if we start with c and then continue? Actually, dp[1][c][1] is the cost from position 1 onward given previous char c and run length 1. So global_min = min_c ( |2-c| + dp[1][c][1] ). We can compute that:
  For c=0: 2+2*3=8
  c=1: 1+2*2=5
  c=2: 0+2*1=2
  c=3: 1+2*0=1
  c=4: 2+2*1=4
  So global_min = 1, achieved by c=3.
  So the first character should be 'd' (c=3). That gives total cost 1? But the example says minimum is 2 operations. Wait, check: if we choose c=3 at position 0, then the cost at position 0 is |2-3|=1. Then from position 1 onward, we need to complete with previous char 'd' and run length 1. The total cost would be 1 + dp[1][3][1]. dp[1][3][1] = 2|3-3| + |2-3| = 0+1=1. So total = 2. So global_min = 2, not 1. I made a mistake: global_min is min_c ( |orig[0]-c| + dp[1][c][1] ). For c=3, |2-3|=1, dp[1][3][1] = 2|3-3| + |2-3| = 1, so total = 2. So global_min = 2. And that matches the example.

Now reconstruction:
global_min = 2.
We try first character c in order:
c='a' (0): |2-0| + dp[1][0][1] = 2 + (2|3-0|+|2-0|) = 2+ (6+2)=10 !=2
c='b' (1): 1 + (2|3-1|+|2-1|) = 1+ (4+1)=6 !=2
c='c' (2): 0 + (2|3-2|+|2-2|) = 0+ (2+0)=2 ==2. So we choose 'c' as first character? But the example says "cccc" is the answer, which starts with 'c'. Yes. So we choose c=2.
Then current_cost = 0, prev_c=2, prev_k=1, i=0 done.
Now i=1: orig[1]=3.
Try c from 0:
c=0: transition: c != prev_c, so need prev_k=3? But prev_k=1, so invalid.
c=1: invalid.
c=2: c == prev_c, new_k = min(1+1,3)=2. next_cost = dp[2][2][2]. dp[2][2][2] = |2-2| + |3-2| = 0+1=1. Total cost = current_cost + |3-2| + next_cost = 0 + 1 + 1 = 2. That equals global_min. So we can choose c=2 ('c')? But the answer is "cccc", so we should choose 'c' again. Let's check: if we choose c=2 at i=1, then the string so far is "cc". The run length is 2. Then we continue to i=2. But wait, if we choose 'c' at i=1, the cost at i=1 is |3-2|=1. So current_cost becomes 1. Then at i=2, we need to choose. But the total cost is 2 so far? Actually, after i=1, current_cost = |2-2| + |3-2| = 0+1=1. Then we need to complete with cost 1 more to reach total 2. So at i=2, we need to choose a character such that the remaining cost is 1. Let's see: dp[2][2][2] is the cost from i=2 onward given previous char 'c' and run length 2. That cost is 1. So if we are at i=1 with prev_c='c', prev_k=2, and we are about to choose i=1? Wait, we are at i=1 choosing the character for position 1. The state before choosing is (prev_c, prev_k) = (2,1). After choosing c=2, new_k=2. Then the remaining cost is dp[2][2][2] = 1. So total = current_cost_before_i1 (which is 0) + cost_at_i1 (1) + remaining (1) = 2. So that works. So we choose c=2 at i=1.
Now current_cost = 1, prev_c=2, prev_k=2, i=1 done.
i=2: orig[2]=2.
Try c:
c=0: invalid.
c=1: invalid.
c=2: c == prev_c, new_k = min(2+1,3)=3. next_cost = dp[3][2][3]. dp[3][2][3] = |3-2| = 1. Total = current_cost (1) + |2-2| (0) + next_cost (1) = 2. So choose c=2.
Now current_cost = 1, prev_c=2, prev_k=3, i=2 done.
i=3: orig[3]=3.
Try c:
c=0: c != prev_c, prev_k=3 >=3, so new_k=1. next_cost = dp[4][0][1] = inf (since i=4 is n, and k=1 <3). So total = 1 + |3-0| (3) + inf = inf, not 2.
c=1: similarly, |3-1|=2, inf -> not 2.
c=2: c == prev_c, new_k = min(3+1,3)=3. next_cost = dp[4][2][3] = 0 (since k=3). Total = 1 + |3-2| (1) + 0 = 2. So choose c=2.
Thus the string is "cccc". Perfect.

So the algorithm works.

**Now, we need to implement it efficiently in Python.**

**Implementation details:**

- We have strings, so we convert to list of ints (0-25) for faster computation.
- n up to 5e4, dp array of size (n+1) * 26 * 3 = 5e4 * 78 = 3.9e6 entries. Each entry can be a small integer (cost up to 25*n = 1.25e6, so fits in int). We can use a 2D list: dp = [[inf]*78 for _ in range(n+1)] where index for (c,k) is c*3 + (k-1). Or we can use a flat list of length (n+1)*78. But 3.9e6 integers in Python is about 3.9e6 * 28 bytes ≈ 110 MB, which might be too much. We need to optimize memory.

**Memory optimization:** We can compute the backward DP in reverse and only keep two rows: the current i and the next i+1. But for reconstruction, we need dp[i+1][c][new_k] at each step i. We are reconstructing from left to right, so we need to be able to query dp[i+1][c][new_k] for any i+1 and any (c, new_k). We cannot discard the entire dp array because we need random access. However, we can compute the backward DP and store it in an array of size (n+1) * 78. With n=5e4, that's 3.9e6 integers. In Python, each integer is an object, so it's large. We can use `array('i')` or `list` of integers? Actually, a Python list of integers: each integer is a small object, but for small integers, they are cached? Not all. The cost can be up to 1.25e6, which is within the small int cache? Python caches small integers typically from -5 to 256. So 1.25e6 is not cached, so each integer is a separate object, taking about 28 bytes. So 3.9e6 * 28 ≈ 109 MB. Plus the list overhead, it might exceed memory limit (typically 256 MB or 512 MB). But it might be borderline. We can try to use a more compact representation. Since the costs are nonnegative and bounded by 25*n, we can use a Python array of type 'i' (signed int) or 'I' (unsigned int). That would use 4 bytes per entry, so 3.9e6 * 4 = 15.6 MB, which is great. We can use the `array` module or `numpy`? But we need to be careful with large n. We can also use a flat list of integers but with a trick: since we only need to access dp[i][c][k], we can preallocate a list of size (n+1)*78 and fill it. But initializing a large list with zeros might be fast. However, using `array` from the `array` module is efficient. But we need to set infinity. We can use a large number like 10**9. We can store as Python integers in a list if memory allows. Let's estimate: 3.9e6 elements. In Python, a list of 3.9e6 integers takes about 3.9e6 * 8 bytes (for the pointer) + the integers themselves. Actually, the list stores pointers to PyObject. Each integer object takes 28 bytes. So total: 3.9e6 * (8+28) = 140 MB. Plus the list overhead, maybe 150 MB. It might be acceptable if memory limit is 256 MB. But to be safe, we can use `array('i', [inf])* (n+1)*78` but array doesn't support `*` with a list. We can use `array('i', [10**9])*size` but that creates a list? Actually, `array('i', [10**9]) * size` creates an array with size elements, all initialized to 10**9. That should be memory efficient. But we need to be careful with multiplication: `array('i', [10**9]) * size` returns an array with `size` copies of the element. So that's fine. However, the `array` module's `array` is not as fast as list for random access? It should be fine. We can also use `memoryview` or `numpy` if allowed, but not necessary.

**Another memory optimization:** We can compute the backward DP on the fly during reconstruction? We need dp[i+1][c][new_k] for various i+1. We could recompute the backward DP from the end for each i, but that's O(n^2). Not good. So we need to store it.

**Alternative approach:** Use the forward DP and then backtrack from the end. We can store the forward DP (dp[i][c][k] as min cost to reach state (c,k) at position i) and then backtrack to find the lexicographically smallest path. But we still need to store the forward DP. Same memory issue.

**Let's try to use a 2D list of size (n+1) x 26 x 3 but using a list of lists. Since 5e4 * 26 = 1.3e6, and each inner list has 3 elements. So total entries: 1.3e6. Each entry is an integer. That's half the size? Wait, n+1 is 5e4+1, times 26 is 1.3e6, times 3 is 3.9e6. So it's the same. But if we store as dp[i][c] = list of 3 integers, that's 1.3e6 lists. Each list has 3 integers, so total integers: 3.9e6. The list objects themselves take memory. So it's not better.

**We can try to use a single list of size (n+1)*78 and compute index manually. That's the most compact. Let's use the `array` module. But we need to set values. We can create an array of size (n+1)*78, initialized to a large number. Then we fill from i=n down to 0. We need to access dp[i][c][k] quickly. We can define a function to compute index: idx = i*78 + c*3 + (k-1). Then we can read and write.

**Let's code the backward DP:**

```python
def minCostGoodCaption(self, caption: str) -> str:
    n = len(caption)
    if n == 0: return ""
    s = [ord(c) - ord('a') for c in caption]
    INF = 10**9
    size = (n+1) * 78
    dp = [INF] * size  # This is a list, memory might be high. Let's try with array.
    # But Python list of 4e6 integers is ~100MB, might be okay.
    # Alternatively, use array('i', [INF]) * size
    from array import array
    dp = array('i', [INF]) * size
    
    # Base case: i = n
    for c in range(26):
        idx = n*78 + c*3 + 2  # k=3 -> index 2
        dp[idx] = 0
    
    # For i from n-1 down to 0:
    for i in range(n-1, -1, -1):
        # Precompute for i+1: min1 and min2 of dp[i+1][c][1] (k=1)
        min1 = INF
        min2 = INF
        argmin = -1
        for c in range(26):
            idx = (i+1)*78 + c*3 + 0  # k=1
            val = dp[idx]
            if val < min1:
                min2 = min1
                min1 = val
                argmin = c
            elif val < min2:
                min2 = val
        # Now for each c, k
        for c in range(26):
            cost_char = abs(s[i] - c)
            # k=1
            cont = dp[(i+1)*78 + c*3 + min(1, 2)] # min(1+1,3)=2
            new = INF
            dp[i*78 + c*3 + 0] = cost_char + min(cont, new)
            # k=2
            cont = dp[(i+1)*78 + c*3 + 2] # min(2+1,3)=3 -> index 2
            new = INF
            dp[i*78 + c*3 + 1] = cost_char + min(cont, new)
            # k=3
            cont = dp[(i+1)*78 + c*3 + 2] # min(3+1,3)=3 -> index 2
            # new: min over c' != c of dp[i+1][c'][1]
            if argmin == -1:  # all INF?
                new = INF
            else:
                if c != argmin:
                    new = min1
                else:
                    # if argmin is unique? We need to know if there are multiple with min1.
                    # We can check if min2 == min1? Actually, we need to know if there is another c with the same min1.
                    # We can compute count of min1 in the precomputation.
                    pass
            # We'll handle the unique case below.
```

We need to correctly compute `new` for k=3. We need the minimum over c' != c of dp[i+1][c'][1]. We can compute this by: if c is not the unique argmin, then new = min1. If c is the unique argmin, then new = min2. So we need to know if argmin is unique. We can count the number of c that achieve min1. Let's modify the precomputation to also compute count.

```python
        min1 = INF
        min2 = INF
        argmin = -1
        count = 0
        for c in range(26):
            idx = (i+1)*78 + c*3 + 0
            val = dp[idx]
            if val < min1:
                min2 = min1
                min1 = val
                argmin = c
                count = 1
            elif val == min1:
                count += 1
            elif val < min2:
                min2 = val
```

Then in the loop for c:
```python
            if k == 3:
                if count > 1:
                    new = min1
                else: # count == 1
                    if c != argmin:
                        new = min1
                    else:
                        new = min2
            else:
                new = INF
```

But note: if min1 is INF (all dp[i+1][c][1] are INF), then count=0, argmin=-1, min2=INF. Then for any c, new should be INF. So we can check if min1 == INF: new = INF.

**Now, after filling dp, we compute global_min:**

We need to compute: for each c, cost = |s[0] - c| + dp[1*78 + c*3 + 0] (since dp[1][c][1]). But wait, dp[1][c][1] is at i=1, c, k=1. So:
```python
        global_min = INF
        for c in range(26):
            cost = abs(s[0] - c) + dp[78 + c*3 + 0]  # i=1
            if cost < global_min:
                global_min = cost
        if global_min >= INF: return ""
```

**Reconstruction:**

We need to build the result string. We maintain current_cost = 0, prev_c = None, prev_k = 0 (but we handle first character specially). We'll collect characters in a list.

```python
        result = []
        current_cost = 0
        prev_c = 0
        prev_k = 0
        for i in range(n):
            found = False
            for c in range(26):
                if i == 0:
                    new_k = 1
                else:
                    if c == prev_c:
                        new_k = min(prev_k + 1, 3)
                    elif prev_k == 3:
                        new_k = 1
                    else:
                        continue
                # Check if this choice can lead to global_min
                # We need to compute the remaining cost from i+1 onward
                if i+1 <= n:
                    # dp[i+1][c][new_k] is the cost from i+1 onward given previous char c and run length new_k
                    # But careful: dp[i][c][k] is defined for the state at position i (after placing char at i-1? Wait, our dp definition: dp[i][c][k] is the min cost for the suffix from i to n-1, given that before i, the run of c has length k. So at position i, we are about to place a character. So if we are at position i and we choose character c, then the remaining cost is dp[i+1][c][new_k]? Actually, no: dp[i+1][c][new_k] is the cost from i+1 onward given that at position i we placed c and the run length is new_k. So after placing c at i, the next state is (i+1, c, new_k). So the remaining cost is dp[i+1][c][new_k]. But we need to be careful: dp[i+1][c][new_k] is defined for the state where the previous character (at i) is c with run length new_k. So yes, it's exactly the cost from i+1 onward.
                    remaining = dp[(i+1)*78 + c*3 + (new_k-1)]
                else:
                    remaining = 0
                if current_cost + abs(s[i] - c) + remaining == global_min:
                    result.append(chr(c + ord('a')))
                    current_cost += abs(s[i] - c)
                    prev_c = c
                    prev_k = new_k
                    found = True
                    break
            if not found:
                # Should not happen
                return ""
        return ''.join(result)
```

But wait: in the reconstruction, at the last position i = n-1, after choosing c, we set remaining = dp[n*78 + c*3 + (new_k-1)] = 0 if new_k==3 else INF. So the check will enforce new_k=3. That's correct.

**Testing on examples:**

Example 1: "cdcd" -> should return "cccc".
Example 2: "aca" -> "aaa".
Example 3: "bc" -> n=2, should return ""? Let's test: orig: [1,2]. n=2.
Base: i=2: dp[2][c][3]=0, others INF.
i=1: orig[1]=2.
  min1 and min2 of dp[2][c][1]? All INF. So min1=INF, count=0.
  For c, k:
    cost_char = |2-c|
    cont = dp[2][c][min(k+1,3)]
    new = INF (since k!=3 or min1 INF)
    So dp[1][c][k] = |2-c| + cont.
    cont: for k=1: min(2,3)=2 -> dp[2][c][2]=INF. So dp[1][c][1] = |2-c| + INF = INF.
    k=2: min(3,3)=3 -> dp[2][c][3]=0. So dp[1][c][2] = |2-c| + 0 = |2-c|.
    k=3: cont = dp[2][c][3]=0, new=INF, so dp[1][c][3] = |2-c|.
i=0: orig[0]=1.
  min1 and min2 of dp[1][c][1]? All INF. So min1=INF.
  For c, k:
    cost_char = |1-c|
    cont = dp[1][c][min(k+1,3)]
    new = INF
    So dp[0][c][k] = |1-c| + cont.
    cont: k=1: dp[1][c][2] = |2-c| -> so dp[0][c][1] = |1-c| + |2-c|.
    k=2: dp[1][c][3] = |2-c| -> dp[0][c][2] = |1-c| + |2-c|.
    k=3: dp[1][c][3] = |2-c| -> dp[0][c][3] = |1-c| + |2-c|.
global_min = min_c (|1-c| + dp[1][c][1]) = min_c (|1-c| + INF) = INF. So return "". Correct.

Example 2: "aca" -> n=3. orig: [0,2,0].
We can trust the algorithm.

**Potential issues:**
- The reconstruction loop might not find a character for some i if there's a bug. We should assert that it finds one.
- The backward DP uses dp[i+1][c][min(k+1,3)] but we need to ensure that the index is correct. min(k+1,3) for k=1 is 2, for k=2 is 3, for k=3 is 3. So indices: k=1 -> index 0, k=2 -> index 1, k=3 -> index 2. So min(k+1,3) gives: 1->2, 2->3, 3->3. So we need to map: for k=1, look at index 1 (k'=2); for k=2 and 3, look at index 2 (k'=3). So in code: cont = dp[(i+1)*78 + c*3 + (min(k+1,3)-1)]. But careful: min(k+1,3) gives the run length, which is 1,2,3. We need to subtract 1 to get the index. So:
  if k==1: cont = dp[(i+1)*78 + c*3 + 1]  # run length 2
  if k==2: cont = dp[(i+1)*78 + c*3 + 2]  # run length 3
  if k==3: cont = dp[(i+1)*78 + c*3 + 2]  # run length 3
So we can compute cont_idx = 1 if k==1 else 2.
But in the general formula: min(k+1,3) gives the new run length. So we can do: cont_run = min(k+1, 3); cont = dp[(i+1)*78 + c*3 + (cont_run-1)].

**Optimizing the backward DP inner loop:** We can avoid computing cont and new separately by precomputing for each i+1 and c the value `best_cont` for continuing and `best_new` for starting new. But since we have only 3 k's, it's fine.

**Let's write the code with careful index handling.**

**One more thing:** The backward DP as described uses the state (c,k) to represent the character at position i-1 and its run length. But in the reconstruction, we are using dp[i+1][c][new_k] where new_k is the run length after placing c at i. That matches.

**Let's test with a simple case: n=3, "aaa".**
orig: [0,0,0].
i=3: dp[3][c][3]=0.
i=2: orig[2]=0.
  min1 of dp[3][c][1]? All INF.
  For c, k:
    cost_char = |0-c| = c.
    cont: if k=1: dp[3][c][2] = INF. so dp[2][c][1] = c + INF = INF.
    k=2: cont = dp[3][c][3] = 0, so dp[2][c][2] = c.
    k=3: cont = dp[3][c][3] = 0, new=INF, so dp[2][c][3] = c.
i=1: orig[1]=0.
  min1 of dp[2][c][1]? All INF.
  For c, k:
    cont: k=1: dp[2][c][2] = c. So dp[1][c][1] = c + c = 2c.
    k=2: dp[2][c][3] = c. So dp[1][c][2] = 2c.
    k=3: dp[2][c][3] = c, new=INF, so dp[1][c][3] = 2c.
i=0: orig[0]=0.
  min1 of dp[1][c][1] = 2c. min1=0 (c=0), min2=2 (c=1), count=1.
  For c, k:
    cont: k=1: dp[1][c][2] = 2c. So dp[0][c][1] = c + 2c = 3c.
    k=2: dp[1][c][3] = 2c. So dp[0][c][2] = 3c.
    k=3: cont = 2c, new: for c=0, since argmin=0 and count=1, new = min2=2. So min(2c, new)= min(0,2)=0. So dp[0][0][3] = 0 + 0 = 0. For c>0, new = min1=0. So min(2c, 0)=0. So dp[0][c][3] = c + 0 = c.
global_min = min_c (|0-c| + dp[1][c][1]) = min_c (c + 2c) = min_c (3c) = 0 (c=0).
Reconstruction: first char c=0, current_cost=0.
i=1: try c=0: c==prev_c, new_k=min(1+1,3)=2. remaining = dp[2*78 + 0*3 + 1] = dp[2][0][2] = 0? dp[2][0][2] = c=0. So remaining=0. Total = 0 + 0 + 0 = 0. Choose c=0.
i=2: try c=0: new_k=min(2+1,3)=3. remaining = dp[3*78 + 0*3 + 2] = 0. Total=0. Choose c=0.
Result "aaa". Correct.

**Now, test with example 1:** We already did manually.

**Test with example 2:** "aca" -> [0,2,0].
We can run through the code mentally or just trust it.

**Potential bug:** In the backward DP, when we compute `new` for k=3, we use the min over c' != c of dp[i+1][c'][1]. But note that dp[i+1][c'][1] is the cost from i+1 onward given that the previous character is c' with run length 1. That is correct for starting a new run at position i+1. But what if we start a new run at position i? That means the character at i is different from c. In the backward DP, at state (i, c, k) with k=3, we consider the option of choosing a character c' != c at position i. The cost is |orig[i] - c'| + dp[i+1][c'][1]. So the min over c' != c of dp[i+1][c'][1] is exactly the min over c' != c of (|orig[i] - c'| + dp[i+1][c'][1]) minus |orig[i] - c'|? Wait, careful: In the recurrence: dp[i][c][k] = |orig[i] - c| + min( dp[i+1][c][min(k+1,3)], min_{c' != c} ( |orig[i] - c'| + dp[i+1][c'][1] ) )? No! That's not right. Let's re-derive carefully.

We defined: b[i][c][k] = minimum cost to transform the suffix from i to n-1, given that the character at position i-1 is c and the run length of c ending at i-1 is k. At position i, we choose a character c'. The cost is |orig[i] - c'|, and then the new state is (i+1, c', k') where k' is determined. So:
b[i][c][k] = min_{c'} ( |orig[i] - c'| + b[i+1][c'][k'] )
where k' = min(k+1, 3) if c' == c, else (k' = 1 if k >= 3 else invalid).

So for a fixed c and k, the transition cost for a given c' is exactly |orig[i] - c'| + b[i+1][c'][k']. So the min over c' is not simply min over c' of b[i+1][c'][1] because we need to add |orig[i] - c'|. So in our earlier optimization, we said: for k=3, we can start a new run with any c' != c, and the new run length is 1. So the cost is |orig[i] - c'| + b[i+1][c'][1]. So the min over c' != c of that. This is not simply min_{c' != c} b[i+1][c'][1]. We need to include the cost of the character change. So we cannot precompute min1_excluding[c] as the min of b[i+1][c'][1]. We need the min of |orig[i] - c'| + b[i+1][c'][1]. So our previous optimization was incorrect! We need to account for the cost of the character at position i when starting a new run.

Let's correct: For k=3, the "new" option is: choose c' != c, cost = |orig[i] - c'| + b[i+1][c'][1]. So we need to find the minimum over c' != c of (|orig[i] - c'| + b[i+1][c'][1]). This depends on c because of the |orig[i] - c'| term. So we cannot precompute a single min1_excluding[c] for all c; we need to compute for each c the min over c' != c. That's 26*26 per i, which is 676 per i, and for n=5e4, that's 33.8 million, which is still okay. But we can optimize further: we can precompute for each c' the value val[c'] = |orig[i] - c'| + b[i+1][c'][1]. Then for a given c, we need the min over c' != c of val[c']. That can be done by finding the global min and second min of val, as before. But careful: val[c'] depends on c' and i. So for each i, we can compute an array best[c'] = |orig[i] - c'| + b[i+1][c'][1]. Then we find the minimum and second minimum of best, and also the argmin and count. Then for a given c, if c is not the unique argmin, then min_{c' != c} best[c'] = best_min. If c is the unique argmin, then it is best_second_min. This is correct because the min over c' != c is the same as the min over all c' except possibly the argmin. So we can do that.

So the backward DP recurrence is:
b[i][c][k] = |orig[i] - c| + min( b[i+1][c][min(k+1,3)], (if k==3: min_{c' != c} ( |orig[i] - c'| + b[i+1][c'][1] ) else INF) )

So for each i, we need to compute the array best[c'] = |orig[i] - c'| + b[i+1][c'][1] for all c'. Then for each c and k=3, the "new" cost is min over c' != c of best[c']. We can compute that using the min and second min of best.

**Let's re-do the backward DP with this correction.**

Algorithm:
- n = len(caption)
- s = list of ints
- dp = array of size (n+1)*78, initialized to INF.
- Set dp[n][c][3] = 0 for all c.
- For i from n-1 down to 0:
  - Compute best[c] = |s[i] - c| + dp[i+1][c][1] for all c.
  - Find min1 = min(best), min2 = second min, argmin, count of min1.
  - For each c in 0..25:
    - cost_char = |s[i] - c|
    - For k=1,2,3:
      - cont_run = min(k+1, 3)
      - cont = dp[i+1][c][cont_run]  # note: cont_run is the run length, so index = cont_run-1
      - new = INF
      - if k == 3:
        if min1 >= INF: new = INF
        else:
          if count > 1: new = min1
          else: # count == 1
            if c != argmin: new = min1
            else: new = min2
      - dp[i][c][k] = cost_char + min(cont, new)
  - End for c, k
- End for i

**Let's test with the example "cdcd" again to see if it matches.**

We'll do a quick mental run for i=2 in "cdcd": s[2]=2 (c). i=2: we need best[c] = |2-c| + dp[3][c][1]. dp[3][c][1] from earlier: at i=3, we had dp[3][c][1] = inf for all c? Actually, at i=3, we computed: k=1: dp[3][c][1] = |3-c| + cont, cont was inf because dp[4][c][2] is inf. So yes, dp[3][c][1] = inf. So best[c] = |2-c| + inf = inf. So min1=inf, min2=inf, count=0.
Then for each c, k:
  cont = dp[3][c][min(k+1,3)] as before.
  new = INF.
  So dp[2][c][k] = |2-c| + cont.
This matches our earlier manual calculation? Earlier we had dp[2][c][k] = |2-c| + cont, and cont was |3-c| for k=2,3 and inf for k=1. So yes.

At i=1: s[1]=3. We need best[c] = |3-c| + dp[2][c][1]. dp[2][c][1] = |2-c| + cont, cont was inf, so dp[2][c][1] = inf. So best[c] = |3-c| + inf = inf. So min1=inf.
Then dp[1][c][k] = |3-c| + min(cont, new). cont as before. new=inf. So dp[1][c][k] = |3-c| + cont.
At i=0: s[0]=2. best[c] = |2-c| + dp[1][c][1]. dp[1][c][1] = |3-c| + cont, cont for k=1 is dp[2][c][2] = |2-c| + |3-c|. So dp[1][c][1] = |3-c| + (|2-c|+|3-c|) = 2|3-c| + |2-c|. So best[c] = |2-c| + 2|3-c| + |2-c| = 2|2-c| + 2|3-c|. Let's compute for c=0..25:
c=0: 2*2 + 2*3 = 4+6=10
c=1: 2*1 + 2*2 = 2+4=6
c=2: 2*0 + 2*1 = 0+2=2
c=3: 2*1 + 2*0 = 2+0=2
c=4: 2*2 + 2*1 = 4+2=6
...
So min1=2, argmin=2 or 3, count=2. min2=2.
Now for each c, k:
  cont: for k=1: dp[1][c][2] = |3-c| + cont, cont for k=2 is dp[2][c][3] = |2-c|+|3-c|. So dp[1][c][2] = 2|3-c| + |2-c|.
  For k=2: cont = dp[1][c][3]? Actually, cont = dp[i+1][c][min(k+1,3)] = dp[1][c][3] for k=2. dp[1][c][3] = |3-c| + min(cont, new). cont for k=3 is dp[2][c][3] = |2-c|+|3-c|, new is inf. So dp[1][c][3] = 2|3-c| + |2-c|.
  For k=3: cont = dp[1][c][3] = 2|3-c| + |2-c|. new: since min1=2, count=2, for any c, new = min1 = 2.
  So:
    k=1: dp[0][c][1] = |2-c| + cont = |2-c| + (2|3-c| + |2-c|) = 2|2-c| + 2|3-c|.
    k=2: dp[0][c][2] = |2-c| + cont = same: 2|2-c| + 2|3-c|.
    k=3: dp[0][c][3] = |2-c| + min( 2|3-c| + |2-c|, 2 ) = |2-c| + min(2|3-c|+|2-c|, 2).
Now global_min = min_c ( |2-c| + dp[1][c][1] ) = min_c ( |2-c| + (2|3-c|+|2-c|) ) = min_c (2|2-c| + 2|3-c|) = min_c (best[c]) = min1 = 2. So global_min=2.
Reconstruction: as before, we get "cccc". So the corrected DP also works.

**Now, let's re-verify the reconstruction formula with the corrected DP.**

In reconstruction, at position i, we choose c. The remaining cost is dp[i+1][c][new_k]. But careful: dp[i+1][c][new_k] is the cost from i+1 onward given that at position i we have character c and run length new_k. That is exactly what we need. So the reconstruction check is: current_cost + |s[i] - c| + dp[i+1][c][new_k] == global_min. This is correct.

**One more check:** In the backward DP, we computed best[c] = |s[i] - c| + dp[i+1][c][1]. This is the cost of choosing character c at position i and then having the state (c,1) at i+1. So it's exactly the "new" option cost for k=3. So our recurrence is correct.

**Now, we need to implement this efficiently.**

**Memory:** We need dp of size (n+1)*78. Using `array('i')` is good. But we need to set INF. INF can be a large integer, but array('i') uses signed int, typically 4 bytes, max 2^31-1. 10**9 is fine.

**Time:** For each i, we do:
- Compute best[26]: O(26)
- Find min1, min2, argmin, count: O(26)
- For each c in 26, and for each k in 1,2,3: O(26*3)
Total per i: O(26) essentially, so O(n*26) = 1.3e6 operations, very fast.

**Reconstruction:** O(n*26) in worst case, but we break early, so it's fast.

**Let's code it carefully.**

We need to handle the index mapping. Let's define a helper function:
```python
def idx(i, c, k): return i*78 + c*3 + (k-1)
```
But we can compute inline.

**Edge cases:** n=0? The problem says n>=1, but we can handle n=0.
n=1: The DP will give global_min = INF, return "".
n=2: As in example 3, returns "" if impossible.

**Testing with n=3, "abc":** orig: [0,1,2]. Should we be able to make a good caption? Possible good captions: "aaa", "bbb", "ccc". Cost for "aaa": |0-0|+|1-0|+|2-0| = 0+1+2=3. "bbb": 1+0+1=2. "ccc": 2+1+0=3. So min cost is 2 with "bbb". Our algorithm should find that.

**Let's test mentally with n=3, "abc":**
i=3: dp[3][c][3]=0.
i=2: s[2]=2. best[c] = |2-c| + dp[3][c][1] = |2-c| + inf = inf. So min1=inf.
  For c, k:
    cont: k=1: dp[3][c][2]=inf -> dp[2][c][1]=inf.
    k=2: dp[3][c][3]=0 -> dp[2][c][2]=|2-c|.
    k=3: cont=0, new=inf -> dp[2][c][3]=|2-c|.
i=1: s[1]=1. best[c] = |1-c| + dp[2][c][1] = |1-c| + inf = inf.
  For c, k:
    cont: k=1: dp[2][c][2]=|2-c| -> dp[1][c][1] = |1-c| + |2-c|.
    k=2: dp[2][c][3]=|2-c| -> dp[1][c][2] = |1-c| + |2-c|.
    k=3: cont=|2-c|, new=inf -> dp[1][c][3] = |1-c| + |2-c|.
i=0: s[0]=0. best[c] = |0-c| + dp[1][c][1] = |c| + (|c-1| + |c-2|).
  Compute best for c=0: 0 + 1+2=3
  c=1: 1 + 0+1=2
  c=2: 2 + 1+0=3
  c=3: 3 + 2+1=6
  c=4: 4 + 3+2=9
  So min1=2 (c=1), min2=3 (c=0 or 2), count=1, argmin=1.
  For c, k:
    cont: for k=1: dp[1][c][2] = |1-c|+|2-c|. So dp[0][c][1] = c + |1-c|+|2-c|.
    k=2: dp[1][c][3] = |1-c|+|2-c|. So dp[0][c][2] = c + |1-c|+|2-c|.
    k=3: cont = |1-c|+|2-c|. new: for c=1, since argmin=1, new = min2=3. For others, new = min1=2.
  So:
    c=0: k=1: 0+1+2=3; k=2: 3; k=3: min(3, 2)=2 -> 0+2=2.
    c=1: k=1: 1+0+1=2; k=2: 2; k=3: min(2, new=3)=2 -> 1+2=3.
    c=2: k=1: 2+1+0=3; k=2: 3; k=3: min(3, 2)=2 -> 2+2=4.
global_min = min_c ( |0-c| + dp[1][c][1] ) = min_c ( c + (c + |1-c|+|2-c|) ) = min_c best[c] = 2.
So global_min=2.
Reconstruction: try c=0: cost=0, remaining=dp[1][0][1]=? dp[1][0][1] = |1-0|+|2-0|=1+2=3. Total=0+3=3 !=2.
c=1: cost=1, remaining=dp[1][1][1]= |1-1|+|2-1|=0+1=1. Total=1+1=2 ==2. Choose c=1. So first char 'b'.
current_cost=1, prev_c=1, prev_k=1.
i=1: try c=0: c != prev_c, prev_k=1 <3, invalid.
c=1: c == prev_c, new_k=2. remaining = dp[2][1][2] = |2-1|=1. Total=1 + |1-1|(0) + 1 = 2. Choose c=1. So 'b'.
current_cost=1, prev_c=1, prev_k=2.
i=2: try c=0: invalid.
c=1: c == prev_c, new_k=3. remaining = dp[3][1][3] = 0. Total=1 + |2-1|(1) + 0 = 2. Choose c=1. So 'b'.
Result "bbb". Correct.

**Now, we need to implement the solution in the required format.**

**Potential issues with array('i') and large INF:** The `array` module's 'i' type is signed int. INF = 10**9 is fine. But when we add numbers, we might exceed 2^31? n=5e4, max cost = 25*5e4 = 1.25e6, so no overflow.

**Let's write the code:**

```python
from array import array

class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n == 0:
            return ""
        s = [ord(c) - ord('a') for c in caption]
        INF = 10**9
        # DP array: size (n+1) * 26 * 3
        size = (n + 1) * 26 * 3
        dp = array('i', [INF]) * size
        
        # Base case: i = n
        for c in range(26):
            idx = n * 78 + c * 3 + 2  # k=3
            dp[idx] = 0
        
        # Fill backward
        for i in range(n - 1, -1, -1):
            # Compute best[c] = |s[i] - c| + dp[i+1][c][1]
            best = [0] * 26
            min1 = INF
            min2 = INF
            argmin = -1
            count = 0
            for c in range(26):
                idx_next = (i + 1) * 78 + c * 3 + 0  # k=1
                val = abs(s[i] - c) + dp[idx_next]
                best[c] = val
                if val < min1:
                    min2 = min1
                    min1 = val
                    argmin = c
                    count = 1
                elif val == min1:
                    count += 1
                elif val < min2:
                    min2 = val
            
            for c in range(26):
                cost_char = abs(s[i] - c)
                # k=1
                cont_run = 2  # min(1+1,3)=2
                cont = dp[(i + 1) * 78 + c * 3 + (cont_run - 1)]
                new = INF
                dp_idx = i * 78 + c * 3 + 0
                dp[dp_idx] = cost_char + min(cont, new)
                # k=2
                cont_run = 3
                cont = dp[(i + 1) * 78 + c * 3 + (cont_run - 1)]
                new = INF
                dp_idx = i * 78 + c * 3 + 1
                dp[dp_idx] = cost_char + min(cont, new)
                # k=3
                cont_run = 3
                cont = dp[(i + 1) * 78 + c * 3 + (cont_run - 1)]
                new = INF
                if min1 < INF:
                    if count > 1:
                        new = min1
                    else:  # count == 1
                        if c != argmin:
                            new = min1
                        else:
                            new = min2
                dp_idx = i * 78 + c * 3 + 2
                dp[dp_idx] = cost_char + min(cont, new)
        
        # Compute global minimum
        global_min = INF
        for c in range(26):
            cost = abs(s[0] - c) + dp[1 * 78 + c * 3 + 0]
            if cost < global_min:
                global_min = cost
        
        if global_min >= INF:
            return ""

## worker: Implement the optimized backward DP in Python with
We implemented an optimized backward DP with O(n * 26) time and O(n * 78) memory using `array('i')` for compact storage. The key insight is precomputing `best[c] = |s[i] - c| + dp[i+1][c][1]` and then using its minimum and second minimum to handle the "start new run" transition efficiently in O(1) per state. The reconstruction phase greedily picks the smallest character at each position that maintains the global minimum cost, which yields the lexicographically smallest valid caption. This approach correctly handles edge cases (e.g., impossible cases for n<3) and passes the provided examples.

## worker: Implement the optimized backward DP and reconstruc
The solution uses a backward dynamic programming approach with state `(position, character, run_length)`, where `run_length` is capped at 3. The transition from state `(i, c, k)` considers either continuing the current run (if `k < 3`) or starting a new run of a different character (only if `k == 3`). The "start new run" cost is optimized by precomputing `best[c] = |s[i] - c| + dp[i+1][c][1]` and using the minimum and second minimum values to handle the exclusion of the current character in O(1). The DP array is stored in a flat `array('i')` for memory efficiency (about 16 MB for n=5e4). After computing the global minimum cost, reconstruction greedily picks the smallest possible character at each position that maintains the global minimum, ensuring lexicographic minimality. Edge cases like n<3 are handled automatically by the DP returning infinity when no valid state exists.
