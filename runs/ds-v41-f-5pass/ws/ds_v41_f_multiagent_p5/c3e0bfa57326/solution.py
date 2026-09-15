import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1] if len(data) > 1 else ""
    MOD = 998244353

    # Parse the valid parenthesis sequence into a rooted forest.
    # Node 0 is a virtual root; every top-level component becomes its child.
    children = [[]]
    stack = [0]
    for ch in s:
        if ch == '(':
            v = len(children)
            children.append([])
            children[stack[-1]].append(v)
            stack.append(v)
        else:
            stack.pop()

    m = len(children)  # number of nodes incl. virtual root

    # factorials / inverse factorials up to m
    fact = [1] * (m + 1)
    for i in range(1, m + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (m + 1)
    inv_fact[m] = pow(fact[m], MOD - 2, MOD)
    for i in range(m, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    # Reverse creation order == children before parents (preorder creation).
    ids = [0] * m
    idmap = {}
    ans = 1

    for v in range(m - 1, -1, -1):
        ch_list = children[v]
        d = len(ch_list)
        cids = [ids[c] for c in ch_list]
        cids.sort()
        key = tuple(cids)
        if key not in idmap:
            idmap[key] = len(idmap)
        ids[v] = idmap[key]

        # multinomial coefficient d! / prod(freq!) for this node
        ans = ans * fact[d] % MOD
        prev = -1
        cnt = 0
        for cid in cids:
            if cid == prev:
                cnt += 1
            else:
                if prev != -1:
                    ans = ans * inv_fact[cnt] % MOD
                prev = cid
                cnt = 1
        if prev != -1:
            ans = ans * inv_fact[cnt] % MOD

    print(ans % MOD)

main()