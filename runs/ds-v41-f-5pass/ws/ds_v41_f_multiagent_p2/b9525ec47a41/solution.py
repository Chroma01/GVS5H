import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    s = data[1]  # bytes
    MOD = 998244353

    # Flat transition lists (src, dst). Duplicates encode multiplicities.
    flat0 = [(1,2),(1,1),(1,3),(2,2),(2,6),(3,8),(3,3),(4,2),(4,4),(4,10),
             (5,12),(5,5),(5,3),(6,2),(6,6),(7,2),(7,7),(7,6),(8,8),(8,3),
             (9,8),(9,9),(9,3),(10,12),(10,10),(11,12),(11,11),(11,10),(12,12),(12,10)]
    flat1 = [(1,2),(1,4),(1,5),(1,3),(2,2),(2,7),(2,6),(3,8),(3,9),(3,3),
             (4,2),(4,4),(4,11),(4,10),(5,12),(5,11),(5,5),(5,3),(6,2),(6,7),
             (6,6),(7,2),(7,7),(7,7),(7,6),(8,8),(8,9),(8,3),(9,8),(9,9),
             (9,9),(9,3),(10,12),(10,11),(10,10),(11,12),(11,11),(11,11),(11,10),
             (12,12),(12,11),(12,10)]

    # Build adjacency grouped by source
    adj0 = [[] for _ in range(13)]
    for a, b in flat0:
        adj0[a].append(b)
    adj1 = [[] for _ in range(13)]
    for a, b in flat1:
        adj1[a].append(b)

    # dp over 13 states; start at state 1 = (S0={0}, S1={1})
    dp = [0] * 13
    dp[1] = 1

    for ch in s:
        adj = adj1 if ch == 49 else adj0  # 49 = ord('1')
        ndp = [0] * 13
        for a in range(1, 13):
            v = dp[a]
            if v:
                av = adj[a]
                for b in av:
                    ndp[b] += v
        dp = [x % MOD for x in ndp]

    # Accepting states: 0∈S0 or 1∈S1
    ans = 0
    for i in (1, 4, 5, 6, 7, 8, 9, 10, 11, 12):
        ans += dp[i]
    sys.stdout.write(str(ans % MOD) + "\n")

main()