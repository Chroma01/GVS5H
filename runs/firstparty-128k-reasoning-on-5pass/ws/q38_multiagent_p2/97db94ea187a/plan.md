```python
import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    MOD = int(data[1])

    half = N // 2
    half1 = half + 1
    N1 = N + 1
    Emax = N * (N - 1) // 2
    C2 = [i * (i - 1) // 2 for i in range(N1)]

    # finish0/1[s][e]: can a state with s vertices, e even vertices,
    # and last layer parity 0/1 still reach (N, half)?
    finish0 = [[False] * half1 for _ in range(N1)]
    finish1 = [[False] * half1 for _ in range(N1)]
    finish0[N][half] = True
    finish1[N][half] = True
    for s in range(N - 1, 0, -1):
        maxb = N - s
        for e in range(half1):
            lim = maxb
            lim2 = half - (s - e)
            if lim2 < lim:
                lim = lim2
            if lim >= 1:
                for b in range(1, lim + 1):
                    if finish1[s + b][e]:
                        finish0[s][e] = True
                        break

            lim = maxb
            lim2 = half - e
            if lim2 < lim:
                lim = lim2
            if lim >= 1:
                for b in range(1, lim + 1):
                    if finish0[s + b][e + b]:
                        finish1[s][e] = True
                        break

    # possible last-layer sizes for each (s, e, parity)
    poss0 = [[[False] * N1 for _ in range(half1)] for _ in range(N1)]
    poss1 = [[[False] * N1 for _ in range(half1)] for _ in range(N1)]
    poss0[1][1][1] = True

    for s in range(1, N):
        maxb = N - s
        for e in range(half1):
            row0 = poss0[s][e]
            row1 = poss1[s][e]

            lim = maxb
            lim2 = half - (s - e)
            if lim2 < lim:
                lim = lim2
            if lim >= 1:
                for a in range(1, s + 1):
                    if row0[a]:
                        for b in range(1, lim + 1):
                            if finish1[s + b][e]:
                                poss1[s + b][e][b] = True

            lim = maxb
            lim2 = half - e
            if lim2 < lim:
                lim = lim2
            if lim >= 1:
                for a in range(1, s + 1):
                    if row1[a]:
                        for b in range(1, lim + 1):
                            if finish0[s + b][e + b]:
                                poss0[s + b][e + b][b] = True

    a_list0 = [[() for _ in range(half1)] for _ in range(N1)]
    a_list1 = [[() for _ in range(half1)] for _ in range(N1)]
    union_a = [[() for _ in range(half1)] for _ in range(N1)]

    for s in range(1, N1):
        for e in range(half1):
            l0 = tuple(a for a in range(1, s + 1) if poss0[s][e][a])
            l1 = tuple(a for a in range(1, s + 1) if poss1[s][e][a])
            a_list0[s][e] = l0
            a_list1[s][e] = l1
            if l0 and l1:
                union_a[s][e] = tuple(sorted(set(l0) | set(l1)))

    # Precompute transitions: for each s and next layer size b,
    # which e values need both parities, only even-source, only odd-source.
    trans_s = [[] for _ in range(N1)]
    for s in range(1, N):
        lst = []
        maxb = N - s
        for b in range(1, maxb + 1):
            sb = s + b
            both = []
            p0 = []
            p1 = []
            for e in range(half1):
                can0 = bool(a_list0[s][e]) and finish1[sb][e]
                if e + b <= half:
                    can1 = bool(a_list1[s][e]) and finish0[sb][e + b]
                else:
                    can1 = False

                if can0 and can1:
                    both.append((e, union_a[s][e]))
                elif can0:
                    p0.append((e, a_list0[s][e]))
                elif can1:
                    p1.append((e, a_list1[s][e]))

            if both or p0 or p1:
                lst.append((b, sb, both, p0, p1))
        trans_s[s] = lst

    # Maximum possible number of edges (polynomial degree).
    neg = -10**9
    max0 = [[[neg] * N1 for _ in range(half1)] for _ in ran