import sys

MOD = 998244353

def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1].strip()

    # ---------- factorials ----------
    max_n = N
    fact = [1] * (max_n + 1)
    for i in range(1, max_n + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (max_n + 1)
    inv_fact[max_n] = pow(fact[max_n], MOD - 2, MOD)
    for i in range(max_n, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    # ---------- parse the string into a forest ----------
    children = []                # children[i] = list of child node ids of node i
    stack = []                  # stack of currently open '(' node ids
    top_level = []              # children of the dummy root (top‑level blocks)

    for ch in S:
        if ch == '(':
            node_id = len(children)
            children.append([])
            stack.append(node_id)
        else:                     # ')'
            node_id = stack.pop()
            if stack:
                parent = stack[-1]
                children[parent].append(node_id)
            else:
                top_level.append(node_id)

    M = len(children)            # number of real nodes = N // 2

    # ---------- DP for real nodes (bottom‑up) ----------
    type_id = [-1] * M           # type id of each real node
    type_dp = []                 # DP value for each type
    key_to_type = {}             # canonical key -> type id

    # children have larger ids, so processing backwards guarantees children are ready
    for v in range(M - 1, -1, -1):
        childs = children[v]

        # frequency of child types
        freq = {}
        for c in childs:
            t = type_id[c]
            freq[t] = freq.get(t, 0) + 1

        k = len(childs)
        cur = fact[k]
        for t, cnt in freq.items():
            cur = cur * pow(type_dp[t], cnt, MOD) % MOD
            cur = cur * inv_fact[cnt] % MOD

        # canonical key: sorted list of (type, count)
        key = tuple(sorted(freq.items()))
        if key not in key_to_type:
            new_type = len(type_dp)
            key_to_type[key] = new_type
            type_dp.append(cur)
        else:
            new_type = key_to_type[key]   # the same DP must be stored already
            # (optional) assert type_dp[new_type] == cur
        type_id[v] = new_type

    # ---------- DP for the dummy root (concatenation of top‑level blocks) ----------
    freq = {}
    for v in top_level:
        t = type_id[v]
        freq[t] = freq.get(t, 0) + 1
    k = len(top_level)
    ans = fact[k]
    for t, cnt in freq.items():
        ans = ans * pow(type_dp[t], cnt, MOD) % MOD
        ans = ans * inv_fact[cnt] % MOD

    print(ans % MOD)


if __name__ == "__main__":
    solve()