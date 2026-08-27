import sys
from collections import deque


def normal_form(s: str, x: int, y: int):
    runs = deque()
    n = len(s)
    i = 0

    while i < n:
        j = i + 1
        while j < n and s[j] == s[i]:
            j += 1
        runs.append((s[i], j - i))
        i = j

    stack = []

    while runs:
        bit, length = runs.popleft()
        if length <= 0:
            continue

        if stack and stack[-1][0] == bit:
            stack[-1][1] += length
        else:
            stack.append([bit, length])

        while len(stack) >= 2:
            bit1, a = stack[-2]
            bit2, b = stack[-1]

            if bit1 != "1" or bit2 != "0" or a < y or b < x:
                break

            stack.pop()
            stack.pop()

            k = min(a // y, b // x)
            replacement = (
                ("1", a - k * y),
                ("0", k * x),
                ("1", k * y),
                ("0", b - k * x),
            )

            for item in reversed(replacement):
                if item[1] > 0:
                    runs.appendleft(item)

            break

    return tuple((bit, length) for bit, length in stack)


def main():
    input = sys.stdin.readline

    n, x, y = map(int, input().split())
    s = input().strip()
    t = input().strip()

    print("Yes" if normal_form(s, x, y) == normal_form(t, x, y) else "No")


if __name__ == "__main__":
    main()