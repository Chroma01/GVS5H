import sys

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())

    constraints = []
    for _ in range(M):
        x, y, c = input().split()
        constraints.append((int(x), int(y), c))

    constraints.sort(key=lambda p: p[0])

    smallest_white_column = N + 1
    i = 0

    while i < M:
        x = constraints[i][0]
        j = i

        # First include all white cells in this row.
        while j < M and constraints[j][0] == x:
            _, y, c = constraints[j]
            if c == 'W':
                smallest_white_column = min(smallest_white_column, y)
            j += 1

        # Then test black cells in this row against all whites above or in this row.
        for k in range(i, j):
            _, y, c = constraints[k]
            if c == 'B' and smallest_white_column <= y:
                print("No")
                return

        i = j

    print("Yes")

if __name__ == "__main__":
    solve()