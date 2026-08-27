import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    # 0-indexed positions of '1'
    p = [i for i, c in enumerate(s) if c == '1']
    k = len(p)
    # q[j] = p[j] - j is non-decreasing since p is strictly increasing
    q = [p[j] - j for j in range(k)]
    m = q[k // 2]  # median
    ans = 0
    for v in q:
        ans += abs(v - m)
    print(ans)

main()