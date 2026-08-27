import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    q = []
    i = 0
    for idx, ch in enumerate(s):
        if ch == '1':
            q.append(idx - i)
            i += 1
    q.sort()
    m = q[len(q) // 2]
    ans = 0
    for v in q:
        ans += abs(v - m)
    sys.stdout.write(str(ans) + "\n")

main()