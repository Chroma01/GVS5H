import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    S = data[2]

    s_idx = [ord(ch) - 97 for ch in S]
    size = 1 << N

    # trans[mask][c] = next mask after appending character c
    trans = [[0] * 26 for _ in range(size)]

    for mask in range(size):
        row = [0] * (N + 1)
        for i in range(1, N + 1):
            row[i] = row[i - 1] + ((mask >> (i - 1)) & 1)

        for c in range(26):
            nrow = [0] * (N + 1)
            for i in range(1, N + 1):
                v = row[i]
                if nrow[i - 1] > v:
                    v = nrow[i - 1]
                if s_idx[i - 1] == c:
                    t = row[i - 1] + 1
                    if t > v:
                        v = t
                nrow[i] = v

            nmask = 0
            for i in range(1, N + 1):
                if nrow[i] > nrow[i - 1]:
                    nmask |= 1 << (i - 1)
            trans[mask][c] = nmask

    cnt = [0] * size
    cnt[0] = 1

    for _ in range(M):
        nxt = [0] * size
        for mask in range(size):
            val = cnt[mask]
            if val == 0:
                continue
            tr = trans[mask]
            for nmask in tr:
                nxt[nmask] = (nxt[nmask] + val) % MOD
        cnt = nxt

    ans = [0] * (N + 1)
    for mask in range(size):
        val = cnt[mask]
        if val:
            k = bin(mask).count("1")
            ans[k] = (ans[k] + val) % MOD

    print(" ".join(map(str, ans)))

if __name__ == "__main__":
    main()