import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = data[1].decode()
    # 0-indexed positions of each '1'
    p = [i for i, c in enumerate(s) if c == '1']
    m = len(p)
    # Transform: b_j = p_j - j
    b = [p[j] - j for j in range(m)]
    # Median minimizes sum of absolute deviations (b is nondecreasing)
    med = b[m // 2]
    ans = 0
    for x in b:
        ans += x - med if x > med else med - x
    sys.stdout.write(str(ans) + "\n")

main()