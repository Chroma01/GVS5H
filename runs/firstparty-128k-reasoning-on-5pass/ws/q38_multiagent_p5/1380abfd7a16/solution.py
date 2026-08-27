import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    m = 1 << ((n - 1).bit_length())

    bit = [0] * (m + 1)
    bit[1:n + 1] = [i & -i for i in range(1, n + 1)]

    ba = bit
    nn = n
    for i in range(nn + 1, m + 1):
        left = i - (i & -i)
        if left < nn:
            ba[i] = nn - left

    nxt = [0] * (m + 1)
    nxt[1:m + 1] = [j + (j & -j) for j in range(1, m + 1)]

    steps = []
    step = m >> 1
    while step:
        steps.append(step)
        step >>= 1
    steps = tuple(steps)

    ans = [0] * n
    data_arr = data
    ans_arr = ans
    m_local = m
    nxt_arr = nxt

    for val in range(n, 0, -1):
        k = data_arr[val]
        idx = 0

        for step in steps:
            nxt_pos = idx + step
            v = ba[nxt_pos]
            if v < k:
                idx = nxt_pos
                k -= v

        pos = idx + 1
        ans_arr[pos - 1] = val

        j = pos
        while j <= m_local:
            ba[j] -= 1
            j = nxt_arr[j]

    sys.stdout.write(' '.join(map(str, ans_arr)))
    sys.stdout.write('\n')

if __name__ == '__main__':
    main()