import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    pos = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        pos[data[i]].append(i)

    total = n * (n + 1) // 2

    # W[v] = number of subarrays that contain no occurrence of value v
    W = [total] * (n + 1)
    for v in range(1, n + 1):
        pv = pos[v]
        if not pv:
            continue
        prev = 0
        s = 0
        for p in pv:
            g = p - prev - 1
            s += g * (g + 1) // 2
            prev = p
        g = n - prev
        s += g * (g + 1) // 2
        W[v] = s

    ans = 0

    for x in range(1, n + 1):
        px = pos[x]
        if not px:
            continue

        # Count subarrays avoiding both x-1 and x.
        pa = pos[x - 1]
        i = j = 0
        na = len(pa)
        nb = len(px)

        prev = 0
        s = 0

        while i < na and j < nb:
            if pa[i] < px[j]:
                p = pa[i]
                i += 1
            else:
                p = px[j]
                j += 1
            g = p - prev - 1
            s += g * (g + 1) // 2
            prev = p

        while i < na:
            p = pa[i]
            i += 1
            g = p - prev - 1
            s += g * (g + 1) // 2
            prev = p

        while j < nb:
            p = px[j]
            j += 1
            g = p - prev - 1
            s += g * (g + 1) // 2
            prev = p

        g = n - prev
        s += g * (g + 1) // 2

        ans += W[x - 1] - s

    print(ans)

if __name__ == "__main__":
    main()