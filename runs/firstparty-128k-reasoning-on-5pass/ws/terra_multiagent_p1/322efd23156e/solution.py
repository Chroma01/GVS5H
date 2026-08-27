import sys


def main():
    input = sys.stdin.buffer.readline
    N, X = map(int, input().split())

    dp = [[0] * (X + 1) for _ in range(3)]

    for _ in range(N):
        v, a, c = map(int, input().split())
        cur = dp[v - 1]
        for cal in range(X, c - 1, -1):
            value = cur[cal - c] + a
            if value > cur[cal]:
                cur[cal] = value

    for v in range(3):
        cur = dp[v]
        for cal in range(1, X + 1):
            if cur[cal - 1] > cur[cal]:
                cur[cal] = cur[cal - 1]

    d1, d2, d3 = dp
    answer = 0

    for c1 in range(X + 1):
        v1 = d1[c1]
        remaining_after_1 = X - c1

        for c2 in range(remaining_after_1 + 1):
            value = min(v1, d2[c2], d3[remaining_after_1 - c2])
            if value > answer:
                answer = value

    print(answer)


if __name__ == "__main__":
    main()