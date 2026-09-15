import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = data[1] if len(data) > 1 else b""

    # a_j = p_j - j - 1 + 1 = p_j - j, where p_j is the 1-indexed position
    # of the j-th one (j 0-indexed). This equals (i+1) - idx for 0-indexed i.
    a = []
    idx = 0
    for i, c in enumerate(s):
        if c == 49:  # ord('1')
            a.append(i + 1 - idx)
            idx += 1

    k = idx
    if k <= 1:
        print(0)
        return

    # Minimize sum |a_j - L| over the block start L; the median is optimal.
    med = a[k // 2]
    ans = 0
    for x in a:
        ans += abs(x - med)
    print(ans)

main()