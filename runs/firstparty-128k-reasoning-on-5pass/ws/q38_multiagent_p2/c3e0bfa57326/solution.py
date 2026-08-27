import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    n_input = int(data[0])
    s = ''.join(data[1:])
    n = max(n_input, len(s))

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (n + 1)
    invfact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # Type 0 is the empty node/forest: no children.
    type_id = {(): 0}
    counts = [1]

    def calc(key):
        """Number of ordered realizations of a type whose child-type multiset is key."""
        m = len(key)
        res = fact[m]
        i = 0
        while i < m:
            j = i + 1
            while j < m and key[j] == key[i]:
                j += 1
            k = j - i
            res = res * invfact[k] % MOD
            res = res * pow(counts[key[i]], k, MOD) % MOD
            i = j
        return res

    def get_type(children):
        children.sort()
        key = tuple(children)
        tid = type_id.get(key)
        if tid is None:
            tid = len(counts)
            type_id[key] = tid
            counts.append(calc(key))
        return tid

    stack = []
    top = []

    for ch in s:
        if ch == '(':
            stack.append([])
        else:
            children = stack.pop()
            tid = get_type(children)
            if stack:
                stack[-1].append(tid)
            else:
                top.append(tid)

    ans_id = get_type(top)
    print(counts[ans_id] % MOD)

if __name__ == "__main__":
    main()