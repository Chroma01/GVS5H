import sys

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    MAX = 500000
    # difference array for coverage counts
    diff = [0] * (MAX + 3)  # indices up to MAX+2 inclusive
    for _ in range(N):
        L = int(next(it))
        R = int(next(it))
        diff[L] += 1
        if R + 1 <= MAX + 2:
            diff[R + 1] -= 1
    # prefix sum to get c[y] = number of intervals covering rating y
    c = [0] * (MAX + 3)
    cur = 0
    for i in range(1, MAX + 3):
        cur += diff[i]
        c[i] = cur
    # final[y] = final rating starting from y
    final = [0] * (MAX + 3)
    # base case for y = MAX+1 (sentinel)
    final[MAX + 1] = MAX + 1
    # compute from MAX down to 1
    for y in range(MAX, 0, -1):
        if c[y] == 0:
            final[y] = y
        else:
            nxt = y + c[y]
            # nxt is at most MAX+1 because c[y] >= 1 and y <= MAX
            final[y] = final[nxt]
    Q = int(next(it))
    out_lines = []
    for _ in range(Q):
        X = int(next(it))
        out_lines.append(str(final[X]))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()