import sys
from collections import deque

INF = 10**30


def solve_positions(x, s):
    """
    x: sorted positions of 1s in A
    s: sorted positions of 1s in B
    Returns minimum operations, or -1.
    """
    K = len(x)
    L = len(s)

    if K < L:
        return -1
    if K == 0:
        return 0 if L == 0 else -1
    if L == 0:
        return -1

    # Total gap reduction needed.
    S = (x[-1] - x[0]) - (s[-1] - s[0])
    if S < 0:
        return -1

    # Required displacement of the leftmost piece.
    delta = s[0] - x[0]
    parity = S & 1

    # If there is only one target square, there are no target gaps to match.
    if L == 1:
        ans = INF
        for u in (0, 1):
            v = u ^ parity
            cost = delta + u
            other = S + v - delta
            if other > cost:
                cost = other
            if cost < ans:
                ans = cost
        return ans

    Lm1 = L - 1
    r0 = 0  # next target gap index for start b0 = 0
    r1 = 0  # next target gap index for start b0 = 1
    p = 0   # parity of x[j] - x[0]
    s0 = s[0]

    # Greedily match target gaps to initial gaps for both possible b0 values.
    for j in range(K - 1):
        d = x[j + 1] - x[j]

        if r0 < Lm1:
            g = s[r0 + 1] - s[r0]
            if d >= g:
                if d > g:
                    r0 += 1
                else:
                    q = (s[r0] - s0) & 1
                    if (p ^ q) == 0:
                        r0 += 1

        if r1 < Lm1:
            g = s[r1 + 1] - s[r1]
            if d >= g:
                if d > g:
                    r1 += 1
                else:
                    q = (s[r1] - s0) & 1
                    if (p ^ q) == 1:
                        r1 += 1

        p ^= (d & 1)

        if r0 == Lm1 and r1 == Lm1:
            break

    ans = INF

    if r0 == Lm1:
        # b0 = 0, b_last = parity
        v = parity
        cost = delta
        other = S + v - delta
        if other > cost:
            cost = other
        ans = cost

    if r1 == Lm1:
        # b0 = 1, b_last = 1 ^ parity
        v = 1 ^ parity
        cost = delta + 1
        other = S + v - delta
        if other > cost:
            cost = other
        if cost < ans:
            ans = cost

    return -1 if ans == INF else ans


def validate(max_n=6):
    """
    Brute-force validation on all nonempty subsets for small N.
    Run with: python3 solution.py --validate
    """
    for N in range(1, max_n + 1):
        masks = list(range(1, 1 << N))
        pos = {
            m: tuple(i for i in range(N) if (m >> i) & 1)
            for m in masks
        }

        trans = {}
        for m in masks:
            st = pos[m]
            arr = []
            for c in range(N):
                ns = sorted({
                    p + (1 if c > p else (-1 if c < p else 0))
                    for p in st
                })
                nm = 0
                for p in ns:
                    nm |= 1 << p
                arr.append(nm)
            trans[m] = arr

        for start in masks:
            dist = {start: 0}
            q = deque([start])
            while q:
                cur = q.popleft()
                nd = dist[cur] + 1
                for nxt in trans[cur]:
                    if nxt not in dist:
                        dist[nxt] = nd
                        q.append(nxt)

            for target in masks:
                if target.bit_count() <= start.bit_count():
                    expected = solve_positions(pos[start], pos[target])
                    actual = dist.get(target, -1)
                    if expected != actual:
                        print(
                            f"MISMATCH N={N} start={start} target={target} "
                            f"expected={expected} actual={actual}"
                        )
                        return False

    print("validation ok")
    return True


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        validate()
        return

    t = int(data[0])
    idx = 1
    out = []

    for _ in range(t):
        n = int(data[idx])
        idx += 1
        a = data[idx]
        idx += 1
        b = data[idx]
        idx += 1

        x = [i for i, c in enumerate(a) if c == 49]  # ord('1') == 49
        s = [i for i, c in enumerate(b) if c == 49]

        out.append(str(solve_positions(x, s)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--validate":
        validate()
    else:
        main()