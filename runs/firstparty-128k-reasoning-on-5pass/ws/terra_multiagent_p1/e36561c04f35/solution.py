import sys

def solve_case(a):
    vals = []
    lens = []

    for x in a:
        if vals and vals[-1] == x:
            lens[-1] += 1
        else:
            vals.append(x)
            lens.append(1)

    m = len(vals)
    reductions = 0
    i = 0

    while i + 3 < m:
        if (vals[i] == vals[i + 2] and
                vals[i + 1] == vals[i + 3] and
                lens[i + 1] == 1 and
                lens[i + 2] == 1):
            reductions += 1
            # The two middle runs are consumed. The next compatible
            # reduction may start at i+3, sharing the right outer run.
            i += 3
        else:
            i += 1

    return m - reductions

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    p = 1
    ans = []

    for _ in range(t):
        n = data[p]
        p += 1
        a = data[p:p + n]
        p += n
        ans.append(str(solve_case(a)))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    main()