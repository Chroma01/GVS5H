import sys

def solve():
    readline = sys.stdin.buffer.readline
    T = int(readline())
    out = []
    append = out.append

    for _ in range(T):
        N = int(readline())
        A = readline().strip()
        B = readline().strip()

        # 0-indexed positions of '1'
        a = [i for i, c in enumerate(A) if c == 49]
        b = [i for i, c in enumerate(B) if c == 49]

        M = len(a)
        K = len(b)

        if M < K:
            append("-1")
            continue

        if K == 1:
            ans = b[0] - a[0]
            d = a[-1] - b[0]
            if d > ans:
                ans = d
            append(str(ans))
            continue

        S = (a[-1] - a[0]) - (b[-1] - b[0])
        if S < 0:
            append("-1")
            continue

        C = b[0] - a[0]
        a0 = a[0]
        b0 = b[0]

        best = 10**18
        mm1 = M - 1
        kk1 = K - 1

        for l in (0, 1):
            j = 0
            L = b[1] - b[0]
            req = a0 & 1  # (a0 + b[0] - b0) & 1

            for t in range(mm1):
                g = a[t + 1] - a[t]
                if g >= L:
                    if g > L or ((a[t] & 1) == (req ^ l)):
                        j += 1
                        if j == kk1:
                            break
                        L = b[j + 1] - b[j]
                        req = (a0 + b[j] - b0) & 1

            if j == kk1:
                r = l ^ (S & 1)
                cand = C + l
                alt = S + r - C
                if alt > cand:
                    cand = alt
                if cand < best:
                    best = cand
                    if best == 0:
                        break

        if best == 10**18:
            append("-1")
        else:
            append(str(best))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()