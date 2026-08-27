import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1]
    T = data[2]

    mp = [-1] * 26
    ps = [False] * 26
    pt = [False] * 26

    for i in range(N):
        c = ord(S[i]) - 97
        d = ord(T[i]) - 97
        ps[c] = True
        pt[d] = True
        if mp[c] == -1:
            mp[c] = d
        elif mp[c] != d:
            print(-1)
            return

    base = sum(1 for c in range(26) if ps[c] and mp[c] != c)

    in_cycle = [False] * 26
    for i in range(26):
        if not ps[i]:
            continue
        seen = {}
        cur = i
        while True:
            if not ps[cur]:
                break
            nxt = mp[cur]
            if nxt < 0 or nxt == cur or not ps[nxt]:
                break
            if cur in seen:
                break
            seen[cur] = len(seen)
            cur = nxt
        if cur in seen:
            x = cur
            while True:
                in_cycle[x] = True
                x = mp[x]
                if x == cur:
                    break

    isolated = 0
    counted = [False] * 26
    for i in range(26):
        if in_cycle[i] and not counted[i]:
            cyc = []
            x = i
            while True:
                cyc.append(x)
                counted[x] = True
                x = mp[x]
                if x == i:
                    break
            cs = set(cyc)
            has_incoming_outside = any(
                ps[u] and u not in cs and mp[u] in cs
                for u in range(26)
            )
            if not has_incoming_outside:
                isolated += 1

    buffer_available = not (all(ps) and all(pt))

    if isolated > 0 and not buffer_available:
        print(-1)
    else:
        print(base + isolated)

if __name__ == "__main__":
    solve()