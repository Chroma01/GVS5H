import sys

# Increase recursion depth just in case, though we use iterative DP
sys.setrecursionlimit(20000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        X = int(next(iterator))
    except StopIteration:
        return

    foods = []
    for _ in range(N):
        v = int(next(iterator))
        a = int(next(iterator))
        c = int(next(iterator))
        foods.append((v, a, c))

    # dp[c] will store a list of tuples (v1, v2, v3) representing the non-dominated
    # vitamin combinations achievable with exactly c calories.
    # A state (v1, v2, v3) dominates (v1', v2', v3') if v1>=v1', v2>=v2', v3>=v3'
    # and at least one inequality is strict.
    # We maintain the list of non-dominated states for each cost.
    
    dp = [[] for _ in range(X + 1)]
    # Base case: cost 0 has (0,0,0)
    dp[0].append((0, 0, 0))
    
    for v_type, a_val, c_val in foods:
        # Iterate backwards to avoid using the same item twice for the same cost (0/1 Knapsack)
        for c in range(X - c_val, -1, -1):
            if not dp[c]:
                continue
            
            current_states = dp[c]
            
            # Determine the vitamin vector added by this food
            add_vec = (0, 0, 0)
            if v_type == 1:
                add_vec = (a_val, 0, 0)
            elif v_type == 2:
                add_vec = (0, a_val, 0)
            else:
                add_vec = (0, 0, a_val)
            
            new_states = []
            for (v1, v2, v3) in current_states:
                nv1, nv2, nv3 = v1 + add_vec[0], v2 + add_vec[1], v3 + add_vec[2]
                new_states.append((nv1, nv2, nv3))
            
            # Merge new_states into dp[c + c_val]
            target_idx = c + c_val
            existing = dp[target_idx]
            
            # Combine existing and new states
            all_states = existing + new_states
            
            # Filter non-dominated states
            # Sort by v1 descending, then v2 descending.
            # This allows us to efficiently filter: if a state has v3 >= min_v3_so_far,
            # it is dominated by a previously kept state (which has higher/equal v1, v2).
            all_states.sort(key=lambda x: (x[0], x[1]), reverse=True)
            
            filtered = []
            min_v3 = float('inf')
            
            for state in all_states:
                if state[2] < min_v3:
                    filtered.append(state)
                    min_v3 = state[2]
            
            dp[target_idx] = filtered

    # Find the answer: maximum min(v1, v2, v3) across all costs <= X
    ans = 0
    for c in range(X + 1):
        for (v1, v2, v3) in dp[c]:
            current_min = min(v1, v2, v3)
            if current_min > ans:
                ans = current_min
                
    print(ans)

if __name__ == '__main__':
    solve()