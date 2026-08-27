import sys
from collections import Counter

def main():
    MOD = 998244353
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()

    # Build rooted forest with a virtual root (node 0).
    # children[i] = list of child node ids of node i.
    children = [[]]
    stack = [0]  # virtual root
    for ch in s:
        if ch == '(':
            node = len(children)
            children.append([])
            children[stack[-1]].append(node)
            stack.append(node)
        else:  # ')'
            stack.pop()

    # Post-order traversal (iterative) to compute labels bottom-up.
    label = [0] * len(children)
    order = []
    st = [0]
    while st:
        u = st.pop()
        order.append(u)
        for v in children[u]:
            st.append(v)
    # order is preorder; process in reverse so children come before parents.

    label_id = {}  # tuple of sorted child labels -> canonical id
    next_id = 0

    fact = [1] * (n + 2)
    for i in range(1, n + 2):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (n + 2)
    inv_fact[n + 1] = pow(fact[n + 1], MOD - 2, MOD)
    for i in range(n + 1, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    ans = 1
    for u in reversed(order):
        child_labels = sorted(label[v] for v in children[u])
        key = tuple(child_labels)
        if key not in label_id:
            label_id[key] = next_id
            next_id += 1
        label[u] = label_id[key]

        # Number of distinct permutations of the multiset of children:
        # k! / prod(multiplicity!)
        k = len(children[u])
        ways = fact[k]
        for m in Counter(child_labels).values():
            ways = ways * inv_fact[m] % MOD
        ans = ans * ways % MOD

    print(ans)

main()