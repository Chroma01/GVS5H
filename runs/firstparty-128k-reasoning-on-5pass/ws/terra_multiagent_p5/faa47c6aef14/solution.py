import sys
from bisect import bisect_left


def build_required_path(perm, has_ball, x):
    n = len(perm)

    cycle = []
    pos_in_cycle = [-1] * n
    v = x
    while pos_in_cycle[v] == -1:
        pos_in_cycle[v] = len(cycle)
        cycle.append(v)
        v = perm[v]

    # Since we started at x, this is exactly x's permutation cycle.
    length = len(cycle)

    farthest_dist = 0
    for i, present in enumerate(has_ball):
        if not present or i == x:
            continue
        if pos_in_cycle[i] == -1:
            return None
        # cycle[pos] is reached from x after pos steps.
        # Distance from this vertex to x along perm is length - pos.
        dist = length - pos_in_cycle[i]
        if dist > farthest_dist:
            farthest_dist = dist

    if farthest_dist == 0:
        return []

    start_pos = length - farthest_dist
    path = []
    for p in range(start_pos, length):
        path.append(cycle[p])
    return path


def main():
    input = sys.stdin.readline

    n, x = map(int, input().split())
    x -= 1

    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    p = [v - 1 for v in map(int, input().split())]
    q = [v - 1 for v in map(int, input().split())]

    red_path = build_required_path(p, a, x)
    blue_path = build_required_path(q, b, x)

    if red_path is None or blue_path is None:
        print(-1)
        return

    # The minimum operation sequence is a shortest common supersequence
    # of the red path and blue path. Each path has distinct vertices.
    pos_red = [-1] * n
    for i, v in enumerate(red_path):
        pos_red[v] = i

    lis = []
    for v in blue_path:
        pos = pos_red[v]
        if pos != -1:
            k = bisect_left(lis, pos)
            if k == len(lis):
                lis.append(pos)
            else:
                lis[k] = pos

    lcs = len(lis)
    print(len(red_path) + len(blue_path) - lcs)


if __name__ == "__main__":
    main()