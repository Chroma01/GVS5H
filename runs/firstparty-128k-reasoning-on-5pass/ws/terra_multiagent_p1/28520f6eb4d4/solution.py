import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]

    if n == 1:
        print(-1)
        return

    px = data[1]
    ph = data[2]

    best_num = None
    best_den = 1

    pos = 3
    for _ in range(1, n):
        x = data[pos]
        h = data[pos + 1]
        pos += 2

        num = x * ph - px * h
        den = x - px

        if best_num is None or num * best_den > best_num * den:
            best_num = num
            best_den = den

        px, ph = x, h

    if best_num < 0:
        print(-1)
    else:
        print("{:.18f}".format(best_num / best_den))

if __name__ == "__main__":
    main()