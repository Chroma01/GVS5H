import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    t = data[0]
    idx = 1
    out = []

    for _ in range(t):
        n = data[idx]
        idx += 1

        prev = data[idx]
        idx += 1

        colors = []
        lengths = []
        cnt = 1

        for _ in range(n - 1):
            x = data[idx]
            idx += 1
            if x == prev:
                cnt += 1
            else:
                colors.append(prev)
                lengths.append(cnt)
                prev = x
                cnt = 1

        colors.append(prev)
        lengths.append(cnt)

        r = len(colors)

        if r < 4:
            out.append(str(r))
            continue

        # dp[k] = maximum number of useful reductions using the first k runs.
        dp = [0] * (r + 1)
        c = colors
        l = lengths

        for k in range(4, r + 1):
            # Last four runs are k-4, k-3, k-2, k-1.
            # Middle two runs are k-3 and k-2.
            if (
                l[k - 3] == 1
                and l[k - 2] == 1
                and c[k - 4] == c[k - 2]
                and c[k - 3] == c[k - 1]
            ):
                cand = dp[k - 3] + 1
                if cand > dp[k - 1]:
                    dp[k] = cand
                else:
                    dp[k] = dp[k - 1]
            else:
                dp[k] = dp[k - 1]

        out.append(str(r - dp[r]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()