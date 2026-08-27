import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    # 0-indexed positions of '1'
    pos = [i for i, ch in enumerate(s) if ch == '1']
    k = len(pos)
    # q_j = p_j - j is non-decreasing; median minimizes sum of abs deviations
    q = [p - j for j, p in enumerate(pos)]
    m = q[k // 2]
    ans = 0
    for v in q:
        ans += abs(v - m)
    print(ans)

main()