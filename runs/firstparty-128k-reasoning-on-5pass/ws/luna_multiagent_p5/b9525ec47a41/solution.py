import sys

MOD = 998244353


def build_transitions(spoke):
    trans = [[0] * 4 for _ in range(16)]

    for mask in range(16):
        for d in range(4):
            nxt = 0
            for start in (0, 1):
                for prev in (0, 1):
                    bit = 1 << (2 * start + prev)
                    if not (mask & bit):
                        continue

                    for cur in (0, 1):
                        base = prev + 1 - cur
                        if d == base or (spoke and d == base + 1):
                            nxt |= 1 << (2 * start + cur)
            trans[mask][d] = nxt

    return trans


def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = data[1].decode()

    trans0 = build_transitions(False)
    trans1 = build_transitions(True)

    # Pair (start, current) is encoded by 2 * start + current.
    # Initially current is the cycle edge x_{N-1}, which is also start.
    initial = (1 << 0) | (1 << 3)

    dp = [0] * 16
    dp[initial] = 1

    for ch in s:
        trans = trans1 if ch == '1' else trans0
        ndp = [0] * 16

        # For s_i=0, output degrees are only 0,1,2.
        # For s_i=1, output degrees are 0,1,2,3.
        limit = 4 if ch == '1' else 3

        for mask, ways in enumerate(dp):
            if ways == 0:
                continue
            for d in range(limit):
                nxt = trans[mask][d]
                if nxt:
                    ndp[nxt] = (ndp[nxt] + ways) % MOD

        dp = ndp

    answer = 0
    for mask, ways in enumerate(dp):
        if mask & ((1 << 0) | (1 << 3)):
            answer = (answer + ways) % MOD

    print(answer)


if __name__ == "__main__":
    solve()