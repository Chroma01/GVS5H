import sys

MOD = 998244353

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    # N is data[0], S is data[1]
    S = data[1] if len(data) > 1 else ""

    children = []
    roots = []
    stack = []

    for ch in S:
        if ch == '(':
            idx = len(children)
            children.append([])
            if stack:
                children[stack[-1]].append(idx)
            else:
                roots.append(idx)
            stack.append(idx)
        else:
            stack.pop()

    M = len(children)

    fact = [1] * (M + 1)
    for i in range(1, M + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv_fact = [1] * (M + 1)
    inv_fact[M] = pow(fact[M], MOD - 2, MOD)
    for i in range(M, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    class_id = [-1] * M
    class_dp = []
    key_to_id = {}

    # Children always have larger indices than their parent, so reverse order is bottom-up.
    for idx in range(M - 1, -1, -1):
        ch_ids = [class_id[c] for c in children[idx]]
        ch_ids.sort()
        key = tuple(ch_ids)

        cid = key_to_id.get(key)
        if cid is None:
            cid = len(class_dp)
            key_to_id[key] = cid

            k = len(ch_ids)
            val = fact[k]
            i = 0
            while i < k:
                j = i + 1
                cur = ch_ids[i]
                while j < k and ch_ids[j] == cur:
                    j += 1
                m = j - i
                val = val * inv_fact[m] % MOD
                val = val * pow(class_dp[cur], m, MOD) % MOD
                i = j
            class_dp.append(val)

        class_id[idx] = cid

    root_ids = [class_id[r] for r in roots]
    root_ids.sort()
    K = len(root_ids)

    ans = fact[K]
    i = 0
    while i < K:
        j = i + 1
        cur = root_ids[i]
        while j < K and root_ids[j] == cur:
            j += 1
        m = j - i
        ans = ans * inv_fact[m] % MOD
        ans = ans * pow(class_dp[cur], m, MOD) % MOD
        i = j

    print(ans)


if __name__ == "__main__":
    solve()