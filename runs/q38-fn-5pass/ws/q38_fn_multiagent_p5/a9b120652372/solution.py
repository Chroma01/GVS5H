import sys


def can(p, a, b, k, m):
    ia = 0
    last = k - 1
    aa = a
    bb = b

    for j in range(m - 1):
        g = bb[j + 1] - bb[j]
        bj = bb[j]

        while ia < last:
            d = aa[ia + 1] - aa[ia]
            if d >= g:
                if d > g or ((bj - aa[ia]) & 1) == p:
                    ia += 1
                    break
            ia += 1
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
    can_func = can

    for _ in range(t):
        idx += 1  # N is not needed explicitly
        A = data[idx]
        idx += 1
        B = data[idx]
        idx += 1

        a = [i for i, c in enumerate(A) if c == 49]  # '1'
        b = [i for i, c in enumerate(B) if c == 49]

        k = len(a)
        m = len(b)

        if k < m:
            out.append("-1")
            continue

        if b[-1] - b[0] > a[-1] - a[0]:
            out.append("-1")
            continue

        base = b[0] - a[0]
        v = a[-1] - b[-1]
        if v > base:
            base = v
        if base < 0:
            base = 0

        if m == 1:
            out.append(str(base))
            continue

        p0 = base & 1
        if can_func(p0, a, b, k, m):
            out.append(str(base))
        elif can_func(p0 ^ 1, a, b, k, m):
            out.append(str(base + 1))
        else:
            out.append("-1")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()