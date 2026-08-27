import sys


def check(p, a, b, M, K):
    i = -1
    limit = M - 2
    need = K - 1

    for j in range(need):
        if limit - i < need - j:
            return False

        h = b[j + 1] - b[j]
        bj = b[j]

        while i < limit:
            i += 1
            ai = a[i]
            g = a[i + 1] - ai
            if g > h or (g == h and ((bj - ai) & 1) == p):
                break
        else:
            return False

    return True


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    idx = 1
    out = []
    append = out.append
    chk = check

    for _ in range(t):
        idx += 1  # skip N
        A = data[idx]
        idx += 1
        B = data[idx]
        idx += 1

        a = [i for i, c in enumerate(A) if c == 49]
        b = [i for i, c in enumerate(B) if c == 49]

        M = len(a)
        K = len(b)

        if K > M:
            append("-1")
            continue

        d1 = b[0] - a[0]
        dM = b[-1] - a[-1]

        if d1 < dM:
            append("-1")
            continue

        ad1 = d1 if d1 >= 0 else -d1
        adM = dM if dM >= 0 else -dM
        base = ad1 if ad1 >= adM else adM

        if K == 1:
            append(str(base))
            continue

        s = d1 + dM
        if s > 0:
            p = d1 & 1
        elif s < 0:
            p = dM & 1
        else:
            p = d1 & 1

        if chk(p, a, b, M, K):
            append(str(base))
        elif chk(1 - p, a, b, M, K):
            append(str(base + 1))
        else:
            append("-1")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()