import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))

    # positions[v] = list of 1-indexed positions where value v occurs
    positions = [[] for _ in range(n + 2)]
    for i, x in enumerate(A, 1):
        positions[x].append(i)

    total_sub = n * (n + 1) // 2

    # total1 = sum over values v of (# subarrays containing v)
    total1 = 0
    for v in range(1, n + 1):
        ps = positions[v]
        if not ps:
            continue
        avoid = 0
        prev = 0
        for p in ps:
            g = p - prev - 1
            avoid += g * (g + 1) // 2
            prev = p
        g = n - prev
        avoid += g * (g + 1) // 2
        total1 += total_sub - avoid

    # total2 = sum over v>=2 of (# subarrays containing both v-1 and v)
    # For a pair (a,b): cnt = sum_{R=1..N} min(last_a(R), last_b(R))
    # computed by walking merged event positions.
    # At each event position pos:
    #   - the OLD min applies to R in (prev, pos), i.e. (pos - prev - 1) points
    #   - after updating la/lb, the NEW min applies at R = pos itself (+m_new)
    #   - subsequent points are handled by the next segment / tail.
    total2 = 0
    for v in range(2, n + 1):
        pa = positions[v - 1]
        pb = positions[v]
        if not pa or not pb:
            continue
        la = 0
        lb = 0
        i = 0
        j = 0
        prev = 0
        lena = len(pa)
        lenb = len(pb)
        cnt = 0
        while i < lena or j < lenb:
            if j >= lenb or (i < lena and pa[i] <= pb[j]):
                pos = pa[i]
                i += 1
                m = la if la < lb else lb
                cnt += m * (pos - prev - 1)
                la = pos
                m = la if la < lb else lb
                cnt += m
            else:
                pos = pb[j]
                j += 1
                m = la if la < lb else lb
                cnt += m * (pos - prev - 1)
                lb = pos
                m = la if la < lb else lb
                cnt += m
            prev = pos
        # tail segment after last event
        m = la if la < lb else lb
        cnt += m * (n - prev)
        total2 += cnt

    print(total1 - total2)

main()