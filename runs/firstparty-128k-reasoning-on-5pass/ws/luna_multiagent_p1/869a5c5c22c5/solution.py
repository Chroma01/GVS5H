import sys
from collections import deque

LIMIT = 10**9
BASE = 500_000_000


def validate(ans, red_count, blue_count):
    n = red_count + blue_count
    if ans is None or len(ans) != n:
        return False

    seen = set()
    cr = cb = 0

    for i, (color, r, c) in enumerate(ans):
        if not (1 <= r <= LIMIT and 1 <= c <= LIMIT):
            return False
        if (r, c) in seen:
            return False
        seen.add((r, c))

        nr, nc = ans[(i + 1) % n][1], ans[(i + 1) % n][2]
        dr = abs(r - nr)
        dc = abs(c - nc)

        if color == "R":
            cr += 1
            if dr + dc != 1:
                return False
        elif color == "B":
            cb += 1
            if dr != 1 or dc != 1:
                return False
        else:
            return False

    return cr == red_count and cb == blue_count


def make_pure_red(n):
    if n == 2:
        return [
            ("R", BASE, BASE),
            ("R", BASE, BASE + 1),
        ]

    a = 1
    b = n // 2 - 1
    x = BASE
    y = BASE
    ans = []

    for i in range(a):
        ans.append(("R", x + i, y))
    for i in range(b):
        ans.append(("R", x + a, y + i))
    for i in range(a):
        ans.append(("R", x + a - i, y + b))
    for i in range(b):
        ans.append(("R", x, y + b - i))

    return ans


def make_pure_blue(n):
    if n == 2:
        return [
            ("B", BASE, BASE),
            ("B", BASE + 1, BASE + 1),
        ]

    a = 1
    b = n // 2 - 1
    u = 2 * BASE
    v = 0
    points = []

    for _ in range(a):
        points.append((u, v))
        u += 2
    for _ in range(b):
        points.append((u, v))
        v += 2
    for _ in range(a):
        points.append((u, v))
        u -= 2
    for _ in range(b):
        points.append((u, v))
        v -= 2

    return [
        ("B", (u0 + v0) // 2, (u0 - v0) // 2)
        for u0, v0 in points
    ]


def make_mixed(red_count, blue_count):
    nodes = []

    def add_node(r, c, color):
        idx = len(nodes)
        nodes.append([r, c, -1, color])
        return idx

    if blue_count & 1:
        base_coords = [(0, 0), (1, 0), (1, 1)]
        base_colors = ["R", "R", "B"]
    else:
        base_coords = [(0, 0), (1, 0), (2, 1), (1, 1)]
        base_colors = ["R", "B", "R", "B"]

    base_ids = []
    for (r, c), color in zip(base_coords, base_colors):
        base_ids.append(add_node(BASE + r, BASE + c, color))

    for i, idx in enumerate(base_ids):
        nodes[idx][2] = base_ids[(i + 1) % len(base_ids)]

    occupied = {(nodes[i][0], nodes[i][1]) for i in base_ids}
    queues = {"R": deque(), "B": deque()}

    for idx in base_ids:
        queues[nodes[idx][3]].append(idx)

    def expand(idx):
        color = nodes[idx][3]
        nxt = nodes[idx][2]
        r1, c1 = nodes[idx][0], nodes[idx][1]
        r2, c2 = nodes[nxt][0], nodes[nxt][1]

        candidates = []

        if color == "R":
            if r1 == r2:
                for shift in (-1, 1):
                    candidates.append(
                        ((r1 + shift, c1), (r2 + shift, c2))
                    )
            else:
                for shift in (-1, 1):
                    candidates.append(
                        ((r1, c1 + shift), (r2, c2 + shift))
                    )
        else:
            dr = r2 - r1
            dc = c2 - c1
            for sign in (1, -1):
                off_r = sign * dr
                off_c = -sign * dc
                candidates.append(
                    ((r1 + off_r, c1 + off_c),
                     (r2 + off_r, c2 + off_c))
                )

        for (wr, wc), (zr, zc) in candidates:
            if not (1 <= wr <= LIMIT and 1 <= wc <= LIMIT):
                continue
            if not (1 <= zr <= LIMIT and 1 <= zc <= LIMIT):
                continue
            if (wr, wc) in occupied or (zr, zc) in occupied:
                continue

            w = add_node(wr, wc, color)
            z = add_node(zr, zc, color)

            nodes[idx][2] = w
            nodes[w][2] = z
            nodes[z][2] = nxt

            occupied.add((wr, wc))
            occupied.add((zr, zc))
            queues[color].append(w)
            queues[color].append(z)
            return True

        return False

    def add_edges(color, amount):
        q = queues[color]
        for _ in range(amount):
            while q:
                idx = q.popleft()
                if expand(idx):
                    break
            else:
                return False
        return True

    base_blue = 1 if (blue_count & 1) else 2

    if not add_edges("R", (red_count - 2) // 2):
        return None
    if not add_edges("B", (blue_count - base_blue) // 2):
        return None

    ans = []
    cur = base_ids[0]
    for _ in range(red_count + blue_count):
        r, c, nxt, color = nodes[cur]
        ans.append((color, r, c))
        cur = nxt

    if cur != base_ids[0]:
        return None
    return ans


def solve_case(red_count, blue_count):
    if red_count & 1:
        return None

    if red_count == 0:
        if blue_count >= 2 and blue_count % 2 == 0:
            return make_pure_blue(blue_count)
        return None

    if blue_count == 0:
        if red_count >= 2:
            return make_pure_red(red_count)
        return None

    if red_count < 2:
        return None

    return make_mixed(red_count, blue_count)


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    pos = 1
    output = []

    for _ in range(t):
        red_count = data[pos]
        blue_count = data[pos + 1]
        pos += 2

        ans = solve_case(red_count, blue_count)

        if not validate(ans, red_count, blue_count):
            output.append("No")
        else:
            output.append("Yes")
            output.extend(
                f"{color} {r} {c}"
                for color, r, c in ans
            )

    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    main()