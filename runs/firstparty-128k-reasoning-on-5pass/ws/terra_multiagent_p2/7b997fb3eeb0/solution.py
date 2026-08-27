import sys
from bisect import bisect_left

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:1 + n]

    # d[i] = first position having size >= 2*a[i], minus i
    d = [bisect_left(a, x * 2) - i for i, x in enumerate(a)]

    logs = [0] * (n + 1)
    for i in range(2, n + 1):
        logs[i] = logs[i >> 1] + 1

    st = [d]
    length = 2
    while length <= n:
        prev = st[-1]
        half = length >> 1
        m = n - length + 1
        cur = [
            prev[i] if prev[i] >= prev[i + half] else prev[i + half]
            for i in range(m)
        ]
        st.append(cur)
        length <<= 1

    pos = 1 + n
    q = data[pos]
    pos += 1
    ans = []

    for _ in range(q):
        l = data[pos] - 1
        r = data[pos + 1] - 1
        pos += 2

        lo = 0
        hi = (r - l + 1) // 2

        while lo < hi:
            k = (lo + hi + 1) >> 1
            level = logs[k]
            row = st[level]
            block = 1 << level

            mx = row[l]
            other = row[l + k - block]
            if other > mx:
                mx = other

            if mx <= r - l - k + 1:
                lo = k
            else:
                hi = k - 1

        ans.append(str(lo))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    main()