import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    S = data[1].strip() if len(data) >= 2 else ""

    # Build the ordered forest. Node 0 is the artificial root.
    children = [[]]
    stack = [0]
    for ch in S:
        if ch == '(':
            u = len(children)
            children.append([])
            children[stack[-1]].append(u)
            stack.append(u)
        else:
            stack.pop()

    num_nodes = len(children)

    max_deg = 0
    for c in children:
        if len(c) > max_deg:
            max_deg = len(c)

    # Factorials and inverse factorials up to the maximum number of children.
    fact = [1] * (max_deg + 1)
    for i in range(1, max_deg + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (max_deg + 1)
    invfact[max_deg] = pow(fact[max_deg], MOD - 2, MOD)
    for i in range(max_deg, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # Bottom-up canonical IDs for unordered rooted subtree isomorphism classes.
    # Parent indices are always smaller than child indices, so reverse order works.
    node_id = [0] * num_nodes
    id_map = {}
    next_id = 0
    ans = 1

    for u in range(num_nodes - 1, -1, -1):
        ids = [node_id[v] for v in children[u]]
        ids.sort()

        key = tuple(ids)
        cid = id_map.get(key)
        if cid is None:
            cid = next_id
            id_map[key] = cid
            next_id += 1
        node_id[u] = cid

        # Multiply by the multinomial coefficient for ordering this node's children.
        deg = len(ids)
        ans = ans * fact[deg] % MOD

        i = 0
        while i < deg:
            j = i + 1
            while j < deg and ids[j] == ids[i]:
                j += 1
            ans = ans * invfact[j - i] % MOD
            i = j

    print(ans)

if __name__ == "__main__":
    main()