import sys
from collections import Counter

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = data[1].decode()

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (n + 1)
    invfact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # Each stack entry stores the canonical IDs of the children
    # of one currently open parenthesis.
    stack = []
    roots = []

    type_to_id = {}
    dp = []

    for ch in s:
        if ch == '(':
            stack.append([])
        else:
            children = stack.pop()
            key = tuple(sorted(children))

            node_id = type_to_id.get(key)
            if node_id is None:
                node_id = len(dp)
                type_to_id[key] = node_id

                ways = fact[len(children)]
                for child_id in children:
                    ways = ways * dp[child_id] % MOD

                for multiplicity in Counter(children).values():
                    ways = ways * invfact[multiplicity] % MOD

                dp.append(ways)

            if stack:
                stack[-1].append(node_id)
            else:
                roots.append(node_id)

    answer = fact[len(roots)]
    for root_id in roots:
        answer = answer * dp[root_id] % MOD

    for multiplicity in Counter(roots).values():
        answer = answer * invfact[multiplicity] % MOD

    print(answer)

if __name__ == "__main__":
    main()