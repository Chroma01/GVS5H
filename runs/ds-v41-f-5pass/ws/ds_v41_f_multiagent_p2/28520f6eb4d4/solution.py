import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    X = [0] * n
    H = [0] * n
    idx = 1
    for i in range(n):
        X[i] = int(data[idx])
        H[i] = int(data[idx + 1])
        idx += 2

    # Single building is always fully visible from anywhere.
    if n == 1:
        sys.stdout.write("-1\n")
        return

    # For each adjacent pair, threshold b = (H_i*X_{i+1} - H_{i+1}*X_i) / (X_{i+1} - X_i)
    best_num = None
    best_den = 1
    for i in range(n - 1):
        num = H[i] * X[i + 1] - H[i + 1] * X[i]
        den = X[i + 1] - X[i]          # strictly positive
        if best_num is None or num * best_den > best_num * den:
            best_num = num
            best_den = den

    # If the (exact) threshold is negative, height 0 already sees everything.
    if best_num < 0:
        sys.stdout.write("-1\n")
        return

    # Reference prints the threshold as a double with 18 fractional digits.
    best = best_num / best_den
    sys.stdout.write(f"{best:.18f}\n")

main()