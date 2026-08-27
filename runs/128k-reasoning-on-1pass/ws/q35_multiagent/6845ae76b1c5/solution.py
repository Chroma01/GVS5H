import sys

# Increase recursion depth to handle deep segment tree traversals safely
sys.setrecursionlimit(300000)

def solve():
    # Fast I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
        B = [int(next(iterator)) for _ in range(N)]
        K = int(next(iterator))
        queries = []
        for _ in range(K):
            queries.append((int(next(iterator)), int(next(iterator))))
    except StopIteration:
        return
        
    # Coordinate Compression
    vals = sorted(list(set(A + B)))
    comp = {v: i for i, v in enumerate(vals)}
    M = len(vals)
    
    # Persistent Segment Tree arrays
    # Index 0 represents an empty/null node
    left_child = [0]
    right_child = [0]
    cnt = [0]
    sum_val = [0]
    
    def new_node(l=0, r=0, c=0, s=0):
        left_child.append(l)
        right_child.append(r)
        cnt.append(c)
        sum_val.append(s)
        return len(cnt) - 1
        
    # Update function: creates a new version by adding val at idx
    def update(node, l, r, idx, val):
        new_node_idx = new_node()
        if l == r:
            cnt[new_node_idx] = cnt[node] + 1
            sum_val[new_node_idx] = sum_val[node] + val
            return new_node_idx
        mid = (l + r) >> 1
        if idx <= mid:
            left_child[new_node_idx] = update(left_child[node], l, mid, idx, val)
            right_child[new_node_idx] = right_child[node]
        else:
            left_child[new_node_idx] = left_child[node]
            right_child[new_node_idx] = update(right_child[node], mid + 1, r, idx, val)
        cnt[new_node_idx] = cnt[left_child[new_node_idx]] + cnt[right_child[new_node_idx]]
        sum_val[new_node_idx] = sum_val[left_child[new_node_idx]] + sum_val[right_child[new_node_idx]]
        return new_node_idx
        
    # Query function: computes sum of |a - b| for a in tree_a, b in tree_b
    def query(node_a, node_b, l, r):
        if l == r or node_a == 0 or node_b == 0:
            return 0
        mid = (l + r) >> 1
        l_a = left_child[node_a]
        r_a = right_child[node_a]
        l_b = left_child[node_b]
        r_b = right_child[node_b]
        
        # Recursive calls for pairs within the same child
        res = query(l_a, l_b, l, mid) + query(r_a, r_b, mid + 1, r)
        
        # Cross terms: A in left, B in right => a <= mid < b => |a-b| = b - a
        res += sum_val[r_b] * cnt[l_a] - sum_val[l_a] * cnt[r_b]
        # Cross terms: A in right, B in left => b <= mid < a => |a-b| = a - b
        res += sum_val[r_a] * cnt[l_b] - sum_val[l_b] * cnt[r_a]
        
        return res
        
    # Build persistent trees for A
    roots_A = [0]
    for x in A:
        roots_A.append(update(roots_A[-1], 0, M - 1, comp[x], x))
        
    # Build persistent trees for B
    roots_B = [0]
    for x in B:
        roots_B.append(update(roots_B[-1], 0, M - 1, comp[x], x))
        
    # Process queries
    results = []
    for x_k, y_k in queries:
        res = query(roots_A[x_k], roots_B[y_k], 0, M - 1)
        results.append(str(res))
        
    sys.stdout.write('\n'.join(results) + '\n')

if __name__ == '__main__':
    solve()