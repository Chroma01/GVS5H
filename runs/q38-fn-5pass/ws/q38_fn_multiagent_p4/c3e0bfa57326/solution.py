import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    N = int(data[0])
    S = data[1] if len(data) > 1 else ""

    # Build the ordered rooted forest.
    # Node 0 is the virtual root.
    children = [[]]
    stack = [0]

    for ch in S:
        if ch == '(':
            v = len(children)
            children.append([])
            children[stack[-1]].append(v)
            stack.append(v)
        else:
            stack.pop()

    m = len(children)

    # Factorials and inverse factorials modulo MOD.
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # Assign exact canonical IDs to unordered subtrees.
    # Children have smaller creation order than parents, so reverse order is postorder.
    cid = [0] * m
    id_map = {}
    next_id = 1
    ans = 1

    for v in range(m - 1, -1, -1):
        child_ids = [cid[u] for u in children[v]]
        child_ids.sort()

        key = tuple(child_ids)
        if key not in id_map:
            id_map[key] = next_id
            next_id += 1
        cid[v] = id_map[key]

        # Multinomial factor for ordering children of this node.
        d = len(child_ids)
        factor = fact[d]

        i = 0
        while i < d:
            j = i + 1
            while j < d and child_ids[j] == child_ids[i]:
                j += 1
            factor = factor * invfact[j - i] % MOD
            i = j

        ans = ans * factor % MOD

    print(ans)

if __name__ == "__main__":
    main()