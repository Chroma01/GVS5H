import sys

MOD = 998244353

def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    N = int(data[0])
    S = data[1] if len(data) > 1 else ""

    # Parse the balanced parenthesis string into a rooted forest.
    # Node 0 is a super-root whose children are the top-level components.
    children = [[] for _ in range(N + 1)]
    stack = [0]
    node_count = 1

    for ch in S:
        if ch == "(":
            u = node_count
            node_count += 1
            children[stack[-1]].append(u)
            stack.append(u)
        else:
            stack.pop()

    # Factorials and inverse factorials modulo MOD.
    fact = [1] * (node_count + 1)
    for i in range(1, node_count + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (node_count + 1)
    invfact[node_count] = pow(fact[node_count], MOD - 2, MOD)
    for i in range(node_count, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # Assign canonical IDs to unordered rooted subtrees bottom-up.
    # Node creation order is preorder, so reverse order processes children first.
    child_id = [0] * node_count
    type_id = {}
    next_id = 1

    ans = 1

    for u in range(node_count - 1, -1, -1):
        ids = [child_id[v] for v in children[u]]
        ids.sort()

        key = tuple(ids)
        cid = type_id.get(key)
        if cid is None:
            cid = next_id
            type_id[key] = cid
            next_id += 1

        child_id[u] = cid

        # Local multinomial factor for ordering children of this node.
        d = len(ids)
        if d > 1:
            factor = fact[d]
            i = 0
            while i < d:
                j = i + 1
                while j < d and ids[j] == ids[i]:
                    j += 1
                factor = factor * invfact[j - i] % MOD
                i = j
            ans = ans * factor % MOD

    print(ans)

if __name__ == "__main__":
    solve()