import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    a_off = 1
    b_off = 1 + N
    c_off = 1 + 2 * N

    X = []  # A=1, B=0: required negative flip
    Y = []  # A=0, B=1: required positive flip
    D = []  # A=1, B=1: optional off-on pair
    S0 = 0

    for i in range(N):
        a = data[a_off + i]
        b = data[b_off + i]
        c = data[c_off + i]
        if a:
            S0 += c
            if b:
                D.append(c)
            else:
                X.append(c)
        else:
            if b:
                Y.append(c)

    X.sort(reverse=True)
    Y.sort()
    D.sort(reverse=True)

    r = len(X)
    s = len(Y)

    sumN = 0
    Wneg = 0
    for i, c in enumerate(X):
        sumN += c
        Wneg += (r - i) * c

    Wpos = 0
    sumY = 0
    for i, c in enumerate(Y):
        sumY += c
        Wpos += (s - i) * c

    m = r + s
    p = s
    ans = m * S0 - p * sumN - Wneg + Wpos

    k = 0
    sumD_prev = 0
    sumD_gt = 0
    group_count = 0
    prev_c = None

    nx = 0
    sumX_gt = 0
    pos = s
    sumY_lt = sumY
    lenX = r
    lenY = s

    for c in D:
        if c != prev_c:
            sumD_gt = sumD_prev
            group_count = 0
            prev_c = c

        while nx < lenX and X[nx] > c:
            sumX_gt += X[nx]
            nx += 1

        while pos > 0 and Y[pos - 1] >= c:
            pos -= 1
            sumY_lt -= Y[pos]

        Wneg += c + sumX_gt + sumD_gt + c * ((lenX - nx) + group_count)
        Wpos += c + sumY_lt + c * ((lenY - pos) + k)

        sumN += c
        k += 1
        m += 2
        p += 1
        sumD_prev += c
        group_count += 1

        cost = m * S0 - p * sumN - Wneg + Wpos
        if cost < ans:
            ans = cost

    print(ans)

if __name__ == "__main__":
    main()