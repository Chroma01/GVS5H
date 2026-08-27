import sys
from collections import Counter

def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    S = data[1]
    P = 998244353

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % P
    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], P - 2, P)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % P

    id_of = {}

    def finalize(children):
        # children: list of (class_id, ans)
        k = len(children)
        prod = 1
        ids = []
        for cid, a in children:
            ids.append(cid)
            prod = prod * a % P
        key = tuple(sorted(ids))
        nid = id_of.get(key)
        if nid is None:
            nid = len(id_of)
            id_of[key] = nid
        res = prod * fact[k] % P
        for m in Counter(ids).values():
            res = res * invfact[m] % P
        return nid, res

    stack = [[]]  # virtual root frame
    for ch in S:
        if ch == '(':
            stack.append([])
        else:
            children = stack.pop()
            nid, res = finalize(children)
            stack[-1].append((nid, res))

    _, ans = finalize(stack[0])
    print(ans)

main()