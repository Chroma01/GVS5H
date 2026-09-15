import sys
from bisect import bisect_left


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    out = sys.stdout.write

    a_vals = data[1:1 + n]
    b_vals = data[1 + n:1 + 2 * n]

    cnt_a = {}
    cnt_b = {}
    fa = fb = 0
    max_a = max_b = -1

    for x in a_vals:
        if x != -1:
            fa += 1
            cnt_a[x] = cnt_a.get(x, 0) + 1
            if x > max_a:
                max_a = x

    for x in b_vals:
        if x != -1:
            fb += 1
            cnt_b[x] = cnt_b.get(x, 0) + 1
            if x > max_b:
                max_b = x

    # Minimum number of fixed-fixed pairs that must be made.
    t = fa + fb - n

    if t <= 0:
        out("Yes\n")
        return

    if not cnt_a or not cnt_b or t > fa or t > fb:
        out("No\n")
        return

    # One fixed-fixed pair is always enough: pair a global maximum
    # with any fixed value on the other side.
    if t == 1:
        out("Yes\n")
        return

    max_s = max_a if max_a > max_b else max_b

    # If one value pair alone can supply all required pairs.
    heavy_a = -1
    for x, c in cnt_a.items():
        if c >= t and x > heavy_a:
            heavy_a = x

    heavy_b = -1
    for x, c in cnt_b.items():
        if c >= t and x > heavy_b:
            heavy_b = x

    if heavy_a != -1 and heavy_b != -1 and heavy_a + heavy_b >= max_s:
        out("Yes\n")
        return

    # Enumerate weighted pair sums.  Use the smaller unique side outside.
    if len(cnt_a) <= len(cnt_b):
        outer = cnt_a
        inner = cnt_b
    else:
        outer = cnt_b
        inner = cnt_a

    inner_items = sorted(inner.items())
    inner_vals = [v for v, _ in inner_items]
    inner_counts = [c for _, c in inner_items]
    m = len(inner_vals)

    # Pack (sum, weight) into one integer.
    # weight <= n < 2^shift, so lower bits never carry into the sum bits.
    shift = max(1, n.bit_length())
    inner_shift = [v << shift for v in inner_vals]

    bl = bisect_left
    prepared = []
    for x, c in outer.items():
        start = bl(inner_vals, max_s - x)
        if start < m:
            prepared.append((x << shift, c, start))

    if not prepared:
        out("No\n")
        return

    # If only one value on either side can participate, valid sums cannot
    # collide, and the heavy-pair check above already handled single-pair wins.
    if len(prepared) == 1 or m == 1:
        out("No\n")
        return

    arr = [
        x_shift + inner_shift[j] + (c if c < inner_counts[j] else inner_counts[j])
        for x_shift, c, start in prepared
        for j in range(start, m)
    ]

    if not arr:
        out("No\n")
        return

    arr.sort()

    mask = (1 << shift) - 1
    prev_sum = -1
    total = 0

    for v in arr:
        s = v >> shift
        if s != prev_sum:
            prev_sum = s
            total = 0
        total += v & mask
        if total >= t:
            out("Yes\n")
            return

    out("No\n")


if __name__ == "__main__":
    solve()