import sys

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())

    events = []
    for _ in range(M):
        x, y, c = input().split()
        events.append((int(x), int(y), c))

    events.sort()

    min_white_col = 10**30
    i = 0

    while i < M:
        row = events[i][0]
        j = i
        while j < M and events[j][0] == row:
            if events[j][2] == 'W':
                min_white_col = min(min_white_col, events[j][1])
            j += 1

        for k in range(i, j):
            x, y, c = events[k]
            if c == 'B' and min_white_col <= y:
                print("No")
                return

        i = j

    print("Yes")

if __name__ == "__main__":
    solve()