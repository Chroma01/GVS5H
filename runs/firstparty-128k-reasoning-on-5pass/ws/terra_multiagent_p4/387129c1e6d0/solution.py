import sys

def mark_visited(houses, segments, visited):
    houses.sort()
    segments.sort()

    n = len(houses)
    m = len(segments)
    hp = 0
    si = 0

    while si < m:
        fixed = segments[si][0]

        while hp < n and houses[hp][0] < fixed:
            hp += 1

        hq = hp
        while hq < n and houses[hq][0] == fixed:
            hq += 1

        k = hp

        def apply_interval(left, right):
            nonlocal k
            while k < hq and houses[k][1] < left:
                k += 1
            while k < hq and houses[k][1] <= right:
                visited[houses[k][2]] = True
                k += 1

        left = segments[si][1]
        right = segments[si][2]
        si += 1

        while si < m and segments[si][0] == fixed:
            nl = segments[si][1]
            nr = segments[si][2]

            if nl <= right:
                if nr > right:
                    right = nr
            else:
                apply_interval(left, right)
                left, right = nl, nr

            si += 1

        apply_interval(left, right)
        hp = hq


def solve():
    input = sys.stdin.buffer.readline

    n, m, sx, sy = map(int, input().split())

    horizontal_houses = []
    vertical_houses = []

    for i in range(n):
        x, y = map(int, input().split())
        horizontal_houses.append((y, x, i))
        vertical_houses.append((x, y, i))

    horizontal_segments = []
    vertical_segments = []

    x, y = sx, sy

    for _ in range(m):
        d, c = input().split()
        c = int(c)

        if d == b'L':
            nx = x - c
            horizontal_segments.append((y, nx, x))
            x = nx
        elif d == b'R':
            nx = x + c
            horizontal_segments.append((y, x, nx))
            x = nx
        elif d == b'D':
            ny = y - c
            vertical_segments.append((x, ny, y))
            y = ny
        else:
            ny = y + c
            vertical_segments.append((x, y, ny))
            y = ny

    visited = [False] * n

    mark_visited(horizontal_houses, horizontal_segments, visited)
    mark_visited(vertical_houses, vertical_segments, visited)

    print(x, y, sum(visited))


if __name__ == "__main__":
    solve()