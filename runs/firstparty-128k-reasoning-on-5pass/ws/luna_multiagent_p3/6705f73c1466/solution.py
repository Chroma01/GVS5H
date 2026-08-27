import sys


def solve():
    data = sys.stdin.buffer.read().split()
    s = data[1]

    adjusted = []
    one_index = 0

    for position, value in enumerate(s):
        if value == ord('1'):
            adjusted.append(position - one_index)
            one_index += 1

    adjusted.sort()
    median = adjusted[len(adjusted) // 2]
    answer = sum(abs(value - median) for value in adjusted)

    print(answer)


if __name__ == "__main__":
    solve()