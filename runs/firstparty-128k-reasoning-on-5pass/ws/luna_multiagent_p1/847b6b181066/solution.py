import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    R = int(data[1])
    C = int(data[2])
    s = data[3].decode()

    row = 0
    col = 0
    visited = {(0, 0)}
    answer = []

    for ch in s:
        if ch == 'N':
            row -= 1
        elif ch == 'S':
            row += 1
        elif ch == 'W':
            col -= 1
        else:  # E
            col += 1

        visited.add((row, col))
        answer.append('1' if (row - R, col - C) in visited else '0')

    sys.stdout.write(''.join(answer))

if __name__ == "__main__":
    solve()