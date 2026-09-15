import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    xs = [0] * n
    hs = [0] * n
    idx = 1
    for i in range(n):
        xs[i] = int(data[idx])
        hs[i] = int(data[idx + 1])
        idx += 2

    if n == 1:
        print(-1)
        return

    best_num = None
    best_den = 1
    for i in range(n - 1):
        num = hs[i] * xs[i + 1] - hs[i + 1] * xs[i]
        den = xs[i + 1] - xs[i]
        if best_num is None or num * best_den > best_num * den:
            best_num = num
            best_den = den

    if best_num < 0:
        print(-1)
    else:
        ans = best_num / best_den
        print(f"{ans:.18f}")

if __name__ == "__main__":
    solve()