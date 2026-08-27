import sys
import random
sys.setrecursionlimit(10000)

MOD = 998244353

def solve():
    N = int(sys.stdin.readline())
    S = sys.stdin.readline().strip()
    if N % 2 == 1:
        print(0)
        return
    # Brute force for small N
    if N <= 20:
        from collections import deque
        def revcomp(sub):
            res = []
            L = len(sub)
            for i in range(L):
                j = L - 1 - i
                if sub[j] == '(':
                    res.append(')')
                else:
                    res.append('(')
            return ''.join(res)
        def is_valid(t):
            bal = 0
            for c in t:
                if c == '(':
                    bal += 1
                else:
                    bal -= 1
                if bal < 0:
                    return False
            return bal == 0
        seen = set()
        queue = deque()
        queue.append(S)
        seen.add(S)
        while queue:
            cur = queue.popleft()
            L = len(cur)
            for l in range(L):
                bal = 0
                for r in range(l, L):
                    if cur[r] == '(':
                        bal += 1
                    else:
                        bal -= 1
                    if bal == 0 and (r - l + 1) % 2 == 0:
                        sub = cur[l:r+1]
                        new_sub = revcomp(sub)
                        new_str = cur[:l] + new_sub + cur[r+1:]
                        if new_str not in seen:
                            seen.add(new_str)
                            queue.append(new_str)
        print(len(seen) % MOD)
        return
    # For large N, use tree DP with careful intersection handling
    # Build tree
    parent = [0]
    children = [[]]
    stack = []
    for c in S:
        if c == '(':
            node = len(parent)
            parent.append(stack[-1] if stack else 0)
            children.append([])
            if stack:
                children[parent[-1]].append(node)
            else:
                children[0].append(node)
            stack.append(node)
        else:
            stack.pop()
    
    # Compress single-child nodes
    new_children = []
    new_parent = []
    def compress(u):
        ch = children[u]
        if len(ch) == 0:
            new_id = len(new_children)
            new_children.append([])
            new_parent.append(-1)
            return new_id
        elif len(ch) == 1:
            return compress(ch[0])
        else:
            new_id = len(new_children)
            new_children.append([])
            new_parent.append(-1)
            for c in ch:
                cc = compress(c)
                new_children[new_id].append(cc)
                new_parent[cc] = new_id
            return new_id
    
    root_compressed = compress(0)
    
    if not new_children[root_compressed]:
        print(1)
        return
    
    M = len(new_children)
    # Post-order traversal
    order = []
    stack = [root_compressed]
    visited = [False]*M
    while stack:
        u = stack.pop()
        if visited[u]:
            continue
        visited[u] = True
        order.append(u)
        for v in new_children[u]:
            stack.append(v)
    order.reverse()
    
    # Assign random hash for "()"
    random.seed(42)
    leaf_hash = random.randint(1, 2**61-1)
    
    size_arr = [0]*M
    # For each node, store a canonical tuple representation
    # The tuple is invariant under reversal of children order
    # For internal nodes: tuple of children's canonical tuples, normalized to be the smaller of tuple and its reverse
    rep_arr = [None]*M
    # Also store hash for quick comparison
    hash_arr = [0]*M
    
    for u in order:
        ch = new_children[u]
        if not ch:
            size_arr[u] = 1
            rep_arr[u] = (leaf_hash,)
            hash_arr[u] = leaf_hash
        else:
            n = len(ch)
            child_sizes = [size_arr[v] for v in ch]
            child_reps = [rep_arr[v] for v in ch]
            # Compute product of sizes
            prod = 1
            for s in child_sizes:
                prod = prod * s % MOD
            # Compute intersection product
            inter_prod = 1
            for i in range(n//2):
                if child_reps[i] == child_reps[n-1-i]:
                    inter_prod = inter_prod * child_sizes[i] % MOD
                else:
                    inter_prod = 0
                    break
            if n % 2 == 1:
                mid = n//2
                inter_prod = inter_prod * child_sizes[mid] % MOD
            size_u = (2 * prod - inter_prod) % MOD
            # Compute canonical rep: min of tuple and reversed tuple
            tup = tuple(child_reps)
            rev_tup = tup[::-1]
            if tup <= rev_tup:
                rep_arr[u] = tup
            else:
                rep_arr[u] = rev_tup
            # Compute a hash of the rep for quick comparison
            h = 0
            for x in rep_arr[u]:
                h = (h * 1000003 + hash(x)) % (2**61-1)
            hash_arr[u] = h
            size_arr[u] = size_u
    
    print(size_arr[root_compressed] % MOD)

if __name__ == "__main__":
    solve()