import sys

MOD = 998244353

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    s = data[1]

    # Bit encoding of a relation on {0,1}:
    # bit 0: 0->0, bit 1: 0->1, bit 2: 1->0, bit 3: 1->1
    #
    # For s_i = 0, possible degree labels 0,1,2 give relations:
    labels0 = (2, 9, 4)
    # For s_i = 1, possible degree labels 0,1,2,3 give relations:
    labels1 = (2, 11, 13, 4)

    # comp[m][t] = composition m ; t
    comp = [[0] * 16 for _ in range(16)]
    for m in range(16):
        for t in range(16):
            res = 0
            for p in range(2):
                for q in range(2):
                    if (m >> (p * 2 + q)) & 1:
                        if (t >> (q * 2)) & 1:
                            res |= 1 << (p * 2)
                        if (t >> (q * 2 + 1)) & 1:
                            res |= 1 << (p * 2 + 1)
            comp[m][t] = res

    # Build sparse transition edges:
    # (from_mask, to_mask, multiplicity), where multiplicity is the number
    # of distinct degree labels producing this transition.
    edges = [[], []]
    for c, labels in enumerate((labels0, labels1)):
        for m in range(16):
            cnt = {}
            for t in labels:
                nm = comp[m][t]
                if nm:
                    cnt[nm] = cnt.get(nm, 0) + 1
            for nm, mult in cnt.items():
                edges[c].append((m, nm, mult))

    # Table by byte value of the input character.
    edge_table = [()] * 256
    edge_table[48] = tuple(edges[0])  # '0'
    edge_table[49] = tuple(edges[1])  # '1'

    # Initial relation is identity: mask 9 = bits 0 and 3.
    dp = [0] * 16
    dp[9] = 1
    ndp = [0] * 16
    zero = [0] * 16

    # Reduce modulo periodically to keep integers small while avoiding
    # 16 modulo operations per character.
    cnt = 0
    et = edge_table
    for ch in s:
        ndp[:] = zero
        for m, nm, mult in et[ch]:
            ndp[nm] += dp[m] * mult
        dp, ndp = ndp, dp

        cnt += 1
        if cnt == 16:
            dp = [x % MOD for x in dp]
            cnt = 0

    ans = 0
    for m in range(16):
        if m & 9:  # contains (0,0) or (1,1)
            ans += dp[m]
    print(ans % MOD)

if __name__ == "__main__":
    solve()