import sys


def main():
    input = sys.stdin.buffer.readline

    n = int(input())
    a = list(map(int, input().split()))

    # last[x] = latest position where value x has appeared.
    # last[n + 1] remains 0 as the virtual always-absent successor.
    last = [0] * (n + 2)

    # S = sum_{x=1..n} max(0, last[x] - last[x+1])
    current_sum = 0
    answer = 0

    for r, x in enumerate(a, 1):
        # Only terms for x-1 and x can change.
        if x > 1:
            current_sum -= max(0, last[x - 1] - last[x])
        current_sum -= max(0, last[x] - last[x + 1])

        last[x] = r

        if x > 1:
            current_sum += max(0, last[x - 1] - last[x])
        current_sum += max(0, last[x] - last[x + 1])

        answer += current_sum

    print(answer)


if __name__ == "__main__":
    main()