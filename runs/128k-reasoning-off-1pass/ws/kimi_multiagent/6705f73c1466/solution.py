import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    pos = [i for i, ch in enumerate(s) if ch == '1']
    k = len(pos)
    q = [pos[j] - j for j in range(k)]
    m = q[k // 2]
    ans = 0
    for v in q:
        ans += abs(v - m)
    print(ans)

main()