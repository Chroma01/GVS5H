import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]

    def cross1(S, T):
        # sum over (s,t) in S x T of odd_part(s + t + 1)
        ans = 0
        while S and T:
            if len(S) == 1 and len(T) == 1:
                v = S[0] + T[0] + 1
                ans += v // (v & -v)
                break
            so_l = [x for x in S if x & 1]
            to_l = [x for x in T if x & 1]
            sso = sum(so_l)
            sto = sum(to_l)
            nso = len(so_l)
            nto = len(to_l)
            nse = len(S) - nso
            nte = len(T) - nto
            sse = sum(S) - sso
            ste = sum(T) - sto
            # s even, t even -> s+t+1 odd: direct
            ans += sse * nte + ste * nse + nse * nte
            # s odd, t odd -> s+t+1 odd: direct
            ans += sso * nto + sto * nso + nso * nto
            # mixed pairs are even, halve and recurse with offset 1:
            # (odd+even+1)/2 = (odd>>1) + (even>>1) + 1
            c1s = [x >> 1 for x in so_l]
            c1t = [x >> 1 for x in to_l]   # wait: t odd pairs with s even
            # child A: (SO>>1, TE>>1); child B: (SE>>1, TO>>1)
            cA_s = c1s
            cA_t = [x >> 1 for x in T if not x & 1]
            cB_s = [x >> 1 for x in S if not x & 1]
            cB_t = [x >> 1 for x in to_l]
            sizeA = len(cA_s) + len(cA_t)
            sizeB = len(cB_s) + len(cB_t)
            if sizeA <= sizeB:
                if cA_s and cA_t:
                    ans += cross1(cA_s, cA_t)
                S, T = cB_s, cB_t
            else:
                if cB_s and cB_t:
                    ans += cross1(cB_s, cB_t)
                S, T = cA_s, cA_t
        return ans

    def f1(S):
        # sum over i<=j of odd_part(s_i + s_j + 1), s_i >= 0
        if not S:
            return 0
        if len(S) == 1:
            return 2 * S[0] + 1
        odds = [x for x in S if x & 1]
        so = sum(odds)
        no = len(odds)
        ne = len(S) - no
        se = sum(S) - so
        # same-parity pairs give odd sums -> direct
        ans = (ne + 1) * se + ne * (ne + 1) // 2
        ans += (no + 1) * so + no * (no + 1) // 2
        if no and ne:
            ans += cross1([x >> 1 for x in S if not x & 1],
                          [x >> 1 for x in odds])
        return ans

    # F0: sum over i<=j of odd_part(s_i + s_j), s_i >= 1, iterative halving
    ans = 0
    S = A
    while len(S) > 1:
        odds = [x for x in S if x & 1]
        so = sum(odds)
        no = len(odds)
        ne = len(S) - no
        if no and ne:
            se = sum(S) - so
            ans += ne * so + no * se
        if no:
            ans += f1([x >> 1 for x in odds])
        S = [x >> 1 for x in S if not x & 1]
    if len(S) == 1:
        x = S[0]
        ans += x // (x & -x)
    print(ans)

main()