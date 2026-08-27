import sys

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    T = int(next(it))
    out = []
    for _ in range(T):
        N = int(next(it))
        A = next(it).decode()
        B = next(it).decode()

        # positions of pieces (0‑based) and required positions
        P = [i for i, ch in enumerate(A) if ch == '1']
        Tpos = [i for i, ch in enumerate(B) if ch == '1']
        M, K = len(P), len(Tpos)

        # not enough pieces to cover all required squares
        if M < K:
            out.append("-1")
            continue

        # ------------------------------------------------------------
        # feasibility test: can we match K pieces to the K targets
        # within distance d, respecting the order of pieces?
        # ------------------------------------------------------------
        def feasible(d: int) -> bool:
            i = 0                 # index in P
            prev_p = None         # piece used for previous target
            prev_t = None         # previous target position
            for t in Tpos:
                lower = t - d                     # piece must be at least this far left
                if prev_p is not None:
                    # we also need the gap between pieces to be at least the gap between targets
                    lower = max(lower, prev_p + (t - prev_t))
                # skip pieces that are too far left
                while i < M and P[i] < lower:
                    i += 1
                # no piece in the allowed interval
                if i >= M or P[i] > t + d:
                    return False
                # use this piece for the current target
                prev_p = P[i]
                prev_t = t
                i += 1
            return True

        # if even with the maximal possible distance we cannot succeed → impossible
        if not feasible(N):
            out.append("-1")
            continue

        # binary search the minimal d
        lo, hi = 0, N
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1
        out.append(str(lo))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()