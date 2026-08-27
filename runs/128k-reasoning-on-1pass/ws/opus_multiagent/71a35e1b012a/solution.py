import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    L = list(map(int, data[2::2]))
    R = list(map(int, data[3::2]))
    # safety: ensure lengths
    if len(L) > m:
        L = L[:m]
    if len(R) > m:
        R = R[:m]

    out = sys.stdout.write

    def emit(cost, assignments):
        ops = ['0'] * m
        for idx, o in assignments:
            ops[idx] = o
        out(str(cost) + "\n" + " ".join(ops) + "\n")

    # (1) cost 1
    for i in range(m):
        if L[i] == 1 and R[i] == n:
            emit(1, [(i, '1')])
            return

    # (2) two op1: [1,a] and [b,n] with a+1 >= b
    best_i = -1  # argmax R among L==1
    best_j = -1  # argmin L among R==n
    for i in range(m):
        if L[i] == 1:
            if best_i == -1 or R[i] > R[best_i]:
                best_i = i
        if R[i] == n:
            if best_j == -1 or L[i] < L[best_j]:
                best_j = i
    if best_i != -1 and best_j != -1 and best_i != best_j:
        if R[best_i] + 1 >= L[best_j]:
            emit(2, [(best_i, '1'), (best_j, '1')])
            return

    # (3) containment: op1 on container, op2 on contained
    order = sorted(range(m), key=lambda i: (L[i], -R[i]))
    bestR = -1
    bestIdx = -1
    for idx in order:
        if bestIdx != -1 and R[idx] <= bestR:
            emit(2, [(bestIdx, '1'), (idx, '2')])
            return
        else:
            bestR = R[idx]
            bestIdx = idx

    # (4) disjoint pair: op2 on both
    a = 0  # argmin R
    b = 0  # argmax L
    for i in range(1, m):
        if R[i] < R[a]:
            a = i
        if L[i] > L[b]:
            b = i
    if a != b and L[b] > R[a]:
        emit(2, [(a, '2'), (b, '2')])
        return

    # (5) cost 3
    if m >= 3 and a != b:
        c = -1
        for i in range(m):
            if i != a and i != b:
                c = i
                break
        if c != -1:
            emit(3, [(a, '2'), (b, '2'), (c, '1')])
            return

    out("-1\n")

main()