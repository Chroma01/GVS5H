import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    off_a = 1
    off_b = 1 + n
    off_c = 1 + 2 * n

    D = []  # A=1, B=0
    U = []  # A=0, B=1
    S = []  # A=1, B=1
    W0 = 0  # initial weighted sum

    for i in range(n):
        a = data[off_a + i]
        b = data[off_b + i]
        c = data[off_c + i]

        if a == 1:
            W0 += c

        if a == 1 and b == 0:
            D.append(c)
        elif a == 0 and b == 1:
            U.append(c)
        elif a == 1 and b == 1:
            S.append(c)

    del data

    D.sort()
    U.sort()
    S.sort(reverse=True)

    q = len(D)
    p = len(U)
    sumD = sum(D)

    prefD = [0] * (q + 1)
    for i, d in enumerate(D, 1):
        prefD[i] = prefD[i - 1] + d

    prefU = [0] * (p + 1)
    for i, u in enumerate(U, 1):
        prefU[i] = prefU[i - 1] + u

    # Cost for x = 0 optional 1->1 bits.
    F = 0
    for j, d in enumerate(D):
        F += d * (j + 1)

    G = 0
    for k, u in enumerate(U):
        G += u * (p - k)

    cost = (q + p) * W0 - p * sumD - F + G
    ans = cost

    if S:
        m = len(S)
        prefS = [0] * (m + 1)
        for i, c in enumerate(S, 1):
            prefS[i] = prefS[i - 1] + c

        idxD = q  # number of D values <= current c
        idxU = p  # number of U values < current c
        sumNeg = sumD  # sum of C in the current negative phase
        n0 = q         # current negative phase size
        start = 0      # number of previous S values strictly greater than current c
        prev = None

        for i, c in enumerate(S):
            if i == 0 or c != prev:
                start = i

            while idxD > 0 and D[idxD - 1] > c:
                idxD -= 1
            while idxU > 0 and U[idxU - 1] >= c:
                idxU -= 1

            cntN_gt = (q - idxD) + start
            sumN_gt = (sumD - prefD[idxD]) + prefS[start]
            cntP_lt = idxU
            sumP_lt = prefU[idxU]

            delta = (
                2 * W0
                - sumNeg
                + c * (-n0 - 1 + cntN_gt - cntP_lt)
                + sumP_lt
                - sumN_gt
            )

            cost += delta
            if cost < ans:
                ans = cost

            sumNeg += c
            n0 += 1
            prev = c

    print(ans)

if __name__ == "__main__":
    main()