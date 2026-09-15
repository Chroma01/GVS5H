import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1] if len(data) > 1 else ''
    
    maxn = N + 5
    fact = [1] * (maxn + 1)
    for i in range(1, maxn + 1):
        fact[i] = fact[i-1] * i % MOD
    invfact = [1] * (maxn + 1)
    invfact[maxn] = pow(fact[maxn], MOD - 2, MOD)
    for i in range(maxn, 0, -1):
        invfact[i-1] = invfact[i] * i % MOD

    children = [[]]
    stack = [0]
    node_count = 0
    for ch in S:
        if ch == '(':
            node_count += 1
            idx = node_count
            p = stack[-1]
            children[p].append(idx)
            children.append([])
            stack.append(idx)
        else:
            stack.pop()

    m = node_count
    type_of = [0] * (m + 1)
    type_id = {}
    val_type = {}
    next_id = 1

    for v in range(m, 0, -1):
        chs = children[v]
        k = len(chs)
        if k == 0:
            key = ()
        else:
            key = tuple(sorted(type_of[c] for c in chs))
        tid = type_id.get(key)
        if tid is None:
            tid = next_id
            next_id += 1
            type_id[key] = tid
            if k == 0:
                vv = 1
            else:
                vv = fact[k]
                cnt = 1
                prev = key[0]
                for x in key[1:]:
                    if x == prev:
                        cnt += 1
                    else:
                        vv = vv * invfact[cnt] % MOD
                        vv = vv * pow(val_type[prev], cnt, MOD) % MOD
                        prev = x
                        cnt = 1
                vv = vv * invfact[cnt] % MOD
                vv = vv * pow(val_type[prev], cnt, MOD) % MOD
            val_type[tid] = vv
        type_of[v] = tid

    chs = children[0]
    k = len(chs)
    if k == 0:
        ans = 1
    else:
        key = tuple(sorted(type_of[c] for c in chs))
        ans = fact[k]
        cnt = 1
        prev = key[0]
        for x in key[1:]:
            if x == prev:
                cnt += 1
            else:
                ans = ans * invfact[cnt] % MOD
                ans = ans * pow(val_type[prev], cnt, MOD) % MOD
                prev = x
                cnt = 1
        ans = ans * invfact[cnt] % MOD
        ans = ans * pow(val_type[prev], cnt, MOD) % MOD

    print(ans)

if __name__ == "__main__":
    main()