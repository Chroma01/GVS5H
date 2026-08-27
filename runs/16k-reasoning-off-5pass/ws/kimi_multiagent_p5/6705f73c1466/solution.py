import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    p = [i for i, c in enumerate(s) if c == '1']
    k = len(p)
    # q[i] = p[i] - i is non-decreasing since p is strictly increasing
    median = p[k // 2] - (k // 2)
    ans = 0
    for i in range(k):
        ans += abs((p[i] - i) - median)
    print(ans)

main()