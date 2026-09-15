import sys


def check(X, mode, a, b, k, m):
    # Is there a partition of a[] into m consecutive nonempty groups mapped in
    # order onto b[], with every token displacement <= X, every boundary gap
    # a[r+1]-a[r] >= b[q+1]-b[q], and every FROZEN boundary (equality) having
    # displacement parity == mode (mode < 0 forbids frozen boundaries entirely).
    lo = b[0] - X
    i_low = 0
    while i_low < k and a[i_low] < lo:
        i_low += 1
    hi = b[0] + X
    j_high = -1
    while j_high + 1 < k and a[j_high + 1] <= hi:
        j_high += 1
    Low_cur = i_low
    High_cur = j_high
    L = 0
    r = 0
    km = k - m
    for q in range(m - 1):
        bq1 = b[q + 1]
        lo = bq1 - X
        while i_low < k and a[i_low] < lo:
            i_low += 1
        Low_next = i_low
        hi = bq1 + X
        j = j_high + 1
        while j < k and a[j] <= hi:
            j += 1
        j_high = j - 1
        High_next = j_high

        if L < Low_cur:
            return False
        start = L
        x = Low_next - 1
        if x > start:
            start = x
        UB = High_cur
        x = High_next - 1
        if x < UB:
            UB = x
        x = km + q
        if x < UB:
            UB = x
        if start > UB:
            return False
        if r < start:
            r = start
        gb = bq1 - b[q]
        bq = b[q]
        prev = a[r]
        while r <= UB:
            nxt = a[r + 1]
            g = nxt - prev
            if g < gb:
                prev = nxt
                r += 1
                continue
            if g == gb and (mode < 0 or ((bq - prev) & 1) != mode):
                prev = nxt
                r += 1
                continue
            break
        else:
            return False
        L = r + 1
        r = L
        Low_cur = Low_next
        High_cur = High_next

    if L < Low_cur or High_cur < k - 1:
        return False
    return True


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    pos = 1
    out = []
    for _ in range(t):
        pos += 1  # skip N
        A = data[pos]; pos += 1
        B = data[pos]; pos += 1
        a = [i for i, c in enumerate(A) if c == 49]
        b = [i for i, c in enumerate(B) if c == 49]
        k = len(a); m = len(b)
        if m > k or a[-1] - a[0] < b[-1] - b[0]:
            out.append("-1")
            continue
        d1 = b[0] - a[0]
        if d1 < 0:
            d1 = -d1
        d2 = b[-1] - a[-1]
        if d2 < 0:
            d2 = -d2
        Lb = d1 if d1 > d2 else d2
        p = Lb & 1
        if check(Lb, p, a, b, k, m):
            out.append(str(Lb))
        elif check(Lb, 1 - p, a, b, k, m):
            out.append(str(Lb + 1))
        else:
            out.append("-1")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()