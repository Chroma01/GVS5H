import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])

    # Hull lines are stored by their building coordinates/heights.
    # start_num / start_den is the height where this hull line becomes
    # the maximum of the upper envelope.
    xs = []
    hs = []
    start_num = []
    start_den = []

    # Best non-negative blocking height, stored exactly as best_num / best_den.
    best_num = -1
    best_den = 1

    idx = 1
    for _ in range(n):
        x = int(data[idx])
        h = int(data[idx + 1])
        idx += 2

        # Insert line L(h) = (h - H) / X?  Here line for building (x,h) is
        # (h - observer_height) / x.  Slopes -1/x are strictly increasing.
        #
        # Remove last hull line if the new line intersects it not to the right
        # of where that last line became active.
        while len(xs) >= 2:
            x_last = xs[-1]
            h_last = hs[-1]

            # intersection(last, new) <= start(last)
            # intersection(last, new) =
            #   (h_last * x - h * x_last) / (x - x_last)
            if (h_last * x - h * x_last) * start_den[-1] <= start_num[-1] * (x - x_last):
                xs.pop()
                hs.pop()
                start_num.pop()
                start_den.pop()
            else:
                break

        if xs:
            x_last = xs[-1]
            h_last = hs[-1]

            # First height where this new building becomes visible.
            # At this height it is still blocked by equality, so it is a
            # candidate answer if non-negative.
            num = h_last * x - h * x_last
            den = x - x_last

            if num >= 0:
                if best_num < 0 or num * best_den > best_num * den:
                    best_num = num
                    best_den = den

            new_start_num = num
            new_start_den = den
        else:
            # First building has no blocker. Its start value is never used
            # while the hull has at least two lines.
            new_start_num = 0
            new_start_den = 1

        xs.append(x)
        hs.append(h)
        start_num.append(new_start_num)
        start_den.append(new_start_den)

    if best_num < 0:
        sys.stdout.write("-1\n")
    else:
        sys.stdout.write(f"{best_num / best_den:.18f}\n")

if __name__ == "__main__":
    solve()