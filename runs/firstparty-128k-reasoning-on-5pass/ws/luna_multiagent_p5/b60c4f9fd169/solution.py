import sys


def main():
    data = sys.stdin.buffer.read().split()
    k = int(data[0])
    s = data[1].decode()
    t = data[2].decode()

    ls = len(s)
    lt = len(t)

    if abs(ls - lt) > k:
        print("No")
        return

    # Remove a common prefix.
    prefix = 0
    while prefix < ls and prefix < lt and s[prefix] == t[prefix]:
        prefix += 1

    # Remove a common suffix, without overlapping the removed prefix.
    suffix = 0
    while (
        prefix + suffix < ls
        and prefix + suffix < lt
        and s[ls - 1 - suffix] == t[lt - 1 - suffix]
    ):
        suffix += 1

    s_left = prefix
    t_left = prefix
    s_len = ls - prefix - suffix
    t_len = lt - prefix - suffix

    if s_len == 0 or t_len == 0:
        print("Yes" if max(s_len, t_len) <= k else "No")
        return

    # Use the shorter remaining string as the DP row dimension.
    if s_len <= t_len:
        a, a_start, m = s, s_left, s_len
        b, b_start, n = t, t_left, t_len
    else:
        a, a_start, m = t, t_left, t_len
        b, b_start, n = s, s_left, s_len

    if n - m > k:
        print("No")
        return

    inf = k + 1

    # Row i stores dp[i][j] only for max(0, i-k) <= j <= min(n, i+k).
    prev_lo = 0
    prev_hi = min(n, k)
    prev = list(range(prev_hi + 1))

    for i in range(1, m + 1):
        lo = max(0, i - k)
        hi = min(n, i + k)
        cur = [inf] * (hi - lo + 1)
        a_char = a[a_start + i - 1]

        for idx in range(len(cur)):
            j = lo + idx
            best = inf

            # Delete a character from a.
            if prev_lo <= j <= prev_hi:
                value = prev[j - prev_lo] + 1
                if value < best:
                    best = value

            # Insert a character into a.
            if idx > 0:
                value = cur[idx - 1] + 1
                if value < best:
                    best = value

            # Match or replace one character.
            if j > 0 and prev_lo <= j - 1 <= prev_hi:
                value = prev[j - 1 - prev_lo]
                if a_char != b[b_start + j - 1]:
                    value += 1
                if value < best:
                    best = value

            cur[idx] = best if best <= k else inf

        prev = cur
        prev_lo = lo
        prev_hi = hi

    if prev_lo <= n <= prev_hi and prev[n - prev_lo] <= k:
        print("Yes")
    else:
        print("No")


if __name__ == "__main__":
    main()