import sys

def solve():
    data = sys.stdin.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    A = int(data[idx]); idx += 1
    B = int(data[idx]); idx += 1
    bad = []
    for _ in range(M):
        L = int(data[idx]); idx += 1
        R = int(data[idx]); idx += 1
        bad.append((L, R))

    # Special case: fixed step length d = A = B.
    if A == B:
        d = A
        if (N - 1) % d != 0:
            print("No")
            return
        for (L, R) in bad:
            # smallest position >= L congruent to 1 (mod d): 1 + ceil((L-1)/d)*d
            t = -(-(L - 1) // d)
            if 1 + t * d <= R:
                print("No")
                return
        print("Yes")
        return

    # A < B case: interval propagation.
    def merge(ivs):
        ivs = sorted(ivs)
        res = []
        for a, b in ivs:
            if res and a <= res[-1][1] + 1:
                if b > res[-1][1]:
                    res[-1][1] = b
            else:
                res.append([a, b])
        return res

    def expand_closure(seeds, lo, hi):
        # Least fixpoint of reachable positions inside safe zone [lo, hi],
        # given reachable seed positions (some may lie < lo).
        init = []
        for a, b in seeds:
            ca, cb = max(a, lo), min(b, hi)
            if ca <= cb:
                init.append((ca, cb))
            ta, tb = max(a + A, lo), min(b + B, hi)
            if ta <= tb:
                init.append((ta, tb))
        if not init:
            return []
        cur = merge(init)
        for _ in range(45):
            # full-extension rule: an interval of length >= A self-extends
            # contiguously (a+A <= b+1), so everything up to hi is reachable.
            for k in range(len(cur)):
                a, b = cur[k]
                if b - a + 1 >= A:
                    return cur[:k] + [[a, hi]]
            new = [tuple(x) for x in cur]
            for a, b in cur:
                ta, tb = max(a + A, lo), min(b + B, hi)
                if ta <= tb:
                    new.append((ta, tb))
            new = merge(new)
            if new == cur:
                break
            cur = new
        return cur

    S = [[1, 1]]          # reachable positions within trailing window
    cur_lo = 1            # start of current safe zone
    for (L, R) in bad:
        hi = L - 1        # end of current safe zone
        res = expand_closure(S, cur_lo, hi)
        S = merge([tuple(x) for x in S] + [tuple(x) for x in res])
        # Move to next zone; keep only sources that can jump into it
        # (a jump has length at most B, so sources >= next_lo - B).
        nxt_lo = R + 1
        low_bound = nxt_lo - B
        newS = []
        for a, b in S:
            if b >= low_bound:
                newS.append([max(a, low_bound), b])
        S = newS
        if not S:
            print("No")
            return
        cur_lo = nxt_lo

    res = expand_closure(S, cur_lo, N)
    S = merge([tuple(x) for x in S] + [tuple(x) for x in res])
    for a, b in S:
        if a <= N <= b:
            print("Yes")
            return
    print("No")

solve()