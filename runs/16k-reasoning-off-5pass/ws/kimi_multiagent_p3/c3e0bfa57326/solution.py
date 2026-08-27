import sys

def main():
    MOD = 998244353
    data = sys.stdin.read().split()
    N = int(data[0])
    S = data[1].strip()

    # Build tree with a stack. Node 0 = virtual root (top-level forest).
    # children[i] = list of child node indices of node i.
    children = [[]]
    stack = [0]
    for ch in S:
        if ch == '(':
            children.append([])
            node = len(children) - 1
            children[stack[-1]].append(node)
            stack.append(node)
        else:  # ch == ')'
            stack.pop()

    # Canonical IDs for unordered rooted trees:
    # id(node) determined by the sorted tuple of child ids.
    canon = {}
    node_id = [0] * len(children)

    # Iterative post-order traversal.
    order = []
    st = [(0, False)]
    while st:
        v, processed = st.pop()
        if processed:
            order.append(v)
        else:
            st.append((v, True))
            for c in children[v]:
                st.append((c, False))

    for v in order:
        key = tuple(sorted(node_id[c] for c in children[v]))
        if key not in canon:
            canon[key] = len(canon)
        node_id[v] = canon[key]

    # Factorials and inverse factorials.
    fact = [1] * (N + 2)
    for i in range(1, N + 2):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (N + 2)
    inv_fact[N + 1] = pow(fact[N + 1], MOD - 2, MOD)
    for i in range(N + 1, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    # For each node (including virtual root), contribution =
    # k! / prod(m_i!), where m_i are multiplicities of equal child subtrees.
    ans = 1
    for v in range(len(children)):
        ch = children[v]
        k = len(ch)
        if k <= 1:
            continue
        ans = ans * fact[k] % MOD
        counts = {}
        for c in ch:
            cid = node_id[c]
            counts[cid] = counts.get(cid, 0) + 1
        for m in counts.values():
            if m > 1:
                ans = ans * inv_fact[m] % MOD

    print(ans)

main()