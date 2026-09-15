import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    s = data[1] if len(data) > 1 else ""
    MOD = 998244353

    # Build the forest. Node 0 is an artificial root representing top-level trees.
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

    m = len(children)

    # Factorials / inverse factorials up to N.
    fact = [1] * (n + 2)
    for i in range(1, n + 2):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (n + 2)
    inv_fact[n + 1] = pow(fact[n + 1], MOD - 2, MOD)
    for i in range(n + 1, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    # Canonical IDs for unordered rooted subtrees, bottom-up.
    # Children always have larger ids than their parent (preorder creation),
    # so iterating in decreasing id processes all children first.
    intern = {}
    cid = [0] * m
    for v in range(m - 1, -1, -1):
        key = tuple(sorted(cid[u] for u in children[v]))
        idx = intern.get(key)
        if idx is None:
            idx = len(intern)
            intern[key] = idx
        cid[v] = idx

    # Answer = product over all nodes of multinomial over child isomorphism-type frequencies.
    ans = 1
    for v in range(m):
        kids = children[v]
        k = len(kids)
        if k == 0:
            continue
        freq = {}
        for u in kids:
            t = cid[u]
            freq[t] = freq.get(t, 0) + 1
        mult = fact[k]
        for f in freq.values():
            mult = mult * inv_fact[f] % MOD
        ans = ans * mult % MOD

    print(ans % MOD)

main()