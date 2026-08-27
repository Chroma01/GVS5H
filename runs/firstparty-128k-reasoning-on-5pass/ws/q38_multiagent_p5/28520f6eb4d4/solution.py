import sys

def main():
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

    max_num = None
    max_den = 1

    for _ in range(n - 1):
        x = int(data[idx])
        h = int(data[idx + 1])
        idx += 2

        num = prev_h * x - h * prev_x
        den = x - prev_x

        if max_num is None or num * max_den > max_num * den:
            max_num = num
            max_den = den

        prev_x, prev_h = x, h

    if max_num < 0:
        print(-1)
    elif max_num == 0:
        print("0.000000000000000000")
    else:
        print(f"{max_num / max_den:.18f}")

if __name__ == "__main__":
    main()