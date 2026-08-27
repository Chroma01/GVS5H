import sys
from collections import defaultdict

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    s = data[2]

    initial = (0,) * (n + 1)
    states = {initial: 1}
    transition_cache = {}

    for _ in range(m):
        next_states = defaultdict(int)

        for row, count in states.items():
            successors = transition_cache.get(row)
            if successors is None:
                successors = []
                for c in range(26):
                    nxt = [0] * (n + 1)
                    for j in range(1, n + 1):
                        if s[j - 1] == c + 97:
                            nxt[j] = row[j - 1] + 1
                        else:
                            nxt[j] = max(row[j], nxt[j - 1])
                    successors.append(tuple(nxt))
                transition_cache[row] = successors

            for nxt in successors:
                next_states[nxt] = (next_states[nxt] + count) % MOD

        states = next_states

    answer = [0] * (n + 1)
    for row, count in states.items():
        answer[row[-1]] = (answer[row[-1]] + count) % MOD

    print(*answer)

if __name__ == "__main__":
    main()