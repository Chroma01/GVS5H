import sys

def main():
    MOD = 998244353
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1] if len(data) > 1 else ""

    # Parse into a rooted forest. children[i] = list of child node indices.
    # Node 0 is the virtual root.
    children = [[]]
    stack = [0]
    for ch in S:
        if ch == '(':
            children.append([])
            node = len(children) - 1
            children[stack[-1]].append(node)
            stack.append(node)
        else:  # ')'
            stack.pop()

    # Compute canonical subtree IDs bottom-up (children always have larger
    # indices than their parent, so reversed index order is a valid post-order).
    id_of = {}
    canon = [0] * len(children)
    for node in range(len(children) - 1, -1, -1):
        key = tuple(sorted(canon[c] for c in children[node]))
        if key not in id_of:
            id_of[key] = len(id_of)
        canon[node] = id_of[key]

    # Factorials and inverse factorials up to N.
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    ans = 1
    for node in range(len(children)):
        ch = children[node]
        m = len(ch)
        if m <= 1:
            continue
        ways = fact[m]
        # multiplicities of each distinct child isomorphism class
        ch_sorted = sorted(canon[c] for c in ch)
        run = 1
        for i in range(1, m + 1):
            if i < m and ch_sorted[i] == ch_sorted[i - 1]:
                run += 1
            else:
                if run > 1:
                    ways = ways * inv_fact[run] % MOD
                run = 1
        ans = ans * ways % MOD

    print(ans)

main()