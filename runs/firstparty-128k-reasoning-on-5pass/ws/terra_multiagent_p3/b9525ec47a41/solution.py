import sys

MOD = 998244353

def canon_labels(roots):
    mp = {}
    res = []
    nxt = 0
    for x in roots:
        if x not in mp:
            mp[x] = nxt
            nxt += 1
        res.append(mp[x])
    return tuple(res)

# All partitions of (hub, vertex 0, current vertex).
states = [
    (0, 0, 0),
    (0, 0, 1),
    (0, 1, 0),
    (0, 1, 1),
    (0, 1, 2),
]
state_id = {x: i for i, x in enumerate(states)}

# trans[has_spoke][old_state] = list of (new_state, multiplicity).
trans = [[None] * 5 for _ in range(2)]

for has_spoke in range(2):
    for si, st in enumerate(states):
        cnt = {}
        for use_spoke in range(has_spoke + 1):
            for use_rim in range(2):
                parent = list(range(4))

                def find(x):
                    while parent[x] != x:
                        parent[x] = parent[parent[x]]
                        x = parent[x]
                    return x

                def unite(a, b):
                    a = find(a)
                    b = find(b)
                    if a == b:
                        return False
                    parent[b] = a
                    return True

                # Reconstruct the old connectivity on:
                # 0 = hub, 1 = vertex 0, 2 = current vertex.
                for a in range(3):
                    for b in range(a):
                        if st[a] == st[b]:
                            unite(a, b)

                ok = True
                # 3 is the newly added cycle vertex.
                if use_spoke:
                    if not unite(0, 3):
                        ok = False
                if ok and use_rim:
                    if not unite(2, 3):
                        ok = False

                if ok:
                    ns = canon_labels([find(0), find(1), find(3)])
                    ni = state_id[ns]
                    cnt[ni] = cnt.get(ni, 0) + 1

        trans[has_spoke][si] = list(cnt.items())

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()

    # Before processing any rim edge, vertex 0 is also the current vertex.
    dp = [0] * 5
    if s[0] == '1':
        dp[state_id[(0, 0, 0)]] = 1  # spoke (0, hub) is selected
    dp[state_id[(0, 1, 1)]] += 1     # spoke is not selected

    # Add vertices 1..N-1 and their preceding rim edges.
    for i in range(1, n):
        tr = trans[1 if s[i] == '1' else 0]
        ndp = [0] * 5
        for old, value in enumerate(dp):
            if value:
                for new, mul in tr[old]:
                    ndp[new] += value * mul
        dp = [x % MOD for x in ndp]

    # Finally choose whether to add the closing rim edge (N-1, 0).
    ans = 0
    for i, st in enumerate(states):
        # Omitting it is always valid. Adding it is valid iff its endpoints
        # are currently in different connected components.
        ways = 2 if st[1] != st[2] else 1
        ans += dp[i] * ways

    print(ans % MOD)

if __name__ == "__main__":
    main()