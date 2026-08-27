import sys

def main():
    vals = list(map(int, sys.stdin.buffer.read().split()))
    if not vals:
        return

    n = vals[0]
    if n == 1:
        print(-1)
        return

    prev_x = vals[1]
    prev_h = vals[2]

    x = vals[3]
    h = vals[4]
    best_num = prev_h * x - h * prev_x
    best_den = x - prev_x

    prev_x, prev_h = x, h

    for i in range(5, len(vals), 2):
        x = vals[i]
        h = vals[i + 1]

        num = prev_h * x - h * prev_x
        den = x - prev_x

        if num * best_den > best_num * den:
            best_num = num
            best_den = den

        prev_x, prev_h = x, h

    if best_num < 0:
        print(-1)
    elif best_num == 0:
        print("0.000000000000000000")
    else:
        print(f"{best_num / best_den:.18f}")

if __name__ == "__main__":
    main()