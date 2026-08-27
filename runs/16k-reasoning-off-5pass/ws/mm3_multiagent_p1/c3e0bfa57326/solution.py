import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1].strip()
    # Build parenthesis tree using stack
    # Each node corresponds to a matched pair of parentheses.
    # We'll store parent of each node.
    parent = [-1] * (N // 2)  # number of pairs = N/2
    stack = []
    node_id = 0
    # We'll map each position to its node id (the pair it belongs to)
    pos_to_node = [0] * N
    for i, ch in enumerate(S):
        if ch == '(':
            # new node starts
            cur = node_id
            node_id += 1
            if stack:
                # stack top is the parent node id
                p = stack[-1]
                parent[cur] = p
            stack.append(cur)
            pos_to_node[i] = cur
        else:  # ')'
            cur = stack.pop()
            pos_to_node[i] = cur
    # Now we have parent array. Count children for each node.
    num_nodes = N // 2
    children_count = [0] * num_nodes
    for node in range(num_nodes):
        p = parent[node]
        if p != -1:
            children_count[p] += 1
    # Precompute factorials up to N (max children count <= N/2)
    max_fact = num_nodes
    fact = [1] * (max_fact + 1)
    for i in range(1, max_fact + 1):
        fact[i] = fact[i-1] * i % MOD
    ans = 1
    for cnt in children_count:
        ans = ans * fact[cnt] % MOD
    print(ans)

if __name__ == "__main__":
    main()