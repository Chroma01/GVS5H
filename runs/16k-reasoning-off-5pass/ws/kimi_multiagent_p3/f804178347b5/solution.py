import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    # Bits may be space-separated or one contiguous string; concatenate all remaining tokens.
    s = b"".join(data[1:])
    m = 3 ** n
    # Leaf costs: cost to make leaf 0 / 1.
    c0 = [0] * m
    c1 = [0] * m
    for i in range(m):
        if s[i] == 49:  # '1'
            c0[i] = 1
        else:
            c1[i] = 1
    # Fold level by level; also track current majority values.
    vals = [1 if s[i] == 49 else 0 for i in range(m)]
    length = m
    for _ in range(n):
        new_len = length // 3
        n0 = [0] * new_len
        n1 = [0] * new_len
        nv = [0] * new_len
        for i in range(new_len):
            j = 3 * i
            # cost to force 1: sum of two smallest c1 among children
            a, b, c = c1[j], c1[j + 1], c1[j + 2]
            n1[i] = a + b + c - max(a, b, c)
            # cost to force 0: sum of two smallest c0 among children
            a, b, c = c0[j], c0[j + 1], c0[j + 2]
            n0[i] = a + b + c - max(a, b, c)
            # current majority value
            nv[i] = 1 if (vals[j] + vals[j + 1] + vals[j + 2]) >= 2 else 0
        c0, c1, vals = n0, n1, nv
        length = new_len
    root_val = vals[0]
    # Cost to flip the root's output.
    ans = c0[0] if root_val == 1 else c1[0]
    sys.stdout.write(str(ans) + "\n")

main()