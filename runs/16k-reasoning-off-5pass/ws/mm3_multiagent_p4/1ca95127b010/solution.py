import sys

def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    X = int(data[1])
    Y = int(data[2])
    S = data[3].strip()
    T = data[4].strip()
    if S.count('1') != T.count('1'):
        print("No")
        return
    d = X + Y
    INF = 10**9
    min_pref = [0] * d
    cur = 0
    for i, (sc, tc) in enumerate(zip(S, T)):
        if sc == '1':
            cur += 1
        if tc == '1':
            cur -= 1
        # cur is pref[i+1]
        r = (i + 1) % d
        if cur < min_pref[r]:
            min_pref[r] = cur
    # final cur is pref[N]
    # Need pref[N] == 0 (it is because total ones equal)
    # but also each residue's last pref must be 0? Actually final cur is same for all, if it is 0, ok.
    # Check min_pref >= 0
    ok = all(v >= 0 for v in min_pref)
    print("Yes" if ok else "No")

if __name__ == "__main__":
    solve()