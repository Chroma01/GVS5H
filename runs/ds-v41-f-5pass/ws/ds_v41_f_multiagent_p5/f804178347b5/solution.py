import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    s = b''.join(data[1:]).decode()
    L = 3 ** N

    try:
        import numpy as np
    except ImportError:
        np = None

    if np is not None:
        # v: current level values (0/1), f: min flips to flip current value
        v = np.frombuffer(s.encode(), dtype=np.uint8).astype(np.int64) - 48
        f = np.ones(v.size, dtype=np.int64)
        while v.size > 1:
            va = v[0::3]
            vb = v[1::3]
            vc = v[2::3]
            # majority of each triple
            nv = ((va + vb + vc) >= 2).astype(np.int64)
            t = 1 - nv  # value children must reach to flip this node
            fa = f[0::3]
            fb = f[1::3]
            fc = f[2::3]
            ca = np.where(va == t, 0, fa)
            cb = np.where(vb == t, 0, fb)
            cc = np.where(vc == t, 0, fc)
            # need at least 2 children at target -> sum of two smallest costs
            f = ca + cb + cc - np.maximum(ca, np.maximum(cb, cc))
            v = nv
        print(int(f[0]))
        return

    # Pure Python fallback
    v = [1 if ch == '1' else 0 for ch in s]
    f = [1] * L
    while len(v) > 1:
        nv = []
        nf = []
        ap = nv.append
        af = nf.append
        for i in range(0, len(v), 3):
            a = v[i]; b = v[i + 1]; c = v[i + 2]
            mv = 1 if a + b + c >= 2 else 0
            t = 1 - mv
            ca = 0 if a == t else f[i]
            cb = 0 if b == t else f[i + 1]
            cc = 0 if c == t else f[i + 2]
            mx = ca if ca > cb else cb
            if cc > mx:
                mx = cc
            ap(mv)
            af(ca + cb + cc - mx)
        v = nv
        f = nf
    print(f[0])


main()