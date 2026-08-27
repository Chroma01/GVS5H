import sys

def main():
    input = sys.stdin.readline
    N, M = map(int, input().split())

    points = []
    for _ in range(M):
        x, y, c = input().split()
        points.append((int(y), int(x), c))

    points.sort(reverse=True)  # descending by column

    max_black_row = -1
    i = 0

    while i < M:
        j = i
        col = points[i][0]

        while j < M and points[j][0] == col:
            _, row, color = points[j]
            if color == 'B':
                max_black_row = max(max_black_row, row)
            j += 1

        for k in range(i, j):
            _, row, color = points[k]
            if color == 'W' and row <= max_black_row:
                print("No")
                return

        i = j

    print("Yes")

if __name__ == "__main__":
    main()