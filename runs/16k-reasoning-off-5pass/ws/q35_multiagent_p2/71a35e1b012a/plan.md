1.  **Analyze the Operations**: Operation 1 sets a range `[L, R]` to 1. Operation 2 sets the complement `[1, L-1] U [R+1, N]` to 1. Operation 0 does nothing. We want all positions `1..N` to be 1.
2.  **Identify Unreachable Cases**: If there is a gap between consecutive intervals that cannot be covered by any Operation 2 (which covers the "outside" of an interval), it might be impossible. Specifically, if we only use Operation 1s, we need the union of chosen intervals to cover `[1, N]`. If we use Operation 2s, they cover the "exterior". Note that Operation 2 on `[L, R]` effectively sets `1..L-1` and `R+1..N` to 1.
3.  **Dynamic Programming Approach**: Let `dp[i]` be the minimum cost to make the prefix `1..i` all 1s, considering the operations in order. However, the operations are given in a fixed sequence, and each operation must be decided immediately. This suggests we process operations one by one. But the state needs to capture which positions are currently 1. Since N is large, we can't track the exact array.
4.  **Key Insight**: The problem can be modeled by tracking the "rightmost contiguous block of 1s starting from 1" or more generally, the set of covered indices. However, Operation 2 is tricky because it sets disjoint parts to 1.
    Actually, let's look at the structure. We want to cover `[1, N]`.
    - Operation 1 on `[L, R]` covers `[L, R]`.
    - Operation 2 on `[L, R]` covers `[1, L-1]` and `[R+1, N]`.
    
    This looks like a shortest path problem on a graph where nodes represent the state of coverage. But the state space is huge.
    
    Alternative View:
    Let's define `dp[i]` as the minimum cost to ensure that position `i` is 1, AND all positions `1..i-1` are also 1? No, because Operation 2 might cover `1..L-1` and `R+1..N` leaving a hole in the middle.
    
    Let's reconsider. We process operations `1` to `M`. We need to decide for each op whether to use Op 0, 1, or 2.
    The final state must have all `x_j = 1`.
    
    Let's use DP where `dp[i]` is the minimum cost to have the prefix `1..i` fully covered by 1s, *assuming* that we don't care about positions `> i` yet, OR that positions `> i` might be covered by future operations. This is tricky because an Operation 2 later might cover a gap in the middle.
    
    Actually, notice that Operation 2 on `[L, R]` sets `1..L-1` to 1. This is very powerful for the prefix.
    
    Let `dp[i]` = minimum cost to make `x_1 ... x_i` all equal to 1.
    To compute `dp[i]`, we can look at the last operation that helped cover up to `i`.
    However, the operations are sequential. We must decide `op_1, ..., op_M`.
    
    Let's flip the DP: `dp[k][i]` = min cost using first `k` operations to cover prefix `1..i`.
    State: `dp[i]` = min cost to cover `1..i`.
    Initialize `dp[0] = 0`, `dp[i] = infinity` for `i > 0`.
    
    For each operation `(L, R)` with cost 1 (Op 1 or Op 2) or 0 (Op 0):
    - Op 0: `dp` array doesn't change.
    - Op 1: If we apply Op 1, it sets `x[L..R] = 1`. This helps if we already have `1..L-1` covered. Then the new covered prefix becomes `max(i, R)`? No, it connects `1..L-1` with `L..R` to form `1..R`. So if we had `1..L-1` covered with cost `C`, we can now have `1..R` covered with cost `C+1`.
      Transition: `dp[R] = min(dp[R], dp[L-1] + 1)`.
      Also, if we had a larger covered prefix `j >= L`, applying Op 1 doesn't extend the prefix beyond `max(j, R)`. But since we want to minimize cost for a specific prefix length, and Op 1 only adds `1`s in `[L, R]`, it effectively extends a coverage ending at `L-1` to `R`. It doesn't help extend a coverage that already goes past `L`.
      Wait, what if `dp[j]` is defined as min cost to cover `1..j`?
      If we have `1..j` covered, and we apply Op 1 on `[L, R]`:
      - If `R <= j`, no change to the prefix coverage.
      - If `L <= j < R`, then `1..R` becomes covered. Cost increases by 1.
      - If `L > j`, then `1..j` is still covered, but `j+1..L-1` are not. The prefix coverage remains `j`.
      
      So, Op 1 allows transitioning from state `L-1` to `R` with cost +1. It also allows transitioning from any state `j >= L-1` to `max(j, R)` with cost +1. But since `dp` is non-decreasing with index? No, `dp[i]` is cost to cover `i`. Usually covering more is harder or equal cost. So `dp[i] <= dp[i+1]`? Not necessarily. Covering `1..10` might cost 5, covering `1..5` might cost 2. So `dp` is non-decreasing with `i`.
      
    - Op 2: Sets `1..L-1` and `R+1..N` to 1.
      This sets the prefix `1..L-1` to 1.
      So if we apply Op 2, we can achieve coverage of `1..L-1` with cost +1, regardless of previous state?
      Yes, because Op 2 explicitly sets `1..L-1` to 1.
      So: `dp[L-1] = min(dp[L-1], dp[any] + 1)`?
      Actually, Op 2 sets `1..L-1` to 1. It doesn't depend on previous state for the prefix `1..L-1`. It just costs 1.
      So `dp[L-1] = min(dp[L-1], 1)`? No, we can combine with previous costs.
      `dp[L-1] = min(dp[L-1], min_{k} (dp[k]) + 1)`. Since `min_k dp[k]` is likely `dp[0]=0` (if we consider empty prefix cost 0), this means `dp[L-1] = min(dp[L-1], 1)`.
      Wait, does Op 2 help extend beyond `L-1`? It sets `R+1..N` to 1. This doesn't help the *prefix* `1..i` unless `i <= L-1`. For `i > L-1`, the gap `L..R` is still 0 (unless covered by other ops). So Op 2 primarily helps establish the prefix `1..L-1`.
      
    So the transitions for operation `(L, R)`:
    1.  **Op 0**: No change.
    2.  **Op 1**: 
        - Can extend a coverage ending at `L-1` to `R`.
        - `dp[R] = min(dp[R], dp[L-1] + 1)`
        - Also, if we already have `1..j` covered with `j >= L`, applying Op 1 might extend it to `max(j, R)`.
        - `dp[max(j, R)] = min(dp[max(j, R)], dp[j] + 1)` for all `j >= L-1`.
        - Since `dp` is non-decreasing, the best way to extend a large `j` is to take the smallest cost `dp[j]` for `j >= L-1`. Let `min_dp_ge = min(dp[L-1], dp[L], ..., dp[N])`.
        - Then `dp[R] = min(dp[R], min_dp_ge + 1)`? No, if `j > R`, `max(j, R) = j`, so it doesn't extend. It only extends if `j < R`.
        - So specifically: `dp[R] = min(dp[R], dp[L-1] + 1)`.
        - And for any `j` such that `L-1 <= j < R`, we can update `dp[R]` from `dp[j] + 1`. Since `dp` is non-decreasing, `dp[L-1]` is the smallest among `dp[L-1]...dp[R-1]`. So `dp[R] = min(dp[R], dp[L-1] + 1)` covers the extension from any `j < R` if we assume we just take the best prefix ending before `L`.
        - What if we have `1..j` covered with `j >= R`? Then Op 1 doesn't change the prefix coverage.
        
    3.  **Op 2**:
        - Sets `1..L-1` to 1.
        - This means we can achieve state `L-1` with cost `current_min_cost + 1`.
        - `current_min_cost` is the minimum cost to achieve *any* valid state before this op. Since we can always choose to ignore previous coverage and just use Op 2 to set `1..L-1`, the cost is `1 + min_{k} dp[k]`.
        - Note: `min_k dp[k]` is `dp[0] = 0`. So `dp[L-1] = min(dp[L-1], 1)`.
        - Does Op 2 help with `i > L-1`? No, because `L..R` becomes 0 (or stays 0). So it doesn't extend the prefix.
        
    So the algorithm:
    Initialize `dp[0] = 0`, `dp[1..N] = infinity`.
    We also need to reconstruct the solution, so we store which operation was chosen.
    
    For each op `(L, R)`:
    - Calculate potential new values.
    - `new_dp` copy of `dp`.
    - **Op 2**: `cost2 = min(dp) + 1`. If `cost2 < new_dp[L-1]`, update `new_dp[L-1] = cost2` and record choice.
    - **Op 1**: `cost1 = dp[L-1] + 1`. If `cost1 < new_dp[R]`, update `new_dp[R] = cost1` and record choice.
      - Wait, is it possible that `dp[j] + 1 < new_dp[R]` for some `j > L-1`?
      - If `j >= R`, `max(j, R) = j`, so it updates `dp[j]`, not `dp[R]`.
      - If `L-1 <= j < R`, it updates `dp[R]`. Since `dp` is non-decreasing, `dp[L-1]` is the minimum in `dp[L-1...R-1]`. So checking `dp[L-1] + 1` is sufficient for updating `dp[R]`.
      
    After processing all M operations, check `dp[N]`. If infinity, output -1.
    Else, backtrack to find the operations.
    
    One detail: `min(dp)` for Op 2. We can maintain the global minimum of `dp` array.
    
    Backtracking:
    We need to store for each step `k` and each state `i`, what was the previous state and operation.
    Since N is 10^6 and M is 2*10^5, storing a full table `M x N` is too big.
    However, notice that `dp[i]` only changes at specific indices.
    Actually, we can just store the decision for the *optimal path*.
    But there are multiple states.
    
    Alternative: Store `parent[k][i]`? Too big.
    
    Let's observe the transitions.
    Op 2 updates `dp[L-1]`.
    Op 1 updates `dp[R]`.
    
    We can store `choice[k][i]` only for the states that are reachable or optimal?
    Or, we can run the DP forward, storing `dp[k][i]` for all `k, i`?
    Memory: `200000 * 1000000` is too big.
    
    We need a more efficient reconstruction.
    Notice that we only care about `dp[N]` at the end.
    We can store `prev_state[k][i]`? No.
    
    Let's store the `dp` array at each step? No.
    
    Idea: Since we only update `dp[L-1]` and `dp[R]`, most of the `dp` array remains unchanged.
    We can use a persistent segment tree or just store the changes.
    But simpler: Just store the entire `dp` table if we use 1D array and overwrite? No, we need history for backtracking.
    
    Wait, `M` is 200,000. `N` is 1,000,000.
    We can store `history[k]` = the index `i` that was updated? No, multiple indices can be updated?
    In each step, we update at most 2 indices: `L-1` (via Op 2) and `R` (via Op 1).
    So we can store `updates[k]` = list of `(index, new_value, prev_index, op_type)`.
    
    Backtracking:
    Start with `best_i = N` at step `M`.
    Find the value `dp[M][N]`.
    Check if it came from `dp[M-1][N]` (Op 0 or Op 1/2 didn't change N) or from an update.
    If `dp[M][N]` was updated by Op 1 at step M to `R=N`, then previous state was `L-1` at step `M-1`.
    If `dp[M][N]` was updated by Op 2 at step M to `L-1=N`, then previous state was `any` (min) at step `M-1`.
    
    This requires knowing the "min" state at step `M-1`.
    
    Let's refine the storage:
    `dp[i]` current best cost to cover `1..i`.
    `history[k]` stores a dictionary/map of changes: `{index: (new_cost, prev_index, op_type)}`.
    Also store `global_min[k]` = min value in `dp` array at step `k`.
    
    Backtracking from `k=M, i=N`:
    Get `history[M]`.
    If `N` is in `history[M]`:
       Let `(cost, prev_i, op) = history[M][N]`.
       If `op == 1`: `prev_i` is `L-1`. We go to step `M-1`, state `L-1`.
       If `op == 2`: `prev_i` is `None` (came from global min). We need to find which state `j` gave the global min at step `M-1`.
       If `op == 0` or `N` not in history:
          The value `dp[M][N]` is same as `dp[M-1][N]`.
          We go to step `M-1`, state `N`.
          
    If `op == 2` and we need to find the state `j` that achieved `global_min[M-1]`:
       We need to know which index `j` had `dp[M-1][j] == global_min[M-1]`.
       We can store `min_index[k]` = an index `j` that achieves the minimum at step `k`.
       
    So, data structures:
    - `dp`: array of size N+1.
    - `history`: list of dicts, size M+1. `history[k]` maps `index -> (new_cost, prev_index, op)`.
    - `global_min`: array of size M+1.
    - `min_index`: array of size M+1.
    
    Initialization:
    `dp[0]=0`, others inf.
    `global_min[0]=0`, `min_index[0]=0`.
    
    Step k (1 to M), op `(L, R)`:
    `new_dp = dp[:]` (copy? No, too slow).
    We only modify `dp[L-1]` and `dp[R]`.
    
    Calculate `c2 = global_min[k-1] + 1`.
    Calculate `c1 = dp[L-1] + 1`. (Note: `dp[L-1]` is from step `k-1`).
    
    Determine updates:
    `updates = {}`
    
    // Op 2 update for L-1
    if `c2 < dp[L-1]`:
        `updates[L-1] = (c2, None, 2)` // None indicates came from global min
        `dp[L-1] = c2`
        
    // Op 1 update for R
    if `c1 < dp[R]`:
        `updates[R] = (c1, L-1, 1)`
        `dp[R] = c1`
        
    // Op 0 is implicit, no update needed if no better path.
    
    `history[k] = updates`
    `global_min[k] = min(global_min[k-1], min(updates.values()) if updates else global_min[k-1])`
    `min_index[k] = ...` find index with min value.
       If `global_min[k]` came from `global_min[k-1]`, `min_index[k] = min_index[k-1]`.
       Else, it came from an update. Check which updated index has the new min.
       
    Backtracking:
    `curr_i = N`
    `ops = []`
    For `k` from `M` down to 1:
       `L, R` = ops[k-1]
       `hist = history[k]`
       
       If `curr_i` in `hist`:
           `cost, prev_i, op_type = hist[curr_i]`
           `ops.append(op_type)`
           if `op_type == 2`:
               `curr_i = min_index[k-1]`
           else:
               `curr_i = prev_i`
       Else:
           `ops.append(0)`
           `curr_i` remains same.
           
    Reverse `ops`.