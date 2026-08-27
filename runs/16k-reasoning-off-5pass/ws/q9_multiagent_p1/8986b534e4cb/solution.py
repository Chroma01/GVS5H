import sys

# Increase recursion depth just in case
sys.setrecursionlimit(2000000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        Q = int(next(iterator))
    except StopIteration:
        return

    people = []
    for i in range(M):
        s = int(next(iterator))
        t = int(next(iterator))
        people.append({'id': i, 's': s, 't': t})
    
    queries = []
    for i in range(Q):
        l = int(next(iterator))
        r = int(next(iterator))
        queries.append({'id': i, 'l': l, 'r': r})
    
    # Step 1: Identify "Same Start" conflicts
    from collections import defaultdict
    same_s = defaultdict(list)
    for i, p in enumerate(people):
        same_s[p['s']].append(i)
    
    # Step 2: Identify "Same End" conflicts
    same_t = defaultdict(list)
    for i, p in enumerate(people):
        same_t[p['t']].append(i)
        
    # Step 3: Identify "Crossing" conflicts
    # Sort people by S. If S is same, sort by T.
    # We use the original index as the key for the final check.
    sorted_people = sorted(range(M), key=lambda x: (people[x]['s'], people[x]['t']))
    
    crossing_pairs = []
    # Iterate through the sorted list. 
    # For any i, the only candidate j > i that could satisfy S_j < T_i is the immediate next one 
    # because S is non-decreasing. If S_{i+1} >= T_i, then for all k > i+1, S_k >= S_{i+1} >= T_i.
    for idx in range(M - 1):
        u = sorted_people[idx]
        v = sorted_people[idx+1]
        
        # Check if S_u < S_v (strictly, to avoid same-start which is handled separately)
        if people[u]['s'] < people[v]['s']:
            # Check if they overlap in S range: S_v < T_u
            if people[v]['s'] < people[u]['t']:
                # Check if they cross: T_v > T_u
                if people[v]['t'] > people[u]['t']:
                    # Crossing: S_u < S_v < T_u < T_v
                    crossing_pairs.append((u, v))
    
    # Collect all bad pairs
    bad_pairs = []
    
    # Same S pairs
    for s in same_s:
        indices = same_s[s]
        # Sort indices to ensure u < v
        indices.sort()
        for k in range(len(indices) - 1):
            bad_pairs.append((indices[k], indices[k+1]))
            
    # Same T pairs
    for t in same_t:
        indices = same_t[t]
        indices.sort()
        for k in range(len(indices) - 1):
            bad_pairs.append((indices[k], indices[k+1]))
            
    # Crossing pairs
    bad_pairs.extend(crossing_pairs)
    
    # Remove duplicates to optimize
    bad_pairs = sorted(list(set(bad_pairs)))
    
    # We need to check if any pair (u, v) with u < v is contained in [L, R].
    # Condition: L <= u AND v <= R.
    # We process queries offline.
    # Sort queries by L descending.
    # Sort bad_pairs by u descending.
    # Iterate L from M down to 1.
    # Add pairs with u >= L to a data structure.
    # Query: Is there any pair with v <= R?
    # We use a Fenwick Tree (BIT) to mark positions v.
    
    bit = [0] * (M + 1)
    
    def update(idx, val):
        while idx <= M:
            bit[idx] += val
            idx += idx & (-idx)
            
    def query(idx):
        s = 0
        while idx > 0:
            s += bit[idx]
            idx -= idx & (-idx)
        return s
        
    # Sort queries by L descending
    queries.sort(key=lambda x: x['l'], reverse=True)
    # Sort bad_pairs by u descending
    bad_pairs.sort(key=lambda x: x[0], reverse=True)
    
    ptr = 0
    num_bad = len(bad_pairs)
    
    results = [False] * Q
    
    for q in queries:
        l, r = q['l'], q['r']
        q_id = q['id']
        
        # Add all pairs with u >= l
        while ptr < num_bad and bad_pairs[ptr][0] >= l:
            u, v = bad_pairs[ptr]
            # Ensure u < v (should be true by construction, but safe check)
            if u < v:
                update(v, 1)
            ptr += 1
            
        # Check if any v <= r is marked
        if query(r) > 0:
            results[q_id] = False # Conflict found
        else:
            results[q_id] = True # No conflict
            
    # Output results
    output = []
    for res in results:
        output.append("Yes" if res else "No")
        
    print('\n'.join(output))

if __name__ == '__main__':
    solve()