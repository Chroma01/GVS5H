import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    q = []
    for i, ch in enumerate(s):
        if ch == '1':
            q.append(i - len(q))
    k = len(q)
    med = q[k // 2]
    ans = 0
    for v in q:
        ans += v - med if v >= med else med - v
    sys.stdout.write(str(ans) + "\n")

main()