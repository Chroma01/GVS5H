import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    if n == 1:
        sys.stdout.write("-1\n")
        return

    best_num = None
    best_den = 1

    prev_x = int(data[1])
    prev_h = int(data[2])
    idx = 3

    for _ in range(n - 1):
        x = int(data[idx])
        h = int(data[idx + 1])
        idx += 2

        num = prev_h * x - h * prev_x
        den = x - prev_x

        if best_num is None or num * best_den > best_num * den:
            best_num = num
            best_den = den

        prev_x, prev_h = x, h

    if best_num < 0:
        sys.stdout.write("-1\n")
        return

    sys.stdout.write(f"{best_num / best_den:.18f}\n")

if __name__ == "__main__":
    main()