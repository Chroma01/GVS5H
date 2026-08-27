import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    # data[0] = N, data[1] = S  (guard in case N line missing)
    if len(data) >= 2:
        s = data[1]
    else:
        s = data[0]
    try:
        import numpy as np
        a = np.frombuffer(s, dtype=np.uint8)
        p = np.flatnonzero(a == 49).astype(np.int64)
        if p.size == 0:
            print(0)
            return
        b = p - np.arange(p.size, dtype=np.int64)
        m = b[b.size // 2]
        print(int(np.abs(b - m).sum()))
    except Exception:
        # pure-Python fallback
        pos = []
        ap = pos.append
        idx = 0
        for ch in s:
            if ch == 49 or ch == '1':
                ap(idx)
            idx += 1
        k = len(pos)
        if k == 0:
            print(0)
            return
        b = [pos[j] - j for j in range(k)]
        m = b[k // 2]
        total = 0
        for v in b:
            d = v - m
            total += d if d >= 0 else -d
        print(total)

main()