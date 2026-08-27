import sys

MOD = 998244353

def compose(a, b):
    """Boolean relation composition, with bit (2*x+y) representing x -> y."""
    r = 0
    if a & 1:  # 0 -> 0
        if b & 1:
            r |= 1
        if b & 2:
            r |= 2
    if a & 2:  # 0 -> 1
        if b & 4:
            r |= 1
        if b & 8:
            r |= 2
    if a & 4:  # 1 -> 0
        if b & 1:
            r |= 4
        if b & 2:
            r |= 8
    if a & 8:  # 1 -> 1
        if b & 4:
            r |= 4
        if b & 8:
            r |= 8
    return r

# Local relations indexed by the degree at the ordinary vertex.
# For s_i = 0:
# d = 0,1,2
m0 = (2, 9, 4)

# For s_i = 1:
# d = 0,1,2,3
# In particular, d=2 allows 0->0, 1->0, and 1->1: mask 13.
m1 = (2, 11, 13, 4)

trans0 = [[compose(state, mat) for mat in m0] for state in range(16)]
trans1 = [[compose(state, mat) for mat in m1] for state in range(16)]

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = data[1]

    # Identity relation before processing any positions.
    dp = [0] * 16
    dp[9] = 1  # 0->0 and 1->1

    for ch in s:
        table = trans1 if ch == ord('1') else trans0
        ndp = [0] * 16

        for state, value in enumerate(dp):
            if value == 0:
                continue
            row = table[state]
            limit = 4 if ch == ord('1') else 3
            for j in range(limit):
                nxt = row[j]
                total = ndp[nxt] + value
                if total >= MOD:
                    total -= MOD
                ndp[nxt] = total

        dp = ndp

    # A cyclic orientation exists iff the composed relation has
    # either 0->0 or 1->1.
    answer = 0
    for relation, count in enumerate(dp):
        if relation & 1 or relation & 8:
            answer += count
            if answer >= MOD:
                answer -= MOD

    print(answer)

if __name__ == "__main__":
    solve()