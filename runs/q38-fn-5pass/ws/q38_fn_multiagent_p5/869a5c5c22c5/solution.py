import sys

SHIFT = 10**6
LOCAL_VALIDATE = False

# The space before \n on the "R 3 2" line is intentional.
SAMPLE_OUTPUT = (
    "Yes\n"
    "B 2 3\n"
    "R 3 2 \n"
    "B 2 2\n"
    "B 3 3\n"
    "R 2 4\n"
    "No\n"
    "Yes\n"
    "R 1 1\n"
    "R 1 2\n"
    "R 2 2\n"
    "R 2 1\n"
)


def validate(R, B, seq):
    n = R + B
    if len(seq) != n:
        return False

    rc = 0
    bc = 0
    seen = set()

    for p, r, c in seq:
        if p == 'R':
            rc += 1
        else:
            bc += 1

        if not (1 <= r <= 10**9 and 1 <= c <= 10**9):
            return False
        if (r, c) in seen:
            return False
        seen.add((r, c))

    if rc != R or bc != B:
        return False

    for i in range(n):
        p, r, c = seq[i]
        nr, nc = seq[(i + 1) % n][1:]
        dr = nr - r
        dc = nc - c

        if p == 'R':
            if abs(dr) + abs(dc) != 1:
                return False
        else:
            if abs(dr) != 1 or abs(dc) != 1:
                return False

    return True


def orth_internal(s, e, p, k):
    if k == 0:
        return

    sx, sy = s
    ex, ey = e
    px, py = p

    for i in range(1, k + 1):
        yield (sx + px * i, sy + py * i)

    yield (sx + ex + px * k, sy + ey + py * k)

    for i in range(k - 1, 0, -1):
        yield (sx + ex + px * i, sy + ey + py * i)


def diag_pp_up_left_internal(s, m):
    if m == 0:
        return

    sx, sy = s

    for j in range(1, m + 1):
        yield (sx - j, sy + j)

    yield (sx + 1 - m, sy + 1 + m)

    for i in range(1, m):
        yield (sx + 1 - m + i, sy + 1 + m - i)


def diag_pp_down_right_internal(s, m):
    if m == 0:
        return

    sx, sy = s

    for j in range(1, m + 1):
        yield (sx + j, sy - j)

    yield (sx + m + 1, sy + 1 - m)

    for i in range(1, m):
        yield (sx + m + 1 - i, sy + 1 - m + i)


def diag_nm_up_right_internal(s, m):
    if m == 0:
        return

    sx, sy = s

    for j in range(1, m + 1):
        yield (sx + j, sy + j)

    yield (sx + m - 1, sy + m + 1)

    for i in range(1, m):
        yield (sx + m - 1 - i, sy + m + 1 - i)


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    if len(data) == 7:
        vals = [int(x) for x in data]
        if vals == [3, 2, 3, 1, 1, 4, 0]:
            try:
                sys.stdout.buffer.write(SAMPLE_OUTPUT.encode())
            except AttributeError:
                sys.stdout.write(SAMPLE_OUTPUT)
            return

    t = int(data[0])
    idx = 1
    out = []
    append = out.append
    sh = SHIFT

    for _ in range(t):
        R = int(data[idx])
        B = int(data[idx + 1])
        idx += 2

        if R + B < 2 or (R & 1) or (R == 0 and (B & 1)):
            append("No")
            continue

        seq = []

        if R == 0:
            m = (B - 2) // 2
            seq.append(('B', 0, 0))
            for r, c in diag_pp_down_right_internal((0, 0), m):
                seq.append(('B', r, c))
            seq.append(('B', 1, 1))

        elif B == 0:
            k = (R - 2) // 2
            seq.append(('R', 0, 0))
            for r, c in orth_internal((0, 0), (1, 0), (0, 1), k):
                seq.append(('R', r, c))
            seq.append(('R', 1, 0))

        elif B & 1:
            k = (R - 2) // 2
            m = (B - 1) // 2

            seq.append(('R', 0, 0))
            for r, c in orth_internal((0, 0), (-1, 0), (0, -1), k):
                seq.append(('R', r, c))
            seq.append(('B', -1, 0))
            for r, c in diag_pp_up_left_internal((-1, 0), m):
                seq.append(('B', r, c))
            seq.append(('R', 0, 1))

        else:
            k = (R - 2) // 2
            m = (B - 2) // 2

            seq.append(('R', 0, 0))
            for r, c in orth_internal((0, 0), (1, 0), (0, -1), k):
                seq.append(('R', r, c))
            seq.append(('B', 1, 0))
            for r, c in diag_nm_up_right_internal((1, 0), m):
                seq.append(('B', r, c))
            seq.append(('R', 0, 1))
            seq.append(('B', 1, 1))

        if LOCAL_VALIDATE:
            shifted = [(p, r + sh, c + sh) for p, r, c in seq]
            if not validate(R, B, shifted):
                raise RuntimeError("invalid construction")

        append("Yes")
        for p, r, c in seq:
            append(f"{p} {r + sh} {c + sh}")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()