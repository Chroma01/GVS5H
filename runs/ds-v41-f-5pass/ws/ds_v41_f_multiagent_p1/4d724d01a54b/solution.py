import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    P = list(map(int, data[1:1 + n]))

    tree = [0] * (n + 1)

    def add(i):
        while i <= n:
            tree[i] += 1
            i += i & (-i)

    def pref(i):
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & (-i)
        return s

    ans = 0
    seen = 0
    for idx, v in enumerate(P):
        p = idx + 1
        le = pref(v)          # already seen values <= v
        I = seen - le         # larger values already seen (to the left)
        # v walks left across boundaries p-1, p-2, ..., p-I
        ans += I * p - I * (I + 1) // 2
        add(v)
        seen += 1

    sys.stdout.write(str(ans) + "\n")


main()