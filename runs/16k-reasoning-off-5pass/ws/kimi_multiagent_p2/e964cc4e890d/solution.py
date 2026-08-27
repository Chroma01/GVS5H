import sys

MOD = 998244353

def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    s = data[1].strip() if len(data) > 1 else ""
    m = 2 * n

    # Quick necessary conditions.
    if n == 0 or len(s) != m or s[0] != 'B' or s[-1] != 'W':
        print(0)
        return

    bal = 0          # #B - #W in current prefix
    minbal = 0       # minimum prefix balance so far
    ans = 1

    # Process the proper prefix s[1:-1].  The first B and last W are forced:
    # the first B starts the unique "open" black stack, and the last W closes it.
    for ch in s[1:-1]:
        if ch == 'B':
            bal += 1
            if bal < minbal:
                minbal = bal
        else:
            # A W may either be matched to one of the currently open black
            # vertices whose match is still undecided, or be left for a future B.
            # The number of currently open black vertices is bal - minbal.
            open_cnt = bal - minbal
            if open_cnt <= 0:
                print(0)
                return
            ans = (ans * open_cnt) % MOD
            bal -= 1
            if bal < minbal:
                minbal = bal

    # After the forced last W, everything must be closed.  Equivalently the
    # minimum prefix balance over the whole string must be -1 (attained only
    # after the first character), and the total balance must be 0.
    if bal != 1 or minbal != -1:
        print(0)
        return

    print(ans % MOD)

if __name__ == "__main__":
    solve()