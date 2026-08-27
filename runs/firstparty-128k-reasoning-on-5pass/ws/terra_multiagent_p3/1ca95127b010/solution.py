import sys

def solve():
    input = sys.stdin.readline

    N, X, Y = map(int, input().split())
    S = input().strip()
    T = input().strip()

    if S.count('0') != T.count('0'):
        print("No")
        return

    zero_s = []
    zero_t = []
    one_s = []
    one_t = []

    for i, c in enumerate(S):
        if c == '0':
            zero_s.append(i % Y)
        else:
            one_s.append(i % X)

    for i, c in enumerate(T):
        if c == '0':
            zero_t.append(i % Y)
        else:
            one_t.append(i % X)

    print("Yes" if zero_s == zero_t and one_s == one_t else "No")

if __name__ == "__main__":
    solve()