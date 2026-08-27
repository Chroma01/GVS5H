import sys
from collections import deque

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1])
    S = data[2].strip()

    start = (0,) * N
    id_of = {start: 0}
    states = [start]
    trans = []  # trans[state_id] = list of 26 next-state ids

    q = deque([start])
    while q:
        st = q.popleft()
        sid = id_of[st]
        nxt_ids = []
        for c in range(26):
            # compute new row via LCS recurrence
            # st[i] = LCS(T_prefix, S[:i+1]); st[-1] conceptually 0 for i=-1
            new = []
            prev_new = 0  # new_{i-1}
            prev_old = 0  # d_{i-1}
            for i in range(N):
                di = st[i]
                val = di
                if prev_new > val:
                    val = prev_new
                if S[i] == chr(ord('a') + c):
                    cand = prev_old + 1
                    if cand > val:
                        val = cand
                new.append(val)
                prev_old = di
                prev_new = val
            nt = tuple(new)
            if nt not in id_of:
                id_of[nt] = len(states)
                states.append(nt)
                q.append(nt)
            nxt_ids.append(id_of[nt])
        trans.append(nxt_ids)

    # Aggregate transitions: per state, dict next_id -> count of letters
    agg = []
    for nxt_ids in trans:
        d = {}
        for nid in nxt_ids:
            d[nid] = d.get(nid, 0) + 1
        agg.append(list(d.items()))

    # M-step counting DP
    cur = [0] * len(states)
    cur[0] = 1
    for _ in range(M):
        nxt = [0] * len(states)
        for sid, cnt in enumerate(cur):
            if cnt:
                for nid, mult in agg[sid]:
                    nxt[nid] = (nxt[nid] + cnt * mult) % MOD
        cur = nxt

    ans = [0] * (N + 1)
    for sid, st in enumerate(states):
        ans[st[-1]] = (ans[st[-1]] + cur[sid]) % MOD

    sys.stdout.write(' '.join(map(str, ans)) + '\n')

main()