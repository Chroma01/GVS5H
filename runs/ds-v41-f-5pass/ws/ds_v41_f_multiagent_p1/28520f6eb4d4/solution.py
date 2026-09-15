import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    xs = [0] * n
    hs = [0] * n
    p = 1
    for i in range(n):
        xs[i] = int(data[p]); hs[i] = int(data[p + 1]); p += 2

    # Single building is always visible from any height -> -1
    if n == 1:
        sys.stdout.write("-1\n")
        return

    bestP = None
    bestQ = 1
    for i in range(n - 1):
        # threshold T_i = (H_i*X_{i+1} - H_{i+1}*X_i) / (X_{i+1} - X_i), Q > 0
        P = hs[i] * xs[i + 1] - hs[i + 1] * xs[i]
        Q = xs[i + 1] - xs[i]
        if bestP is None or P * bestQ > bestP * Q:
            bestP = P
            bestQ = Q

    # M = max T_i. h=0 sees all iff 0 > M iff M < 0.
    if bestP < 0:
        sys.stdout.write("-1\n")
        return

    val = bestP / bestQ
    sys.stdout.write(f"{val:.18f}\n")

main()