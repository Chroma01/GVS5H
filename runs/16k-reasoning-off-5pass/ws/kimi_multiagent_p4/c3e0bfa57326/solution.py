import sys

def main():
    MOD = 998244353
    data = sys.stdin.read().split()
    N = int(data[0])
    S = data[1].strip()

    # Build tree: children lists. Node 0 = virtual root.
    children = [[]]
    stack = [0]
    for ch in S:
        if ch == '(':
            children.append([])
            stack.append(len(children) - 1)
        else:  # ')'
            node = stack.pop()
            children[stack[-1]].append(node)

    # Factorials and inverse factorials up to N
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # Iterative post-order over the whole forest (virtual root included)
    type_id = [0] * len(children)
    cnt = [0] * len(children)
    canon = {}  # sorted tuple of child type ids -> id
    rep_node = {}  # type id -> a node with that type (for cnt lookup)

    order = []
    st = [(0, False)]
    while st:
        node, processed = st.pop()
        if processed:
            order.append(node)
        else:
            st.append((node, True))
            for c in children[node]:
                st.append((c, False))

    for node in order:
        kids = children[node]
        ids = sorted(type_id[c] for c in kids)
        key = tuple(ids)
        tid = canon.get(key)
        if tid is None:
            tid = len(canon)
            canon[key] = tid
        type_id[node] = tid
        rep_node[tid] = node

        # cnt(node) = (total)! * prod over type classes ( cnt(class)^m / m! )
        total = len(kids)
        ways = fact[total]
        i = 0
        while i < total:
            j = i
            while j < total and ids[j] == ids[i]:
                j += 1
            m = j - i
            rep = rep_node[ids[i]]
            ways = ways * invfact[m] % MOD
            ways = ways * pow(cnt[rep], m, MOD) % MOD
            i = j
        cnt[node] = ways

    print(cnt[0] % MOD)

main()