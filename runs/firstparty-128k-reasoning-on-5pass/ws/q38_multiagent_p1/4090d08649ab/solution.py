import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    last = [0] * (n + 2)

    s = 0
    ans = 0

    for r in range(1, n + 1):
        v = data[r]

        lv = last[v]
        lv_prev = last[v - 1]

        tv = lv - lv_prev
        if tv > 0:
            s -= tv

        if v < n:
            lv_next = last[v + 1]
            tv_next = lv_next - lv
            if tv_next > 0:
                s -= tv_next

        last[v] = r

        tv = r - lv_prev
        if tv > 0:
            s += tv

        if v < n:
            lv_next = last[v + 1]
            tv_next = lv_next - r
            if tv_next > 0:
                s += tv_next

        ans += s

    print(ans)

if __name__ == "__main__":
    main()