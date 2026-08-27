import sys
sys.setrecursionlimit(10000)

MOD = 998244353

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    S = input_data[1].strip()
    
    # Parse S into a tree with a dummy root (index 0)
    # nodes[i] = list of children indices
    nodes = [[]]  # root at index 0
    stack = [0]
    for c in S:
        if c == '(':
            new_node = len(nodes)
            nodes.append([])
            nodes[stack[-1]].append(new_node)
            stack.append(new_node)
        else:  # ')'
            stack.pop()
    
    # Precompute factorials and inverse factorials up to N
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i-1] * i % MOD
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        inv_fact[i-1] = inv_fact[i] * i % MOD
    
    # type_id[i] = the type ID of node i
    type_id = [0] * len(nodes)
    # type_f[t] = f value for type t
    type_f = []
    # Map from canonical tuple to type ID
    type_dict = {}
    
    # Process nodes in reverse order (children before parents)
    # Skip root (index 0) for type assignment, but process it for f(root)
    for i in range(len(nodes) - 1, 0, -1):
        child_ids = [type_id[child] for child in nodes[i]]
        child_ids.sort()
        key = tuple(child_ids)
        if key not in type_dict:
            tid = len(type_f)
            type_dict[key] = tid
            type_f.append(0)  # placeholder
            type_id[i] = tid
        else:
            type_id[i] = type_dict[key]
        
        # Compute f(i)
        k = len(child_ids)
        if k == 0:
            f_val = 1
        else:
            # Count multiplicities
            f_val = fact[k]
            j = 0
            while j < k:
                t = child_ids[j]
                cnt = 1
                while j + cnt < k and child_ids[j+cnt] == t:
                    cnt += 1
                f_val = f_val * inv_fact[cnt] % MOD
                f_val = f_val * pow(type_f[t], cnt, MOD) % MOD
                j += cnt
        type_f[type_id[i]] = f_val
    
    # Compute f for the root (dummy root)
    root_children_ids = [type_id[child] for child in nodes[0]]
    root_children_ids.sort()
    k = len(root_children_ids)
    if k == 0:
        ans = 1
    else:
        ans = fact[k]
        j = 0
        while j < k:
            t = root_children_ids[j]
            cnt = 1
            while j + cnt < k and root_children_ids[j+cnt] == t:
                cnt += 1
            ans = ans * inv_fact[cnt] % MOD
            ans = ans * pow(type_f[t], cnt, MOD) % MOD
            j += cnt
    
    print(ans)

if __name__ == "__main__":
    solve()