import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    M = int(data[pos]); pos += 1
    L = [0] * (M + 1)
    R = [0] * (M + 1)
    for i in range(1, M + 1):
        L[i] = int(data[pos]); R[i] = int(data[pos + 1]); pos += 2

    ops = [0] * (M + 1)

    def output(K):
        sys.stdout.write(str(K) + "\n")
        sys.stdout.write(" ".join(str(ops[i]) for i in range(1, M + 1)) + "\n")

    # K = 1: some operation is exactly [1, N], use op1 on it
    for i in range(1, M + 1):
        if L[i] == 1 and R[i] == N:
            ops[i] = 1
            output(1)
            return

    # K = 2, pattern (1,1): op1 on i (Li=1) + op1 on j (Rj=N), need Ri >= Lj - 1
    i1 = -1; bestR = -1
    j1 = -1; bestL = N + 2
    for i in range(1, M + 1):
        if L[i] == 1 and R[i] > bestR:
            bestR = R[i]; i1 = i
        if R[i] == N and L[i] < bestL:
            bestL = L[i]; j1 = i
    if i1 != -1 and j1 != -1 and bestR >= bestL - 1:
        ops[i1] = 1; ops[j1] = 1
        output(2)
        return

    # K = 2, pattern (1,2): op1 on container i + op2 on contained j
    # need i != j with Li <= Lj and Ri >= Rj
    order = sorted(range(1, M + 1), key=lambda i: (L[i], -R[i]))
    maxR = -1; argmax = -1
    for i in order:
        if maxR >= R[i]:
            ops[argmax] = 1; ops[i] = 2
            output(2)
            return
        if R[i] > maxR:
            maxR = R[i]; argmax = i

    # K = 2, pattern (2,2): op2 on i + op2 on j with disjoint intervals
    i2 = 1; j2 = 1
    for i in range(2, M + 1):
        if R[i] < R[i2]: i2 = i
        if L[i] > L[j2]: j2 = i
    if R[i2] < L[j2]:
        ops[i2] = 2; ops[j2] = 2
        output(2)
        return

    # K = 3: op2 on min-L interval, op2 on max-L interval, op1 on any third
    if M >= 3:
        I1 = 1; I2 = 1
        for i in range(2, M + 1):
            if L[i] < L[I1]: I1 = i
            if L[i] > L[I2]: I2 = i
        I3 = 1
        while I3 == I1 or I3 == I2:
            I3 += 1
        ops[I1] = 2; ops[I2] = 2; ops[I3] = 1
        output(3)
        return

    sys.stdout.write("-1\n")

main()