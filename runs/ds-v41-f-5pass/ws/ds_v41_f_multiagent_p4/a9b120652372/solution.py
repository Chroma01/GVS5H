import sys

def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    ptr = 1
    out = []
    for _ in range(t):
        n = int(data[ptr]); ptr += 1
        A = data[ptr]; ptr += 1
        B = data[ptr]; ptr += 1
        x = [i + 1 for i in range(n) if A[i] == 49]
        y = [i + 1 for i in range(n) if B[i] == 49]
        M = len(x)
        K = len(y)
        if K > M:
            out.append("-1")
            continue

        G = [x[i + 1] - x[i] for i in range(M - 1)]
        h = [y[j + 1] - y[j] for j in range(K - 1)]

        # unconstrained subsequence matching: exists partition?
        gi = 0
        ok = True
        for j in range(K - 1):
            hj = h[j]
            while gi < M - 1 and G[gi] < hj:
                gi += 1
            if gi >= M - 1:
                ok = False
                break
            gi += 1
        if not ok:
            out.append("-1")
            continue

        P = y[0] - x[0]
        Q = x[-1] - y[-1]
        D = P if P > Q else Q
        R = (x[-1] - x[0]) - (y[-1] - y[0])
        c = 0 if P >= Q else (R & 1)

        def check(s):
            needed = (s + x[0] - y[0]) & 1
            pos = -1
            for j in range(K - 1):
                hj = h[j]
                i = pos + 1
                found = False
                while i < M - 1:
                    gv = G[i]
                    if gv >= hj:
                        if gv > hj or ((x[i] - y[j]) & 1) == needed:
                            found = True
                            break
                    i += 1
                if not found:
                    return False
                pos = i
            return True

        s0 = check(0)
        s1 = check(1)
        if not (s0 or s1):
            out.append("-1")
        elif (c == 0 and s0) or (c == 1 and s1):
            out.append(str(D))
        else:
            out.append(str(D + 1))

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()