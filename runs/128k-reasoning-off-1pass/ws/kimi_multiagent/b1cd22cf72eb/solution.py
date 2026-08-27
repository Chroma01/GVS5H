import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    X = int(data[idx]); idx += 1
    U = [0] * N
    D = [0] * N
    total = 0
    hi = None
    for i in range(N):
        u = int(data[idx]); idx += 1
        d = int(data[idx]); idx += 1
        U[i] = u
        D[i] = d
        s = u + d
        total += s
        if hi is None or s < hi:
            hi = s

    # For fixed H: u_i must satisfy L_i <= u_i <= min(U_i, H),
    # where L_i = max(0, H - D_i), plus |u_i - u_{i+1}| <= X.
    # Feasibility: propagate upper bounds (u_i <= u_j + X*|i-j|) via
    # forward+backward passes, then check L_i <= up_i for all i.
    def feasible(H):
        up = [0] * N
        mn = H
        for i in range(N):
            u = U[i]
            up[i] = u if u < mn else mn
        # forward pass
        prev = up[0]
        for i in range(1, N):
            v = prev + X
            if v < up[i]:
                up[i] = v
            prev = up[i]
        # backward pass
        prev = up[N - 1]
        for i in range(N - 2, -1, -1):
            v = prev + X
            if v < up[i]:
                up[i] = v
            prev = up[i]
        # check lower bounds
        for i in range(N):
            l = H - D[i]
            if l < 0:
                l = 0
            if l > up[i]:
                return False
        return True

    lo = 0
    # invariant: lo feasible, hi maybe not; find max feasible H
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1

    print(total - N * lo)

main()