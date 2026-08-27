import sys

def solve() -> None:
    data = sys.stdin.read().splitlines()
    if not data:
        return
    K = int(data[0])
    S = data[1] if len(data) > 1 else ''
    T = data[2] if len(data) > 2 else ''
    n = len(S)
    m = len(T)

    # Quick rejection if length difference already exceeds K
    if abs(n - m) > K:
        print("No")
        return

    INF = K + 1  # any value > K is considered infinite

    # Convert strings to lists of integers for faster comparison
    S_ints = [ord(c) for c in S]
    T_ints = [ord(c) for c in T]

    # DP for i = 0 (empty prefix of S)
    cur = [INF] * (m + 1)
    limit0 = min(m, K)
    for j in range(limit0 + 1):
        cur[j] = j  # distance to obtain first j chars of T from empty S

    nxt = [INF] * (m + 1)  # buffer for the next row

    # Iterate over prefixes of S
    for i in range(1, n + 1):
        left = i - K
        if left < 0:
            left = 0
        right = i + K
        if right > m:
            right = m

        # Base case: distance to empty T
        if i <= K:
            nxt[0] = i
        else:
            nxt[0] = INF

        # Ensure the cell just left of the band is INF (needed for insertion at j = left)
        if left > 0 and left - 1 <= m:
            nxt[left - 1] = INF

        # Determine the first j to compute in the band (skip j = 0)
        start = left
        if start == 0:
            start = 1

        if start <= right:
            si = S_ints[i - 1]          # current character of S as int
            cur_row = cur
            nxt_row = nxt
            T_local = T_ints
            INF_local = INF
            K_local = K
            for j in range(start, right + 1):
                # substitution cost (0 if characters match, else 1)
                cost = 0 if si == T_local[j - 1] else 1
                del_cost = cur_row[j] + 1          # delete S[i-1]
                ins_cost = nxt_row[j - 1] + 1      # insert into S
                sub_cost = cur_row[j - 1] + cost   # replace (or keep)
                best = del_cost
                if ins_cost < best:
                    best = ins_cost
                if sub_cost < best:
                    best = sub_cost
                if best > K_local:
                    best = INF_local
                nxt_row[j] = best

        # Prepare for next iteration
        cur, nxt = nxt, cur

    # Result is the distance for the full strings
    print("Yes" if cur[m] <= K else "No")

if __name__ == "__main__":
    solve()