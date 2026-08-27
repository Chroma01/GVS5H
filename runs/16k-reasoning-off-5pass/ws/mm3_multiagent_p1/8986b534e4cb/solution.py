import sys

def solve():
    data = sys.stdin.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    Q = int(next(it))
    even = [0] * (M + 1)  # 1-indexed
    for i in range(1, M + 1):
        s = int(next(it))
        t = int(next(it))
        if abs(s - t) % 2 == 0:
            even[i] = 1
        else:
            even[i] = 0
    # prefix sum
    pref = [0] * (M + 1)
    for i in range(1, M + 1):
        pref[i] = pref[i - 1] + even[i]
    out_lines = []
    for _ in range(Q):
        L = int(next(it))
        R = int(next(it))
        total_even = pref[R] - pref[L - 1]
        if total_even == R - L + 1:
            out_lines.append("Yes")
        else:
            out_lines.append("No")
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()