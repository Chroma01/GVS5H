import sys
from collections import Counter

MOD = 998244353


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    s = data[1].decode() if len(data) > 1 else ""

    # Build the rooted forest. Each matched pair is one node.
    children = []
    roots = []
    stack = [-1]  # virtual root is represented by -1

    for ch in s:
        if ch == '(':
            v = len(children)
            children.append([])
            if stack[-1] == -1:
                roots.append(v)
            else:
                children[stack[-1]].append(v)
            stack.append(v)
        else:
            stack.pop()

    m = len(children)
    fact = [1] * (m + 1)
    invfact = [1] * (m + 1)
    for i in range(1, m + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact[m] = pow(fact[m], MOD - 2, MOD)
    for i in range(m, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # type_id identifies the unordered rooted-tree type.
    signature_to_type = {}
    node_type = [-1] * m
    type_value = []

    # Node indices were created in preorder, hence children have larger indices.
    for v in range(m - 1, -1, -1):
        sig = tuple(sorted(node_type[u] for u in children[v]))

        tid = signature_to_type.get(sig)
        if tid is None:
            tid = len(type_value)
            signature_to_type[sig] = tid

            cnt = Counter(sig)
            ways = fact[len(sig)]
            for child_type, amount in cnt.items():
                ways = ways * invfact[amount] % MOD
                ways = ways * pow(type_value[child_type], amount, MOD) % MOD
            type_value.append(ways)

        node_type[v] = tid

    root_types = [node_type[v] for v in roots]
    cnt = Counter(root_types)
    ans = fact[len(root_types)]
    for tid, amount in cnt.items():
        ans = ans * invfact[amount] % MOD
        ans = ans * pow(type_value[tid], amount, MOD) % MOD

    print(ans)


if __name__ == "__main__":
    solve()