import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    ptr = 1
    out = []
    for _ in range(t):
        n = data[ptr]; ptr += 1
        # compress into maximal runs (value, size)
        rv = []
        rs = []
        prev = -1
        for k in range(n):
            v = data[ptr + k]
            if v == prev:
                rs[-1] += 1
            else:
                rv.append(v)
                rs.append(1)
                prev = v
        ptr += n
        R = len(rv)

        # stack of runs; reduce top4 whenever it forms a,b,a,b
        # with both middle runs of size 1
        sv = []
        ss = []
        cnt = 0
        for i in range(R):
            sv.append(rv[i])
            ss.append(rs[i])
            while len(sv) >= 4:
                l = len(sv)
                if (sv[l - 4] == sv[l - 2] and sv[l - 3] == sv[l - 1]
                        and ss[l - 3] == 1 and ss[l - 2] == 1):
                    n1v = sv[l - 4]
                    n1s = ss[l - 4] + ss[l - 2]
                    n2v = sv[l - 3]
                    n2s = ss[l - 3] + ss[l - 1]
                    # remove the last four runs
                    sv.pop(); sv.pop(); sv.pop(); sv.pop()
                    ss.pop(); ss.pop(); ss.pop(); ss.pop()
                    sv.append(n1v); ss.append(n1s)
                    sv.append(n2v); ss.append(n2s)
                    cnt += 1
                else:
                    break
        # answer = initial number of runs - maximum number of -2 reductions
        out.append(str(R - cnt))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()