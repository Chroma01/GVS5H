import sys

def main():
    arr = list(map(int, sys.stdin.buffer.read().split()))
    if not arr:
        return
    N = arr[0]
    if N < 3:
        sys.stdout.write("0\n")
        return

    first = [0] * (N + 1)
    last = [0] * (N + 1)
    total_distinct = 0
    for idx in range(1, N + 1):
        v = arr[idx]
        if first[v] == 0:
            first[v] = idx
            total_distinct += 1
        last[v] = idx

    diff = [0] * (N + 2)
    for v in range(1, N + 1):
        f = first[v]
        if f:
            l = last[v]
            if f < l:
                diff[f] += 1
                diff[l] -= 1
    del first, last

    size = 1 << (N - 1).bit_length()
    seg_sum = [0] * (2 * size)
    seg_pref = [0] * (2 * size)

    def add_interval(l, r, ss=seg_sum, sp=seg_pref, sz=size):
        i = sz + l - 1
        s = ss[i] + 1
        ss[i] = s
        sp[i] = s if s > 0 else 0

        k = sz + r - 1
        s = ss[k] - 1
        ss[k] = s
        sp[k] = s if s > 0 else 0

        i >>= 1
        k >>= 1
        while i:
            left = i << 1
            right = left | 1
            sl = ss[left]
            sr = ss[right]
            ss[i] = sl + sr
            pl = sp[left]
            pr = sp[right]
            v = sl + pr
            sp[i] = pl if pl >= v else v

            if k != i:
                left = k << 1
                right = left | 1
                sl = ss[left]
                sr = ss[right]
                ss[k] = sl + sr
                pl = sp[left]
                pr = sp[right]
                v = sl + pr
                sp[k] = pl if pl >= v else v

            i >>= 1
            k >>= 1

    prev = [0] * (N + 1)
    prev[arr[1]] = 1

    c = 0
    ans = 0
    sp = seg_pref
    add = add_interval
    T = total_distinct

    for j in range(1, N):
        c += diff[j]
        if j == 1:
            continue

        v = arr[j]
        p = prev[v]
        if p:
            add(p, j)
        prev[v] = j

        val = T + c + sp[1]
        if val > ans:
            ans = val

    sys.stdout.write(str(ans) + "\n")

if __name__ == "__main__":
    main()