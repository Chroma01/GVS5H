import sys

MOD = 998244353


def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    s = data[1] if len(data) > 1 else ""

    # Parse the parenthesis sequence into a rooted ordered forest.
    # Each matching pair is a node.  Top-level pairs are children of an
    # artificial root, stored separately.
    children = []
    stack = []
    root_children = []

    for ch in s:
        if ch == "(":
            idx = len(children)
            children.append([])
            if stack:
                children[stack[-1]].append(idx)
            else:
                root_children.append(idx)
            stack.append(idx)
        else:
            if stack:
                stack.pop()

    m_nodes = len(children)

    # Factorials and inverse factorials up to the maximum possible number
    # of children of any node (including the artificial root).
    fact = [1] * (m_nodes + 1)
    for i in range(1, m_nodes + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (m_nodes + 1)
    invfact[m_nodes] = pow(fact[m_nodes], MOD - 2, MOD)
    for i in range(m_nodes, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # Canonical unordered tree types.
    # A type is represented by the sorted tuple of its children's type IDs.
    type_id = [0] * m_nodes
    type_to_id = {}
    embeddings = []

    def calc_embeddings(tup):
        """Number of ordered embeddings for a node whose sorted child-type
        tuple is tup.  All child types in tup must already have embeddings.
        """
        m = len(tup)
        val = fact[m]
        i = 0
        while i < m:
            ct = tup[i]
            j = i + 1
            while j < m and tup[j] == ct:
                j += 1
            cnt = j - i
            val = val * invfact[cnt] % MOD
            val = val * pow(embeddings[ct], cnt, MOD) % MOD
            i = j
        return val

    def get_type(tup):
        tid = type_to_id.get(tup)
        if tid is not None:
            return tid

        tid = len(embeddings)
        type_to_id[tup] = tid
        embeddings.append(calc_embeddings(tup))
        return tid

    # Parents are created before children, so reverse index order is bottom-up.
    for idx in range(m_nodes - 1, -1, -1):
        if children[idx]:
            tup = tuple(sorted(type_id[c] for c in children[idx]))
        else:
            tup = ()
        type_id[idx] = get_type(tup)

    # Apply the same counting formula to the artificial root / top-level forest.
    if not root_children:
        print(1)
        return

    root_tup = tuple(sorted(type_id[c] for c in root_children))
    ans = calc_embeddings(root_tup)
    print(ans)


if __name__ == "__main__":
    solve()