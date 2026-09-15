import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    idx = 1
    X = [0] * n
    H = [0] * n
    for i in range(n):
        X[i] = int(data[idx])
        H[i] = int(data[idx + 1])
        idx += 2

    # A single building is always fully visible.
    if n == 1:
        sys.stdout.write("-1\n")
        return

    # f_i = (X_{i+1}*H_i - X_i*H_{i+1}) / (X_{i+1} - X_i), denominator > 0.
    best_num = X[1] * H[0] - X[0] * H[1]
    best_den = X[1] - X[0]
    for i in range(1, n - 1):
        num = X[i + 1] * H[i] - X[i] * H[i + 1]
        den = X[i + 1] - X[i]
        # Exact big-int cross multiplication (valid for negatives, den > 0).
        if num * best_den > best_num * den:
            best_num = num
            best_den = den

    if best_num < 0:
        # Height 0 already sees every building.
        sys.stdout.write("-1\n")
    else:
        # Correctly-rounded float formatting; matches the sample harness.
        sys.stdout.write(f"{best_num / best_den:.18f}\n")


main()