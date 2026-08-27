import sys
from bisect import bisect_left


def cycle_path_to_x(perm, x):
    """Vertices of x's cycle excluding x, in forwarding order toward x."""
    path = []
    v = perm[x]
    while v != x:
        path.append(v)
        v = perm[v]
    return path


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    x = next(it) - 1
    a = [next(it) for _ in range(n)]
    b = [next(it) for _ in range(n)]
    p = [next(it) - 1 for _ in range(n)]
    q = [next(it) - 1 for _ in range(n)]

    p_path = cycle_path_to_x(p, x)
    q_path = cycle_path_to_x(q, x)

    p_pos = [-1] * n
    q_pos = [-1] * n
    for i, v in enumerate(p_path):
        p_pos[v] = i
    for i, v in enumerate(q_path):
        q_pos[v] = i

    # A red ball can only travel on its P-cycle, and a blue ball on its Q-cycle.
    for v in range(n):
        if a[v] and v != x and p_pos[v] == -1:
            print(-1)
            return
        if b[v] and v != x and q_pos[v] == -1:
            print(-1)
            return

    # Required operations for each color are a suffix of its path toward X.
    first_p = len(p_path)
    for v in range(n):
        if a[v] and v != x:
            first_p = min(first_p, p_pos[v])

    first_q = len(q_path)
    for v in range(n):
        if b[v] and v != x:
            first_q = min(first_q, q_pos[v])

    red_seq = p_path[first_p:]
    blue_seq = q_path[first_q:]

    # The operation schedule is a shortest common supersequence of these paths.
    # Their entries are distinct within each sequence, so LCS is LIS of P positions
    # encountered along the blue sequence.
    red_index = [-1] * n
    for i, v in enumerate(red_seq):
        red_index[v] = i

    lis = []
    for v in blue_seq:
        pos = red_index[v]
        if pos != -1:
            k = bisect_left(lis, pos)
            if k == len(lis):
                lis.append(pos)
            else:
                lis[k] = pos

    print(len(red_seq) + len(blue_seq) - len(lis))


if __name__ == "__main__":
    main()