### CODE
import sys

# Increase recursion depth just in case
sys.setrecursionlimit(2000)

def solve():
    # Read all input at once
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        T_str = next(iterator)
        T = int(T_str)
    except StopIteration:
        return

    out = []
    
    for _ in range(T):
        try:
            N = int(next(iterator))
            A = [int(next(iterator)) for _ in range(N)]
        except StopIteration:
            break
            
        first = {}
        last = {}
        positions = {}
        
        for idx, val in enumerate(A):
            pos = idx + 1
            if val not in first:
                first[val] = pos
            last[val] = pos
            if val not in positions:
                positions[val] = []
            positions[val].append(pos)
            
        distinct_vals = list(first.keys())
        # Sort by first occurrence index
        distinct_vals.sort(key=lambda x: first[x])
        
        # BIT (Fenwick Tree)
        bit = [0] * (N + 1)
        
        def update(i, delta):
            while i <= N:
                bit[i] += delta
                i += i & (-i)
                
        def query(i):
            s = 0
            while i > 0:
                s += bit[i]
                i -= i & (-i)
            return s
            
        total_sum_L = 0
        computed_sum = 0
        total_added = 0
        
        # Process values in reverse order of first occurrence
        # This corresponds to processing from the end of the sorted list
        for val in reversed(distinct_vals):
            L_val = last[val]
            total_sum_L += L_val
            
            # Add L_val to BIT
            update(L_val, 1)
            total_added += 1
            
            # For each position p of val, we want to count how many L's (from values processed so far) are >= p.
            # The values processed so far are those with first occurrence >= first[val].
            # These are exactly the values v_i with i >= current_index in the sorted list.
            # We need to sum Count(val, L_{v_i}) for all i >= current_index.
            # Count(val, L_{v_i}) is the number of occurrences of val before L_{v_i}.
            # Which is equivalent to counting occurrences p of val such that p <= L_{v_i}.
            # So we sum over p in positions[val], the number of L's >= p.
            
            current_val_count = 0
            for p in positions[val]:
                # Count L's in range [p, N]
                # This is total_added - query(p - 1)
                s = 0
                idx_q = p - 1
                while idx_q > 0:
                    s += bit[idx_q]
                    idx_q -= idx_q & (-idx_q)
                current_val_count += (total_added - s)
            
            computed_sum += current_val_count
            
        # The formula derived is:
        # Total Cost = sum(L_v) - sum_{j} sum_{i>=j} Count(v_j, L_{v_i}) + d
        ans = total_sum_L - computed_sum + len(distinct_vals)
        out.append(str(ans))
        
    print('\n'.join(out))

if __name__ == '__main__':
    solve()