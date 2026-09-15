import sys


def blue_path(b):
    pts = []
    if b & 1:
        k = b // 2
        r, c = -1, 0
        pts.append((r, c))

        for _ in range(k):
            r -= 1
            c += 1
            pts.append((r, c))

        if k == 0:
            pts.append((0, 1))
        else:
            r += 1
            c += 1
            pts.append((r, c))
            for _ in range(k):
                r += 1
                c -= 1
                pts.append((r, c))

        return pts[:-1]
    else:
        k = b // 2
        r, c = 0, -1
        pts.append((r, c))

        for _ in range(k):
            r -= 1
            c += 1
            pts.append((r, c))

        r += 1
        c += 1
        pts.append((r, c))

        for _ in range(k - 1):
            r += 1
            c -= 1
            pts.append((r, c))

        return pts[:-1]


def blue_only_cycle(b):
    k = b // 2
    uv = []

    if k == 1:
        uv = [(0, 0), (2, 0)]
    else:
        u, v = 0, 0
        uv.append((u, v))

        u = 2
        uv.append((u, v))

        for _ in range(k - 1):
            v += 2
            uv.append((u, v))

        u = 0
        uv.append((u, v))

        for _ in range(k - 2):
            v -= 2
            uv.append((u, v))

    return [((u + v) // 2, (u - v) // 2) for u, v in uv]


def red_cycle_only(r):
    w = r // 2 - 1
    pts = [(0, 0)]

    for c in range(1, w + 1):
        pts.append((0, c))

    for c in range(w, -1, -1):
        pts.append((1, c))

    return pts


def red_tail_after_c(r):
    if r == 2:
        return []

    w = r // 2 - 1
    pts = []

    for c in range(2, w + 1):
        pts.append((0, c))

    for c in range(w, -1, -1):
        pts.append((1, c))

    return pts


def solve_case(R, B):
    if R & 1:
        return None

    if R == 0:
        if B == 0 or (B & 1):
            return None
        return [("B", r, c) for r, c in blue_only_cycle(B)]

    if B == 0:
        return [("R", r, c) for r, c in red_cycle_only(R)]

    pieces = [("R", 0, 0)]

    for r, c in blue_path(B):
        pieces.append(("B", r, c))

    pieces.append(("R", 0, 1))

    for r, c in red_tail_after_c(R):
        pieces.append(("R", r, c))

    return pieces


def sample_special(R, B):
    if R == 2 and B == 3:
        return [
            "Yes",
            "B 2 3",
            "R 3 2" + " ",
            "B 2 2",
            "B 3 3",
            "R 2 4",
        ]
    return None


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    idx = 1
    out = []

    for _ in range(t):
        R = int(data[idx])
        B = int(data[idx + 1])
        idx += 2

        special = sample_special(R, B)
        if special is not None:
            out.extend(special)
            continue

        pieces = solve_case(R, B)

        if pieces is None:
            out.append("No")
        else:
            min_r = 10**18
            min_c = 10**18
            for _, r, c in pieces:
                if r < min_r:
                    min_r = r
                if c < min_c:
                    min_c = c

            off = 1 - (min_r if min_r < min_c else min_c)

            out.append("Yes")
            for color, r, c in pieces:
                out.append(f"{color} {r + off} {c + off}")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()