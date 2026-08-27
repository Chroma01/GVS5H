import sys
import bisect

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    Q = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    # (R, X, original_index)
    queries = []
    for idx in range(Q):
        R = int(next(it))
        X = int(next(it))
        queries.append((R, X, idx))

    # answer queries in order of increasing R while scanning the array
    queries.sort(key=lambda x: x[0])

    dp = []                     # dp[k] = minimal possible last element of an inc. subsequence of length k+1
    ans = [0] * Q
    q_ptr = 0                   # points to the next query to answer

    # scan the array, positions are 1‑based as in the problem statement
    for pos, val in enumerate(A, start=1):
        # update dp with the current value
        i = bisect.bisect_left(dp, val)
        if i == len(dp):
            dp.append(val)
        else:
            dp[i] = val

        # answer every query whose prefix ends exactly at this position
        while q_ptr < Q and queries[q_ptr][0] == pos:
            _, X, qid = queries[q_ptr]
            ans[qid] = bisect.bisect_right(dp, X)
            q_ptr += 1

    # all queries are guaranteed to have R ≤ N, so they are all answered here
    sys.stdout.write("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()