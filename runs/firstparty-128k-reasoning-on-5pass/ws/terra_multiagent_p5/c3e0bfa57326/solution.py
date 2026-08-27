import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    s = data[1]
    pairs = n // 2

    fact = [1] * (pairs + 1)
    for i in range(1, pairs + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (pairs + 1)
    invfact[pairs] = pow(fact[pairs], MOD - 2, MOD)
    for i in range(pairs, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # Maps a sorted tuple of unordered child-type IDs to its canonical type ID.
    type_id = {}
    embeddings = []

    def get_type(children):
        children.sort()
        key = tuple(children)

        existing = type_id.get(key)
        if existing is not None:
            return existing

        tid = len(embeddings)
        type_id[key] = tid

        result = fact[len(key)]
        i = 0
        while i < len(key):
            j = i + 1
            while j < len(key) and key[j] == key[i]:
                j += 1

            child = key[i]
            count = j - i
            result = result * invfact[count] % MOD
            result = result * pow(embeddings[child], count, MOD) % MOD
            i = j

        embeddings.append(result)
        return tid

    # Each stack entry stores the children of one currently open node.
    # The initial entry is the virtual root representing the whole forest.
    stack = [[]]

    for ch in s:
        if ch == '(':
            stack.append([])
        else:
            children = stack.pop()
            node_type = get_type(children)
            stack[-1].append(node_type)

    root_type = get_type(stack[0])
    print(embeddings[root_type])


if __name__ == "__main__":
    main()