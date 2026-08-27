import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    L = [0] * M
    R = [0] * M
    for i in range(M):
        L[i] = int(next(it))
        R[i] = int(next(it))

    ans = [0] * M

    # K = 1: some interval is [1, N], use op 1 on it.
    for i in range(M):
        if L[i] == 1 and R[i] == N:
            ans[i] = 1
            sys.stdout.write("1\n" + " ".join(map(str, ans)) + "\n")
            return

    # K = 2, case (1,1): S_a with L_a=1 (max R_a), S_b with R_b=N (min L_b),
    # need R_a >= L_b - 1. a == b would imply a full interval (handled above).
    a = -1
    bestR = -1
    for i in range(M):
        if L[i] == 1 and R[i] > bestR:
            bestR = R[i]
            a = i
    b = -1
    bestL = N + 1
    for i in range(M):
        if R[i] == N and L[i] < bestL:
            bestL = L[i]
            b = i
    if a != -1 and b != -1 and a != b and R[a] >= L[b] - 1:
        ans[a] = 1
        ans[b] = 1
        sys.stdout.write("2\n" + " ".join(map(str, ans)) + "\n")
        return

    # K = 2, case (2,2): T_a ∪ T_b = [1,N] iff S_a ∩ S_b = empty.
    # Take min-R index and max-L index; need R_a < L_b (distinctness automatic).
    a = min(range(M), key=lambda i: R[i])
    b = max(range(M), key=lambda i: L[i])
    if R[a] < L[b]:
        ans[a] = 2
        ans[b] = 2
        sys.stdout.write("2\n" + " ".join(map(str, ans)) + "\n")
        return

    # K = 2, case (1,2): S_a ⊇ S_b with a != b.
    # Sort by L ascending, R descending; scan keeping the max R seen so far.
    order = sorted(range(M), key=lambda i: (L[i], -R[i]))
    maxR = -1
    argmaxR = -1
    for i in order:
        if R[i] <= maxR:
            # S_i is contained in S_argmaxR (distinct index since it came earlier)
            ans[argmaxR] = 1
            ans[i] = 2
            sys.stdout.write("2\n" + " ".join(map(str, ans)) + "\n")
            return
        else:
            maxR = R[i]
            argmaxR = i

    sys.stdout.write("-1\n")

main()