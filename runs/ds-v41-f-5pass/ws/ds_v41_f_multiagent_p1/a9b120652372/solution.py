import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    ONE = 49  # ord('1')

    for _ in range(t):
        n = int(data[idx]); A = data[idx + 1]; B = data[idx + 2]
        idx += 3

        p = [i + 1 for i in range(n) if A[i] == ONE]
        b = [i + 1 for i in range(n) if B[i] == ONE]
        K = len(p); M = len(b)

        if K < M:
            out.append(-1)
            continue

        # max |D_j| = max(D_1, -D_K) ; D is non-increasing for any valid assignment
        t0 = b[0] - p[0]
        x = p[K - 1] - b[M - 1]
        if x > t0:
            t0 = x
        if t0 < 0:
            out.append(-1)
            continue

        ans = -1
        for parity in (t0 & 1, (t0 ^ 1) & 1):
            prev = -1
            ok = True
            for tt in range(M - 1):
                bg = b[tt + 1] - b[tt]
                cap = K - M + tt
                r = prev + 1
                found = -1
                while r <= cap:
                    g = p[r + 1] - p[r]
                    if g > bg:
                        found = r
                        break
                    if g == bg and ((b[tt] - p[r]) & 1) == parity:
                        found = r
                        break
                    r += 1
                if found < 0:
                    ok = False
                    break
                prev = found
            if ok:
                ans = t0 if parity == (t0 & 1) else t0 + 1
                break

        out.append(ans)

    sys.stdout.write('\n'.join(map(str, out)))


main()