import sys

def solve():
    input = sys.stdin.readline
    n = int(input())
    s = input().strip()

    adjusted = []
    ones_seen = 0

    for pos, ch in enumerate(s):
        if ch == "1":
            adjusted.append(pos - ones_seen)
            ones_seen += 1

    median = adjusted[len(adjusted) // 2]
    answer = sum(abs(value - median) for value in adjusted)

    print(answer)

if __name__ == "__main__":
    solve()