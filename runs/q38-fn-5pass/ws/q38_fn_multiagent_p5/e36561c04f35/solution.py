import sys

def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    t = data[0]
    idx = 1
    INF = 10**18
    out = []

    for _ in range(t):
        n = data[idx]
        idx += 1

        # Run-length encoding.
        vals = []
        lens = []

        v = data[idx]
        idx += 1
        length = 1

        for _ in range(n - 1):
            x = data[idx]
            idx += 1
            if x == v:
                length += 1
            else:
                vals.append(v)
                lens.append(length)
                v = x
                length = 1

        vals.append(v)
        lens.append(length)

        m = len(vals)

        # Before processing the current run:
        # p_val  = value of previous run
        # pp_val = value of run before previous
        # a = best cost whose last block value is p_val
        # b = best cost whose last block value is pp_val
        # pend = cost of the special state:
        #        last block value = p_val, size 1, second-last value = current run value
        #
        # Dummy values are smaller than all possible A_i.
        p_val = -1
        pp_val = -2
        a = INF
        b = INF
        pend = INF

        for i in range(m):
            x = vals[i]
            L = lens[i]

            # Start a new last block with value x.
            if i == 0:
                best_start = 0
            else:
                best_start = a if a < b else b
            start = best_start + 1 if best_start < INF else INF

            # Extend an existing last block with value x.
            # This can only be the block whose value is pp_val.
            extend = b if pp_val == x else INF

            # Best cost after this run with last block value x.
            cur = start if start < extend else extend

            # Best cost after this run with last block value p_val.
            # This is possible only by extending the second-last block x
            # through the whole current run.
            prev = pend + L if pend < INF else INF

            # Prepare the special state for the next run.
            # A size-1 last block with value x and second-last value y can be
            # created by starting a new block x from a previous state with last y.
            # This is only needed when the current run has length 1.
            if i + 1 < m and L == 1:
                y = vals[i + 1]
                if y == p_val:
                    best_y = a
                elif y == pp_val:
                    best_y = b
                else:
                    best_y = INF
                pend_next = best_y + 1 if best_y < INF else INF
            else:
                pend_next = INF

            # Shift the window of the last two runs.
            pp_val = p_val
            p_val = x
            b = prev
            a = cur
            pend = pend_next

        out.append(str(a if a < b else b))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()