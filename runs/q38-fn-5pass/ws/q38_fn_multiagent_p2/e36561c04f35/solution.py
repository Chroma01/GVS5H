import sys

def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    t = data[0]
    idx = 1
    ans = []

    for _ in range(t):
        n = data[idx]
        idx += 1

        vals = []
        caps = []  # 1 if the run is a singleton, 2 if its length is at least 2

        prev = data[idx]
        cnt = 1
        idx += 1
        for _ in range(n - 1):
            x = data[idx]
            idx += 1
            if x == prev:
                cnt += 1
            else:
                vals.append(prev)
                caps.append(1 if cnt == 1 else 2)
                prev = x
                cnt = 1
        vals.append(prev)
        caps.append(1 if cnt == 1 else 2)

        r = len(vals)
        if r == 1:
            ans.append("1")
            continue

        # dp[i] is a small dict:
        #   key   = value of the current rightmost "anchor" run after processing runs [0..i]
        #   value = maximum profit (number of profitable swaps)
        #
        # Only the value of the anchor matters; whether it is singleton or long is irrelevant
        # because the anchor is never used as a middle run in the canonical left-to-right process.
        dp = [None] * r
        dp[0] = {vals[0]: 0}

        for i in range(r):
            cur = dp[i]
            if not cur:
                continue

            best = max(cur.values())

            # 1) Do nothing: make the next run the new anchor.
            if i + 1 < r:
                v = vals[i + 1]
                nxt = dp[i + 1]
                if nxt is None:
                    dp[i + 1] = {v: best}
                else:
                    old = nxt.get(v)
                    if old is None or best > old:
                        nxt[v] = best

            # 2) Neutral enabling swap: x y x -> x y, making y the new anchor.
            #    Profit is 0, but it may enable future profitable swaps.
            # 3) Profitable swap: x y x y -> x y, making y the new anchor.
            #    Profit is +1.
            #
            # The two middle runs y and x must be singleton.
            if i + 2 < r and caps[i + 1] == 1 and caps[i + 2] == 1:
                x = vals[i + 2]
                p = cur.get(x)
                if p is not None:
                    y = vals[i + 1]

                    # Neutral transition to i+2.
                    nxt = dp[i + 2]
                    if nxt is None:
                        dp[i + 2] = {y: p}
                    else:
                        old = nxt.get(y)
                        if old is None or p > old:
                            nxt[y] = p

                    # Profitable transition to i+3.
                    if i + 3 < r and vals[i + 3] == y:
                        pp = p + 1
                        nxt = dp[i + 3]
                        if nxt is None:
                            dp[i + 3] = {y: pp}
                        else:
                            old = nxt.get(y)
                            if old is None or pp > old:
                                nxt[y] = pp

        final = dp[r - 1]
        max_profit = max(final.values()) if final else 0
        ans.append(str(r - max_profit))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()