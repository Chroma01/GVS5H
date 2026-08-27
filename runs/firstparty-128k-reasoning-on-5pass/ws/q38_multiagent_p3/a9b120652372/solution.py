import sys

ONE = 49


def build_gaps(s):
    gaps = []
    append = gaps.append
    prev = -1
    for i, ch in enumerate(s, 1):
        if ch == ONE:
            if prev != -1:
                append(i - prev)
            prev = i
    return gaps


def check_p(s, p, h, need):
    r = 0
    pa = 0
    pb = 0
    prev = -1

    for i, ch in enumerate(s, 1):
        if ch == ONE:
            if prev != -1:
                dval = i - prev
                hv = h[r]

                if dval >= hv:
                    if dval > hv or (p ^ pa ^ pb) == 0:
                        r += 1
                        if r == need:
                            return True
                        pb ^= hv & 1
                        pa ^= dval & 1
                        prev = i
                        continue

                pa ^= dval & 1

            prev = i

    return False


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    idx = 1
    out = []
    INF = 10 ** 30

    for _ in range(t):
        idx += 1  # skip N
        A = data[idx]
        idx += 1
        B = data[idx]
        idx += 1

        M = A.count(b'1')
        K = B.count(b'1')

        if K > M:
            out.append("-1")
            continue

        a1 = A.find(b'1') + 1
        aM = A.rfind(b'1') + 1
        b1 = B.find(b'1') + 1
        bK = B.rfind(b'1') + 1

        spanA = aM - a1
        spanB = bK - b1

        if spanA < spanB:
            out.append("-1")
            continue

        if M == 1:
            out.append(str(abs(b1 - a1)))
            continue

        D = spanA - spanB
        C = b1 - a1
        Dpar = D & 1

        if K == 1:
            ans = INF
            for p in (0, 1):
                e1 = p
                eM = p ^ Dpar
                tspan = (D + e1 + eM) // 2
                val = tspan + abs(C - (tspan - e1))
                if val < ans:
                    ans = val
            out.append(str(ans))
            continue

        h = build_gaps(B)
        need = len(h)
        ans = INF

        for p in (0, 1):
            if check_p(A, p, h, need):
                e1 = p
                eM = p ^ Dpar
                tspan = (D + e1 + eM) // 2
                val = tspan + abs(C - (tspan - e1))
                if val < ans:
                    ans = val

        if ans == INF:
            out.append("-1")
        else:
            out.append(str(ans))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()