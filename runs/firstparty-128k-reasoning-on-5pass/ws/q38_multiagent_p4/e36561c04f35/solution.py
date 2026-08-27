import sys


def solve_case(A):
    n = len(A)

    vals = []
    lens = []

    prev = A[0]
    cnt = 1
    for i in range(1, n):
        x = A[i]
        if x == prev:
            cnt += 1
        else:
            vals.append(prev)
            lens.append(cnt)
            prev = x
            cnt = 1
    vals.append(prev)
    lens.append(cnt)

    m = len(vals)
    if m == 1:
        return 1

    # dp_im1 = dp[i-1], dp_im2 = dp[i-2], dp_im3 = dp[i-3]
    dp_im1 = 0
    dp_im2 = 0
    dp_im3 = 0

    for i in range(m - 1):
        best = dp_im1

        # Useful swap: edge i swaps two length-1 runs in pattern x y x y.
        if (
            i >= 1
            and i + 2 < m
            and lens[i] == 1
            and lens[i + 1] == 1
            and vals[i - 1] == vals[i + 1]
            and vals[i] == vals[i + 2]
        ):
            cand = dp_im3 + 1
            if cand > best:
                best = cand

        dp_im3 = dp_im2
        dp_im2 = dp_im1
        dp_im1 = best

    return m - dp_im1


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    idx = 1
    out = []

    for _ in range(t):
        n = int(data[idx])
        idx += 1
        A = list(map(int, data[idx:idx + n]))
        idx += n
        out.append(str(solve_case(A)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()