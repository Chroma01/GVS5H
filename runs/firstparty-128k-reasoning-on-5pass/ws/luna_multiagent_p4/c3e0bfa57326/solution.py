import sys
from collections import Counter

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    s = data[1]

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    # Type IDs represent unordered rooted tree shapes.
    intern = {}
    ways = []

    # Each stack entry is the list of child type IDs of one currently open node.
    stack = []
    root_children = []

    for ch in s:
        if ch == 40:  # '('
            stack.append([])
        else:  # ')'
            children = stack.pop()
            children.sort()
            key = tuple(children)

            node_type = intern.get(key)
            if node_type is None:
                node_type = len(ways)
                intern[key] = node_type

                count = fact[len(children)]
                for child_type, multiplicity in Counter(children).items():
                    count = count * inv_fact[multiplicity] % MOD
                    count = count * pow(ways[child_type], multiplicity, MOD) % MOD

                ways.append(count)

            if stack:
                stack[-1].append(node_type)
            else:
                root_children.append(node_type)

    # The input itself is a forest, handled as the children of a virtual root.
    root_children.sort()
    answer = fact[len(root_children)]
    for child_type, multiplicity in Counter(root_children).items():
        answer = answer * inv_fact[multiplicity] % MOD
        answer = answer * pow(ways[child_type], multiplicity, MOD) % MOD

    print(answer)

if __name__ == "__main__":
    main()