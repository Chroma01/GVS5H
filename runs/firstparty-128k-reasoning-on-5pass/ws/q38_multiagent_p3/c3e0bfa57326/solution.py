import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    s = data[1]

    maxk = n // 2 + 1
    fact = [1] * (maxk + 1)
    for i in range(1, maxk + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (maxk + 1)
    invfact[maxk] = pow(fact[maxk], MOD - 2, MOD)
    for i in range(maxk, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    counts = []
    ids = {}

    def canon(t):
        cid = ids.get(t)
        if cid is not None:
            return cid

        cid = len(counts)
        k = len(t)
        v = fact[k]
        i = 0
        while i < k:
            j = i + 1
            while j < k and t[j] == t[i]:
                j += 1
            m = j - i
            v = v * invfact[m] % MOD
            v = v * pow(counts[t[i]], m, MOD) % MOD
            i = j

        counts.append(v)
        ids[t] = cid
        return cid

    stack = [[]]
    for ch in s:
        if ch == '(':
            stack.append([])
        else:
            children = stack.pop()
            children.sort()
            cid = canon(tuple(children))
            stack[-1].append(cid)

    stack[0].sort()
    cid = canon(tuple(stack[0]))
    print(counts[cid] % MOD)

if __name__ == "__main__":
    main()