import sys
from collections import Counter

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    B = [int(next(it)) for _ in range(N)]

    fixed_A = [x for x in A if x != -1]
    fixed_B = [x for x in B if x != -1]
    a_fixed = len(fixed_A)
    b_fixed = len(fixed_B)

    # Required number of fixed-fixed pairs sharing the same sum S.
    # (Derivation: need M >= a_fixed - b_wild and M >= b_fixed - a_wild,
    #  and both right-hand sides equal a_fixed + b_fixed - N.)
    K = a_fixed + b_fixed - N
    if K <= 0:
        # Enough wildcards to pair every fixed element with a wildcard.
        print("Yes")
        return

    # K > 0 implies both sides have at least one fixed element.
    T = max(max(fixed_A), max(fixed_B))

    ca = Counter(fixed_A)
    cb = Counter(fixed_B)

    # f(S) = sum_v min(cntA[v], cntB[S - v]).
    # Each distinct value pair (a, b) contributes min(ca[a], cb[b]) to f(a+b).
    # Accumulate all contributions in a single O(D_A * D_B) pass.
    f = {}
    f_get = f.get
    for a, acnt in ca.items():
        for b, bcnt in cb.items():
            s = a + b
            if s < T:
                continue
            v = acnt if acnt < bcnt else bcnt
            nv = f_get(s, 0) + v
            if nv >= K:
                # Contributions are non-negative, so final f(s) >= K.
                print("Yes")
                return
            f[s] = nv

    print("No")

main()