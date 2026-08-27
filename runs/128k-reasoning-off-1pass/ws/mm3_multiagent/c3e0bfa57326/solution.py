import sys

def solve():
    sys.setrecursionlimit(10000)
    MOD = 998244353
    N = int(sys.stdin.readline())
    S = sys.stdin.readline().strip()
    
    # Parse S into a parse tree (Dyck tree) with a dummy root (node 0).
    # Each node has a list of children.
    # Using stack: stack[-1] is the current parent.
    nodes = [[] for _ in range(N // 2 + 1)]  # nodes[i] = list of children of node i
    stack = [0]  # start with dummy root
    node_idx = 1
    for c in S:
        if c == '(':
            nodes[stack[-1]].append(node_idx)
            stack.append(node_idx)
            node_idx += 1
        else:  # ')'
            stack.pop()
    
    M = node_idx  # total number of nodes (including dummy root)
    
    # Get a post-order traversal of the tree (children before parent).
    post_order = []
    def dfs(u):
        for v in nodes[u]:
            dfs(v)
        post_order.append(u)
    dfs(0)
    
    # Canonicalize trees using a dictionary mapping tuple of child IDs to a unique integer.
    tree_dict = {(): 0}
    next_id = 1
    
    ID = [0] * M
    IDR = [0] * M
    
    # Process in post-order (children already processed).
    for u in post_order:
        if u == 0:
            continue  # skip dummy root for now
        # Compute ID for the original subtree rooted at u.
        key = tuple(ID[child] for child in nodes[u])
        if key in tree_dict:
            ID[u] = tree_dict[key]
        else:
            ID[u] = next_id
            tree_dict[key] = next_id
            next_id += 1
        
        # Compute IDR for the reversed subtree R(u).
        # R(u) has children R(ck), ..., R(c1) in that order.
        keyR = tuple(IDR[child] for child in reversed(nodes[u]))
        if keyR in tree_dict:
            IDR[u] = tree_dict[keyR]
        else:
            IDR[u] = next_id
            tree_dict[keyR] = next_id
            next_id += 1
    
    # For the root, we need to compute the answer from its children.
    # Group children of the root by their t-orbit key.
    root_children = nodes[0]
    k = len(root_children)
    
    # Precompute factorials and inverse factorials.
    fact = [1] * (k + 1)
    for i in range(1, k + 1):
        fact[i] = fact[i-1] * i % MOD
    inv_fact = [1] * (k + 1)
    inv_fact[k] = pow(fact[k], MOD-2, MOD)
    for i in range(k, 0, -1):
        inv_fact[i-1] = inv_fact[i] * i % MOD
    
    # Group children by t-orbit key.
    groups = {}  # key -> [count, tsize]
    for child in root_children:
        id1 = ID[child]
        id2 = IDR[child]
        key = (min(id1, id2), max(id1, id2))
        tsize = 1 if id1 == id2 else 2
        if key not in groups:
            groups[key] = [1, tsize]
        else:
            groups[key][0] += 1
            # tsize should be the same for same key, but no need to check.
    
    # Compute answer: (k! / prod m_i!) * prod |Q_i|^{m_i}
    ans = fact[k]
    for cnt, tsize in groups.values():
        ans = ans * pow(tsize, cnt, MOD) % MOD
        ans = ans * inv_fact[cnt] % MOD
    
    print(ans)

if __name__ == "__main__":
    solve()