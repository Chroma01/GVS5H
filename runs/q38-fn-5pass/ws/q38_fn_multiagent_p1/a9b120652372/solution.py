import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    idx = 1
    out = []
    INF = 10**30

    def parse(s, ONE=49):
        cnt = 0
        first = 0
        prev = 0
        gaps = []
        append = gaps.append
        for i, ch in enumerate(s):
            if ch == ONE:
                if cnt:
                    append(i - prev)
                else:
                    first = i
                prev = i
                cnt += 1
        return cnt, first, prev, gaps

    for _ in range(t):
        # Skip N.
        idx += 1
        A = data[idx]
        idx += 1
        B = data[idx]
        idx += 1

        M, p0, plast, G = parse(A)
        K, q0, qlast, H = parse(B)

        if K > M:
            out.append("-1")
            continue

        dp = q0 - p0
        dq = qlast - plast

        # Only one final occupied square: collapse everything to that square.
        if K == 1:
            out.append(str(max(dp, -dq)))
            continue

        D = (plast - p0) - (qlast - q0)
        if D < 0:
            out.append("-1")
            continue

        lb = max(dp, -dq)
        m = len(H)

        # If all needed gaps can be matched strictly, there are no zero-deficit
        # barriers, and the endpoint lower bound is attainable.
        i = 0
        for g in G:
            if i < m and g > H[i]:
                i += 1
                if i == m:
                    break

        if i == m:
            out.append(str(lb))
            continue

        ans = INF

        # Exact matched gaps are barriers. All of them must have the same
        # prefix-deficit parity p. Try both parities.
        for p in (0, 1):
            i = 0
            par = 0  # current prefix deficit parity

            for g in G:
                if i >= m:
                    break
                h = H[i]

                if g < h:
                    # This gap cannot match the current needed gap; it must be
                    # reduced to zero.
                    par ^= (g & 1)
                elif g > h:
                    # Match strictly.
                    par ^= ((g - h) & 1)
                    i += 1
                else:
                    # Exact match is allowed only at the chosen parity.
                    if par == p:
                        i += 1
                    else:
                        par ^= (g & 1)

            if i == m:
                # Minimal endpoint-operation counts forced by parity.
                l = p
                r = (D - p) % 2

                if l + r <= D:
                    c = (D - l - r) // 2
                    s = dp - c - r
                    cost = c + l + r + abs(s)

                    if cost < ans:
                        ans = cost
                        if ans == lb:
                            break

        out.append(str(ans if ans != INF else -1))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()