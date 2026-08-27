import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    if n <= 1:
        sys.stdout.write("-1\n")
        return

    idx = 1
    prev_x = int(data[idx])
    prev_h = int(data[idx + 1])
    idx += 2

    best_num = None
    best_den = 1

    for _ in range(1, n):
        x = int(data[idx])
        h = int(data[idx + 1])
        idx += 2

        num = prev_h * x - h * prev_x
        den = x - prev_x

        if best_num is None or num * best_den > best_num * den:
            best_num = num
            best_den = den

        prev_x, prev_h = x, h

    if best_num is None or best_num < 0:
        sys.stdout.write("-1\n")
    elif best_num == 0:
        sys.stdout.write("0." + "0" * 18 + "\n")
    else:
        sys.stdout.write(f"{best_num / best_den:.18f}\n")

if __name__ == "__main__":
    main()