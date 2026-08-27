import sys
from collections import Counter

def main():
    data = sys.stdin.read().split()
    if not data:
        print(1)
        return
    n = int(data[0])
    s = data[1] if len(data) > 1 else ''
    s = s.strip()
    MOD = 998244353

    m = max(len(s), n, 1) + 2
    fact = [1] * (m + 1)
    for i in range(1, m + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (m + 1)
    inv_fact[m] = pow(fact[m], MOD - 2, MOD)
    for i in range(m, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    memo = {}
    ans = 1
    stack = [[]]  # virtual root's children list
    for c in s:
        if c == '(':
            stack.append([])
        elif c == ')':
            ch = stack.pop()
            key = tuple(sorted(ch))
            idx = memo.get(key)
            if idx is None:
                idx = len(memo)
                memo[key] = idx
            f = fact[len(ch)]
            if ch:
                for v in Counter(ch).values():
                    if v > 1:
                        f = f * inv_fact[v] % MOD
            ans = ans * f % MOD
            if not stack:
                stack = [[]]
            stack[-1].append(idx)
        else:
            continue

    top = stack[0] if stack else []
    f = fact[len(top)]
    if top:
        for v in Counter(top).values():
            if v > 1:
                f = f * inv_fact[v] % MOD
    ans = ans * f % MOD

    print(ans % MOD)


main()