import sys
from collections import deque

MOD = 998244353


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])
    S = data[2].decode()

    start = (0,) * (N + 1)
    state_id = {start: 0}
    states = [start]
    transitions = []
    queue = deque([start])

    while queue:
        prev = queue.popleft()
        grouped = {}

        for c in range(26):
            cur = [0] * (N + 1)
            for j in range(1, N + 1):
                best = prev[j]
                if cur[j - 1] > best:
                    best = cur[j - 1]
                if c == ord(S[j - 1]) - 97:
                    candidate = prev[j - 1] + 1
                    if candidate > best:
                        best = candidate
                cur[j] = best

            nxt = tuple(cur)
            if nxt not in state_id:
                state_id[nxt] = len(states)
                states.append(nxt)
                queue.append(nxt)

            dest = state_id[nxt]
            grouped[dest] = grouped.get(dest, 0) + 1

        transitions.append(list(grouped.items()))

    count = [0] * len(states)
    count[0] = 1

    for _ in range(M):
        nxt_count = [0] * len(states)
        for src, ways in enumerate(count):
            if ways:
                for dest, multiplicity in transitions[src]:
                    nxt_count[dest] = (
                        nxt_count[dest] + ways * multiplicity
                    ) % MOD
        count = nxt_count

    answer = [0] * (N + 1)
    for state, ways in zip(states, count):
        answer[state[-1]] = (answer[state[-1]] + ways) % MOD

    print(*answer)


if __name__ == "__main__":
    solve()