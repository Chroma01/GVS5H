import sys
from collections import deque


def solve_case(vals):
    # run-length encode; only equality of values matters
    rv = []
    rl = []
    for x in vals:
        if rv and rv[-1] == x:
            rl[-1] += 1
        else:
            rv.append(x)
            rl.append(1)
    R = len(rv)

    # stack: index -1 is the LEFTMOST run of the processed suffix
    sval = []
    slen = []
    for i in range(R - 1, -1, -1):
        sval.append(rv[i])
        slen.append(rl[i])
        while len(sval) >= 4:
            # window left->right = sval[-1], sval[-2], sval[-3], sval[-4]
            # a,b,c,d need a.val==c.val, b.val==d.val, len(b)=len(c)=1
            if (sval[-1] == sval[-3] and sval[-2] == sval[-4]
                    and slen[-2] == 1 and slen[-3] == 1):
                a = sval[-1]; al = slen[-1]
                b = sval[-2]; bl = slen[-2]
                cl = slen[-3]
                dl = slen[-4]
                del sval[-4:]
                del slen[-4:]
                # new order (left->right): (a, al+cl), (b, bl+dl)
                sval.append(b); slen.append(bl + dl)
                sval.append(a); slen.append(al + cl)
            else:
                break

    return (R + len(sval)) // 2


def run_verification():
    def brute(max_len, alphabet):
        dist = {(): 0}
        q = deque([()])
        while q:
            s = q.popleft()
            d = dist[s]
            if len(s) >= max_len:
                continue
            for i in range(len(s) - 1):
                t = s[:i] + (s[i + 1], s[i]) + s[i + 2:]
                if t not in dist:
                    dist[t] = d + 1
                    q.append(t)
            for v in alphabet:
                t = s
                for _ in range(max_len - len(s)):
                    t = (v,) + t
                    if t not in dist:
                        dist[t] = d + 1
                        q.append(t)
        return dist

    total_bad = 0
    for alphabet, ml in (([1, 2], 12), ([1, 2, 3], 9)):
        dist = brute(ml, alphabet)
        bad = 0
        for s, b in dist.items():
            if len(s) < 2:
                continue
            g = solve_case(list(s))
            if g != b:
                bad += 1
                if bad <= 5:
                    print("MISMATCH", s, "brute", b, "greedy", g)
        total_bad += bad
        print("alphabet", alphabet, "maxlen", ml, "mismatches", bad)
    print("total mismatches", total_bad)


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        run_verification()
        return
    idx = 0
    T = int(data[idx]); idx += 1
    out = []
    for _ in range(T):
        n = int(data[idx]); idx += 1
        vals = data[idx:idx + n]; idx += n
        out.append(str(solve_case(vals)))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()