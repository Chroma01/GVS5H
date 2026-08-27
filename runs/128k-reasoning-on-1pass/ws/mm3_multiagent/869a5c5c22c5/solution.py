import sys

# ------------------------------------------------------------
# construction helpers
# ------------------------------------------------------------

def construct_rectangle(R):
    """R is even, R >= 2, B = 0.
       rectangle height 2, width w = R/2.
    """
    w = R // 2
    path = []
    # start
    path.append((2, 2))
    # right w-1 steps
    for i in range(1, w):
        path.append((2, 2 + i))
    # down
    path.append((3, 2 + w - 1))          # (3, w+1)
    # left w-1 steps
    for i in range(w - 2, -1, -1):
        path.append((3, 2 + i))
    return path


def construct_B1(R):
    """R even, R >= 2, B = 1.
       right w steps, down 1, left w-1 steps, up-left closing.
    """
    w = R // 2
    path = []
    path.append((2, 2))
    # right w steps
    for i in range(1, w + 1):
        path.append((2, 2 + i))
    # down 1
    path.append((3, 2 + w))
    # left w-1 steps
    for i in range(w - 1, 0, -1):
        path.append((3, 2 + i))
    return path


def construct_parallelogram(R, B0):
    """R even, B0 even, B0 = 2*h, h >= 1.
       w = R/2, h = B0/2.
    """
    w = R // 2
    h = B0 // 2
    r0, c0 = 2, 2
    path = []
    # segment A : right w steps
    for i in range(w + 1):
        path.append((r0, c0 + i))
    # segment B : down‑right h steps
    for j in range(1, h + 1):
        path.append((r0 + j, c0 + w + j))
    # segment C : left w steps
    for k in range(1, w + 1):
        path.append((r0 + h, c0 + w + h - k))
    # segment D : up‑left h steps (do not add the final start point)
    for l in range(1, h):
        path.append((r0 + h - l, c0 + h - l))
    return path


def apply_detour(path):
    """Replace the first edge (right step) by a diagonal up‑right + down."""
    v0 = path[0]
    q = (v0[0] - 1, v0[1] + 1)
    return [v0, q] + path[1:]


def construct_blue_cycle(B):
    """R = 0, B even, B >= 2."""
    if B == 2:
        return [(1, 1), (2, 2)]
    k = B // 2          # k >= 2
    a = 1
    b = k - 1           # b >= 1
    # choose start to keep everything >= 1
    r0 = b + 2
    c0 = b + 2
    path = [(r0, c0)]
    # down‑right a steps
    for j in range(1, a + 1):
        path.append((r0 + j, c0 + j))
    # up‑right b steps
    cur_r, cur_c = r0 + a, c0 + a
    for _ in range(b):
        cur_r -= 1
        cur_c += 1
        path.append((cur_r, cur_c))
    # up‑left a steps
    for _ in range(a):
        cur_r -= 1
        cur_c -= 1
        path.append((cur_r, cur_c))
    # down‑left b steps (the last one returns to start)
    for _ in range(b):
        cur_r += 1
        cur_c -= 1
        path.append((cur_r, cur_c))
    # the last vertex equals the start, remove it
    if path[-1] == (r0, c0):
        path.pop()
    return path


# ------------------------------------------------------------
# type computation
# ------------------------------------------------------------

def compute_types(path):
    n = len(path)
    types = []
    for i in range(n):
        r1, c1 = path[i]
        r2, c2 = path[(i + 1) % n]
        if abs(r1 - r2) + abs(c1 - c2) == 1:
            types.append('R')
        else:               # must be diagonal
            types.append('B')
    return types


# ------------------------------------------------------------
# main solver
# ------------------------------------------------------------

def solve_one(R, B):
    # feasibility test
    if R % 2 == 1:
        return None                     # impossible
    if R == 0:
        if B % 2 == 1:
            return None
        # pure blue cycle
        path = construct_blue_cycle(B)
        types = ['B'] * len(path)
        return list(zip(path, types))

    # now R >= 2 and even
    if B == 0:
        path = construct_rectangle(R)
    elif B == 1:
        path = construct_B1(R)
    elif B % 2 == 0:
        path = construct_parallelogram(R, B)
    else:   # B odd and >= 3
        h = (B - 1) // 2
        path = construct_parallelogram(R, 2 * h)
        path = apply_detour(path)

    types = compute_types(path)
    return list(zip(path, types))


def solve() -> None:
    it = iter(sys.stdin.read().strip().split())
    T = int(next(it))
    out_lines = []
    for _ in range(T):
        R = int(next(it))
        B = int(next(it))
        res = solve_one(R, B)
        if res is None:
            out_lines.append("No")
        else:
            out_lines.append("Yes")
            for (r, c), t in res:
                out_lines.append(f"{t} {r} {c}")
    sys.stdout.write("\n".join(out_lines))


if __name__ == "__main__":
    solve()