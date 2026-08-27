import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    if n == 1:
        print(-1)
        return

    idx = 1
    prev_x = int(data[idx])
    prev_h = int(data[idx + 1])
    idx += 2

    best_num = None
    best_den = 1

    for _ in range(n - 1):
        x = int(data[idx])
        h = int(data[idx + 1])
        idx += 2

        num = x * prev_h - prev_x * h
        den = x - prev_x

        if best_num is None or num * best_den > best_num * den:
            best_num = num
            best_den = den

        prev_x, prev_h = x, h

    if best_num is None or best_num < 0:
        print(-1)
    elif best_num == 0:
        print("0.000000000000000000")
    else:
        print(f"{best_num / best_den:.18f}")


if __name__ == "__main__":
    main()