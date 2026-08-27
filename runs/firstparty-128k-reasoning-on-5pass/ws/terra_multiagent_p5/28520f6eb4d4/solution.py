import sys


def main():
    input = sys.stdin.buffer.readline
    n = int(input())

    prev_x, prev_h = map(int, input().split())

    possible_at_zero = True
    best_num = 0
    best_den = 1

    for _ in range(1, n):
        x, h = map(int, input().split())

        required_num = prev_h * x - h * prev_x
        required_den = x - prev_x

        if required_num >= 0:
            possible_at_zero = False
            if required_num * best_den > best_num * required_den:
                best_num = required_num
                best_den = required_den

        prev_x, prev_h = x, h

    if possible_at_zero:
        print(-1)
    else:
        print(f"{best_num / best_den:.18f}")


if __name__ == "__main__":
    main()