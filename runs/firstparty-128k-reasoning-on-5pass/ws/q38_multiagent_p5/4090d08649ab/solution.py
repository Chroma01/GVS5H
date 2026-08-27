import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    n = data[0]
    pos = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        pos[data[i]].append(i)
    del data

    ans = 0
    for x in range(1, n + 1):
        p = pos[x]
        if not p:
            continue
        b = pos[x - 1]
        idx = 0
        lp = len(p)
        prev = 0

        for blocker in b:
            left = prev + 1
            right = blocker - 1
            if left <= right:
                while idx < lp and p[idx] < left:
                    idx += 1
                if idx < lp and p[idx] <= right:
                    m = right - left + 1
                    total = m * (m + 1) // 2
                    no = 0
                    start = left
                    while idx < lp and p[idx] <= right:
                        px = p[idx]
                        seg = px - start
                        no += seg * (seg + 1) // 2
                        start = px + 1
                        idx += 1
                    seg = right - start + 1
                    no += seg * (seg + 1) // 2
                    ans += total - no
            prev = blocker

        left = prev + 1
        right = n
        if left <= right:
            while idx < lp and p[idx] < left:
                idx += 1
            if idx < lp and p[idx] <= right:
                m = right - left + 1
                total = m * (m + 1) // 2
                no = 0
                start = left
                while idx < lp and p[idx] <= right:
                    px = p[idx]
                    seg = px - start
                    no += seg * (seg + 1) // 2
                    start = px + 1
                    idx += 1
                seg = right - start + 1
                no += seg * (seg + 1) // 2
                ans += total - no

    print(ans)

if __name__ == "__main__":
    main()