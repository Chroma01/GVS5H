import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); X = int(data[1]); Y = int(data[2])
    S = data[3]; T = data[4]

    if len(S) != len(T):
        sys.stdout.write("No\n")
        return

    try:
        import numpy as np
        s = np.frombuffer(S, dtype=np.uint8)
        t = np.frombuffer(T, dtype=np.uint8)
        s1 = (s == 49)          # positions of '1'
        t1 = (t == 49)
        if int(s1.sum()) != int(t1.sum()):
            sys.stdout.write("No\n")
            return
        # z_j = number of zeros before the j-th one  (inclusive cumsum of zeros at a '1' position)
        cs0 = np.cumsum(~s1)
        ct0 = np.cumsum(~t1)
        zs = cs0[s1] % X
        zt = ct0[t1] % X
        if not np.array_equal(zs, zt):
            sys.stdout.write("No\n")
            return
        # o_i = number of ones before the i-th zero
        cs1 = np.cumsum(s1)
        ct1 = np.cumsum(t1)
        os_ = cs1[~s1] % Y
        ot_ = ct1[~t1] % Y
        if not np.array_equal(os_, ot_):
            sys.stdout.write("No\n")
            return
        sys.stdout.write("Yes\n")
        return
    except Exception:
        pass

    # pure-python fallback
    def calc(B, X, Y):
        z = []
        o = []
        za = z.append
        oa = o.append
        zeros = 0
        ones = 0
        for c in B:
            if c == 49:
                za(zeros % X)
                ones += 1
            else:
                oa(ones % Y)
                zeros += 1
        return z, o

    zs, os_ = calc(S, X, Y)
    zt, ot_ = calc(T, X, Y)
    if len(zs) != len(zt) or zs != zt or os_ != ot_:
        sys.stdout.write("No\n")
    else:
        sys.stdout.write("Yes\n")

main()