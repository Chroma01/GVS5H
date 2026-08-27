import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    last = [0] * (n + 2)  # indices 0..n+1; last[0] and last[n+1] are boundaries

    cur = 0  # sum of f(L, i) over L for the current right endpoint i
    ans = 0

    for i in range(1, n + 1):
        x = data[i]
        prev = last[x]

        # For L in (prev, i], x was absent before adding position i.
        # Adding x changes f by 1 - [x-1 present] - [x+1 present].
        d = i - prev

        ly = last[x - 1]
        if ly > prev:
            d -= ly - prev

        ry = last[x + 1]
        if ry > prev:
            d -= ry - prev

        cur += d
        ans += cur
        last[x] = i

    print(ans)

if __name__ == "__main__":
    main()