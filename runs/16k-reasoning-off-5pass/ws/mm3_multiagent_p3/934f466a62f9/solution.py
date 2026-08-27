import sys
from collections import deque
import threading

def solve():
    input_data = sys.stdin.read().split()
    it = iter(input_data)
    T = int(next(it))
    out_lines = []
    for _ in range(T):
        N = int(next(it))
        K = int(next(it))
        X = [0]*N
        Y = [0]*N
        Z = [0]*N
        for i in range(N):
            X[i] = int(next(it))
            Y[i] = int(next(it))
            Z[i] = int(next(it))
        # Pre-sort indices by each component in descending order
        idx_X = sorted(range(N), key=lambda i: -X[i])
        idx_Y = sorted(range(N), key=lambda i: -Y[i])
        idx_Z = sorted(range(N), key=lambda i: -Z[i])

        def feasible(M):
            if M <= 0:
                return True
            used = [False]*N
            count = 0
            for _ in range(K):
                best_pair = None
                for comp in range(3):
                    if comp == 0:
                        order = idx_X
                        vals = X
                    elif comp == 1:
                        order = idx_Y
                        vals = Y
                    else:
                        order = idx_Z
                        vals = Z
                    for i in order:
                        if not used[i]:
                            for j in order:
                                if not used[j] and j != i and vals[i] + vals[j] >= M:
                                    best_pair = (i, j)
                                    break
                            if best_pair is not None:
                                break
                    if best_pair is not None:
                        break
                if best_pair is not None:
                    i, j = best_pair
                    used[i] = used[j] = True
                    count += 1
                else:
                    break
            return count >= K

        lo = -1
        hi = 2_000_000_001
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid
        out_lines.append(str(lo))
    sys.stdout.write("\n".join(out_lines))

threading.Thread(target=solve).start()