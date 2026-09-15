import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0]); X = int(data[1]); Y = int(data[2])
    S = data[3].decode(); T = data[4].decode()

    L = X + Y
    # No window of length X+Y exists -> no operation possible.
    if L > N:
        print("Yes" if S == T else "No")
        return

    def build_pref(s):
        p = [0] * (N + 1)
        for i, c in enumerate(s):
            p[i + 1] = p[i] + (1 if c == '1' else 0)
        return p

    def has_move(s, pref):
        # any i with 0^X 1^Y or 1^Y 0^X starting at i
        for i in range(0, N - L + 1):
            if pref[i + X] - pref[i] == 0 and pref[i + L] - pref[i + X] == Y:
                return True
            if pref[i + Y] - pref[i] == Y and pref[i + L] - pref[i + Y] == 0:
                return True
        return False

    pS = build_pref(S)
    pT = build_pref(T)
    # A string with no valid operation is isolated (component = {itself}).
    if (not has_move(S, pS)) or (not has_move(T, pT)):
        print("Yes" if S == T else "No")
        return

    def key(s):
        zeros = tuple(i % Y for i, ch in enumerate(s) if ch == '0')
        ones = tuple(i % X for i, ch in enumerate(s) if ch == '1')
        return (zeros, ones)

    print("Yes" if key(S) == key(T) else "No")

if __name__ == "__main__":
    solve()