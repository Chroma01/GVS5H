import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [0] * (N + 1)
    for i in range(1, N + 1):
        A[i] = int(next(it))
    # Build positions for each value (1-indexed positions)
    pos = [[] for _ in range(N + 1)]
    for i in range(1, N + 1):
        pos[A[i]].append(i)
    total = N * (N + 1) // 2

    # Compute miss[v] for all v
    miss = [0] * (N + 1)
    for v in range(1, N + 1):
        lst = pos[v]
        if not lst:
            miss[v] = total
        else:
            m = 0
            prev = 0
            for p in lst:
                gap = p - prev - 1
                m += gap * (gap + 1) // 2
                prev = p
            gap = N - prev
            m += gap * (gap + 1) // 2
            miss[v] = m

    # sum_distinct = sum over v of (total - miss[v])
    sum_distinct = 0
    for v in range(1, N + 1):
        sum_distinct += total - miss[v]

    # Compute sum_adjacent
    sum_adjacent = 0
    for v in range(1, N):
        lst1 = pos[v]
        lst2 = pos[v + 1]
        # Merge the two sorted lists to compute miss_both
        i1 = 0
        i2 = 0
        prev = 0
        miss_both = 0
        len1 = len(lst1)
        len2 = len(lst2)
        while i1 < len1 and i2 < len2:
            if lst1[i1] < lst2[i2]:
                p = lst1[i1]
                i1 += 1
            else:
                p = lst2[i2]
                i2 += 1
            gap = p - prev - 1
            miss_both += gap * (gap + 1) // 2
            prev = p
        while i1 < len1:
            p = lst1[i1]
            i1 += 1
            gap = p - prev - 1
            miss_both += gap * (gap + 1) // 2
            prev = p
        while i2 < len2:
            p = lst2[i2]
            i2 += 1
            gap = p - prev - 1
            miss_both += gap * (gap + 1) // 2
            prev = p
        gap = N - prev
        miss_both += gap * (gap + 1) // 2

        count = total - miss[v] - miss[v + 1] + miss_both
        sum_adjacent += count

    answer = sum_distinct - sum_adjacent
    print(answer)

if __name__ == "__main__":
    main()