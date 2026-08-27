import sys

MOD = 998244353

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    s = data[1]

    # Node 0 is a virtual root representing the top-level forest.
    children = [[]]
    stack = [0]

    for c in s:
        if c == '(':
            v = len(children)
            children.append([])
            children[stack[-1]].append(v)
            stack.append(v)
        else:
            stack.pop()

    m = n // 2
    fact = [1] * (m + 1)
    for i in range(1, m + 1):
        fact[i] = fact[i - 1] * i % MOD

    ifact = [1] * (m + 1)
    ifact[m] = pow(fact[m], MOD - 2, MOD)
    for i in range(m, 0, -1):
        ifact[i - 1] = ifact[i] * i % MOD

    # Canonical IDs for unordered rooted tree types.
    type_id = [0] * len(children)
    ways = [1] * len(children)
    ids = {}
    next_id = 0

    # Nodes are created before all descendants, so reverse creation order is postorder.
    for v in range(len(children) - 1, -1, -1):
        ch = children[v]
        k = len(ch)

        freq = {}
        value = fact[k]
        for u in ch:
            value = value * ways[u] % MOD
            t = type_id[u]
            freq[t] = freq.get(t, 0) + 1

        for count in freq.values():
            value = value * ifact[count] % MOD

        ways[v] = value

        key = tuple(sorted(freq.items()))
        if key not in ids:
            ids[key] = next_id
            next_id += 1
        type_id[v] = ids[key]

    print(ways[0])

if __name__ == "__main__":
    solve()