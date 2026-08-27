import sys
sys.setrecursionlimit(1 << 25)

def solve():
    import sys
    input = sys.stdin.readline
    N, M = map(int, input().split())
    adj = [[] for _ in range(N + 1)]
    for _ in range(M):
        x, y, z = map(int, input().split())
        adj[x].append((y, z))
        if x != y:  # avoid duplicate edge for self-loop, but still keep once
            adj[y].append((x, z))

    # visited, offset (relative to component root), component id
    visited = [False] * (N + 1)
    offset = [0] * (N + 1)
    comp_id = [-1] * (N + 1)
    components = []          # list of lists of nodes per component
    offsets_per_comp = []    # list of offset lists per component

    # BFS/DFS to assign offsets and check consistency
    from collections import deque
    for start in range(1, N + 1):
        if visited[start]:
            continue
        comp_nodes = []
        comp_offsets = []
        q = deque([start])
        visited[start] = True
        offset[start] = 0
        cur_comp = len(components)
        comp_id[start] = cur_comp
        comp_nodes.append(start)
        comp_offsets.append(0)
        ok = True
        while q and ok:
            u = q.popleft()
            for v, w in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    offset[v] = offset[u] ^ w
                    comp_id[v] = cur_comp
                    comp_nodes.append(v)
                    comp_offsets.append(offset[v])
                    q.append(v)
                else:
                    # check consistency
                    if (offset[u] ^ offset[v]) != w:
                        ok = False
                        break
        if not ok:
            print(-1)
            return
        components.append(comp_nodes)
        offsets_per_comp.append(comp_offsets)

    # ---------- binary trie DP to find best x for each component ----------
    MAX_BIT = 30  # enough for values up to 10^9 (2^30 > 10^9)

    class TrieNode:
        __slots__ = ('child', 'cnt')
        def __init__(self):
            self.child = [None, None]  # 0 and 1 children
            self.cnt = 0               # number of numbers that pass this node

    def insert(root, val):
        node = root
        for b in range(MAX_BIT, -1, -1):
            bit = (val >> b) & 1
            if node.child[bit] is None:
                node.child[bit] = TrieNode()
            node = node.child[bit]
            node.cnt += 1

    # returns (best_x, minimal_sum) for the component using trie rooted at root
    def solve_trie(root):
        # dp returns (best_x, best_sum) for the subtree, given that we are at bit b
        # we'll implement a recursive function that returns (best_x_prefix, min_cost_for_lower_bits)
        # and at each step decide bit value
        def dfs(node, b):
            if node is None or node.cnt == 0:
                return (0, 0)  # no numbers, x bits arbitrary, cost 0
            if b < 0:
                return (0, 0)
            left = node.child[0]
            right = node.child[1]
            cntL = left.cnt if left else 0
            cntR = right.cnt if right else 0
            # Option 0: set current bit of x to 0
            # cost added at this bit: cntR * 2^b
            cost0 = cntR * (1 << b)
            best0, sum0 = dfs(left, b - 1)
            total0 = cost0 + sum0
            # Option 1: set current bit of x to 1
            cost1 = cntL * (1 << b)
            best1, sum1 = dfs(right, b - 1)
            total1 = cost1 + sum1
            if total0 <= total1:
                return (best0, total0)
            else:
                return (best1 | (1 << b), total1)
        best_x, min_sum = dfs(root, MAX_BIT)
        return best_x, min_sum

    ans = [0] * (N + 1)
    for idx, comp_nodes in enumerate(components):
        # build trie for this component
        root = TrieNode()
        for off in offsets_per_comp[idx]:
            insert(root, off)
        best_x, _ = solve_trie(root)
        # assign answers
        for node in comp_nodes:
            ans[node] = best_x ^ offset[node]

    print(' '.join(map(str, ans[1:])))

if __name__ == "__main__":
    solve()