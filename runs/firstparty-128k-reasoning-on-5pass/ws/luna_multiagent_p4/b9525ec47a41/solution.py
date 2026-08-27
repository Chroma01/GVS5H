import sys

MOD = 998244353

# Boolean relation composition:
# relation bit (r * 2 + c) means r -> c.
compose = [[0] * 16 for _ in range(16)]
for a in range(16):
    for b in range(16):
        result = 0
        for r in range(2):
            for m in range(2):
                if (a >> (2 * r + m)) & 1:
                    for c in range(2):
                        if ((b >> (2 * m + c)) & 1):
                            result |= 1 << (2 * r + c)
        compose[a][b] = result

# Output-degree relations for a position without/with a spoke.
# Rows are the previous cycle-edge state, columns the next one.
relations = [
    [2, 9, 4],          # s_i = 0, degrees 0,1,2
    [2, 11, 13, 4],      # s_i = 1, degrees 0,1,2,3
]

transitions = []
for typ in range(2):
    cur = []
    for state in range(16):
        counts = [0] * 16
        for rel in relations[typ]:
            counts[compose[state][rel]] += 1
        cur.append([(to, mult) for to, mult in enumerate(counts) if mult])
    transitions.append(cur)

data = sys.stdin.buffer.read().split()
n = int(data[0])
s = data[1].decode()

# Start with the identity relation: the initial and final cycle states agree.
dp = [0] * 16
dp[9] = 1

for ch in s:
    tr = transitions[1 if ch == '1' else 0]
    ndp = [0] * 16
    for state, ways in enumerate(dp):
        if ways:
            for nxt, multiplicity in tr[state]:
                ndp[nxt] += ways * multiplicity
    for i in range(16):
        ndp[i] %= MOD
    dp = ndp

# A cyclic orientation exists exactly when the resulting relation
# contains (0,0) or (1,1), i.e. one of the diagonal bits.
answer = 0
for state, ways in enumerate(dp):
    if state & 9:
        answer += ways

print(answer % MOD)