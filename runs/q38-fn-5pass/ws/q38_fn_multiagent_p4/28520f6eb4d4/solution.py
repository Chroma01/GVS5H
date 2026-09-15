import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    if n <= 1:
        print(-1)
        return

    prev_x = int(data[1])
    prev_h = int(data[2])

    best_num = None
    best_den = 1

    idx = 3
    for _ in range(n - 1):
        x = int(data[idx])
        h = int(data[idx + 1])
        idx += 2

        # Threshold for the adjacent pair (prev, current):
        # (H_prev * X_cur - H_cur * X_prev) / (X_cur - X_prev)
        num = prev_h * x - h * prev_x
        den = x - prev_x

        if best_num is None or num * best_den > best_num * den:
            best_num = num
            best_den = den

        prev_x, prev_h = x, h

    # If the maximum threshold is negative, height 0 already sees all buildings.
    if best_num is None or best_num < 0:
        print(-1)
        return

    # Print the selected rational as a double-style decimal.
    print(f"{best_num / best_den:.18f}")

if __name__ == "__main__":
    solve()