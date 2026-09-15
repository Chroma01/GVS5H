import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    t = data[0]
    idx = 1
    ans = []

    for _ in range(t):
        n = data[idx]
        idx += 1

        vals = []
        lens = []

        prev = data[idx]
        idx += 1
        cnt = 1

        for _ in range(n - 1):
            x = data[idx]
            idx += 1
            if x == prev:
                cnt += 1
            else:
                vals.append(prev)
                lens.append(cnt)
                prev = x
                cnt = 1

        vals.append(prev)
        lens.append(cnt)

        r = len(vals)

        # With at most three runs, no swap can reduce the number of deletions
        # by more than its own cost.
        if r <= 3:
            ans.append(str(r))
            continue

        # dp0[i] = dp[i][1], dp1[i] = dp[i][2], dp2[i] = dp[i][3]
        dp0 = [1] * (r + 4)
        dp1 = [1] * (r + 4)
        dp2 = [1] * (r + 4)

        v = vals
        ln = lens

        for i in range(r - 1, -1, -1):
            vi = v[i]

            # g = 1
            j = i + 1
            if j < r:
                best = 1 + dp0[j]
                k = j + 1
                if k < r and ln[j] == 1 and ln[k] == 1 and v[k] == vi:
                    l = k + 1
                    if l < r and v[l] == v[j]:
                        cost = 2 + dp2[j]
                    else:
                        cost = 2 + dp1[j]
                    if cost < best:
                        best = cost
                dp0[i] = best

            # g = 2
            j = i + 2
            if j < r:
                best = 1 + dp0[j]
                k = j + 1
                if k < r and ln[j] == 1 and ln[k] == 1 and v[k] == vi:
                    l = k + 1
                    if l < r and v[l] == v[j]:
                        cost = 2 + dp2[j]
                    else:
                        cost = 2 + dp1[j]
                    if cost < best:
                        best = cost
                dp1[i] = best

            # g = 3
            j = i + 3
            if j < r:
                best = 1 + dp0[j]
                k = j + 1
                if k < r and ln[j] == 1 and ln[k] == 1 and v[k] == vi:
                    l = k + 1
                    if l < r and v[l] == v[j]:
                        cost = 2 + dp2[j]
                    else:
                        cost = 2 + dp1[j]
                    if cost < best:
                        best = cost
                dp2[i] = best

        ans.append(str(dp0[0]))

    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    solve()