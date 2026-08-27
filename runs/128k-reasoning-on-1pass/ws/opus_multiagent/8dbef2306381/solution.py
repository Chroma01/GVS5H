import sys

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0]); M = int(data[1]); A = int(data[2]); B = int(data[3])

    full = (1 << B) - 1
    shift = A - 1
    W = (1 << (B - A + 1)) - 1

    if A == B:
        # step is a pure rotate-left by 1 of an A-bit word
        def advance_free(mask, k):
            if mask == 0 or k <= 0:
                return mask
            r = k % A
            if r == 0:
                return mask
            return ((mask << r) | (mask >> (A - r))) & full
    else:
        cache = {}  # mask -> (chain_list, index)  with chain_list[index] == mask

        def advance_free(mask, k):
            while k > 0:
                if mask == 0:
                    return 0
                if mask == full:
                    return full          # full is a fixed point when A < B
                ent = cache.get(mask)
                if ent is None:
                    seq = [mask]
                    local = {mask: 0}
                    m = mask
                    while True:
                        b = 1 if ((m >> shift) & W) else 0
                        m = ((m << 1) | b) & full
                        seq.append(m)
                        if m == 0 or m == full or (m in cache) or (m in local):
                            break
                        local[m] = len(seq) - 1
                    last = seq[-1]
                    if last in local:
                        # cycle inside this chain (should not happen for A<B, safety path)
                        start = local[last]
                        period = (len(seq) - 1) - start
                        if k < start:
                            return seq[k]
                        return seq[start + ((k - start) % period)]
                    for i in range(len(seq) - 1):
                        mm = seq[i]
                        if mm not in cache:
                            cache[mm] = (seq, i)
                    ent = cache[mask]
                lst, idx = ent
                avail = len(lst) - 1 - idx
                if k <= avail:
                    return lst[idx + k]
                k -= avail
                mask = lst[-1]
            return mask

    def advance_bad(mask, length):
        if length >= B:
            return 0
        return (mask << length) & full

    x = 1
    mask = 1
    ok = True

    pos = 4
    for _ in range(M):
        L = int(data[pos]); R = int(data[pos + 1]); pos += 2
        if not ok:
            continue
        free_len = L - 1 - x
        if free_len > 0:
            mask = advance_free(mask, free_len)
            if mask == 0:
                ok = False
                x = R
                continue
        x = L - 1
        mask = advance_bad(mask, R - L + 1)
        x = R
        if mask == 0:
            ok = False
            continue

    if not ok:
        sys.stdout.write("No\n")
        return

    rem = N - x
    if rem > 0:
        mask = advance_free(mask, rem)

    sys.stdout.write("Yes\n" if (mask & 1) else "No\n")

main()