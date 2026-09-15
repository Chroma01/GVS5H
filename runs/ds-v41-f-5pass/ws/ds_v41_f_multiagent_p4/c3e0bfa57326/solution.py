import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    S = data[1] if len(data) > 1 else ""
    MOD = 998244353

    M = N + 5
    fact = [1] * (M + 1)
    for i in range(1, M + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (M + 1)
    inv_fact[M] = pow(fact[M], MOD - 2, MOD)
    for i in range(M, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    def multinom(children):
        cnt = {}
        for c in children:
            cnt[c] = cnt.get(c, 0) + 1
        w = fact[len(children)]
        for v in cnt.values():
            w = w * inv_fact[v] % MOD
        return w

    ans = 1
    id_map = {}
    nxt = 0
    # stack of child-id lists; stack[0] is the virtual root's children
    stack = [[]]
    for ch in S:
        if ch == '(':
            stack.append([])
        else:
            children = stack.pop()
            ans = ans * multinom(children) % MOD
            key = tuple(sorted(children))
            cid = id_map.get(key)
            if cid is None:
                cid = nxt
                id_map[key] = cid
                nxt += 1
            stack[-1].append(cid)
    # virtual root
    ans = ans * multinom(stack[0]) % MOD
    print(ans % MOD)

main()