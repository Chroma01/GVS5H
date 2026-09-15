import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a_start = 1
    b_start = 1 + n
    c_start = 1 + 2 * n

    # P: must flip 1 -> 0
    # Q: must flip 0 -> 1
    # R: initially and finally 1; may optionally flip 1 -> 0 -> 1
    P = []
    Q = []
    R = []
    S0 = 0  # initial weighted sum of A

    for i in range(n):
        a = data[a_start + i]
        b = data[b_start + i]
        c = data[c_start + i]

        if a == 1:
            S0 += c
            if b == 0:
                P.append(c)
            else:
                R.append(c)
        else:
            if b == 1:
                Q.append(c)

    P.sort()
    Q.sort()
    R.sort(reverse=True)

    p0 = len(P)
    q0 = len(Q)

    # For off-list X sorted ascending, F(X) = sum w * rank.
    # For on-list Y sorted ascending, G(Y) = sum w * (q - rank + 1).
    prefP = [0] * (p0 + 1)
    F = 0
    for i, w in enumerate(P):
        prefP[i + 1] = prefP[i] + w
        F += w * (i + 1)

    prefQ = [0] * (q0 + 1)
    G = 0
    for i, w in enumerate(Q):
        prefQ[i + 1] = prefQ[i] + w
        G += w * (q0 - i)

    sumX = prefP[p0]
    p = p0
    q = q0

    # Cost with no optional R pairs.
    ans = (p + q) * S0 - q * sumX - F + G

    # Pointers for strict counts/sums of P and Q smaller than current R weight.
    idxP = p0
    idxQ = q0

    # Add optional R pairs in decreasing weight order.
    for w in R:
        # Insert w into off-list X.
        while idxP > 0 and P[idxP - 1] >= w:
            idxP -= 1
        less_cntP = idxP
        less_sumP = prefP[less_cntP]

        # Existing elements >= w increase their F-coefficient by 1.
        F += sumX - less_sumP + w * (less_cntP + 1)
        sumX += w
        p += 1

        # Insert w into on-list Y.
        while idxQ > 0 and Q[idxQ - 1] >= w:
            idxQ -= 1
        less_cntQ = idxQ
        less_sumQ = prefQ[less_cntQ]

        # Existing elements < w increase their G-coefficient by 1.
        G += less_sumQ + w * (q - less_cntQ + 1)
        q += 1

        total = (p + q) * S0 - q * sumX - F + G
        if total < ans:
            ans = total

    print(ans)

if __name__ == "__main__":
    solve()