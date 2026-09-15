import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    s = data[1] if len(data) > 1 else ""
    n = max(n, len(s))

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (n + 1)
    invfact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    type_id = {}
    local_factor = []

    def get_type(children):
        children.sort()
        key = tuple(children)

        tid = type_id.get(key)
        if tid is not None:
            return tid, local_factor[tid]

        tid = len(local_factor)
        type_id[key] = tid

        deg = len(key)
        factor = fact[deg]

        i = 0
        while i < deg:
            j = i + 1
            while j < deg and key[j] == key[i]:
                j += 1
            cnt = j - i
            factor = factor * invfact[cnt] % MOD
            i = j

        local_factor.append(factor)
        return tid, factor

    ans = 1
    stack = []
    root_children = []

    for ch in s:
        if ch == '(':
            stack.append([])
        else:
            children = stack.pop()
            tid, factor = get_type(children)
            ans = ans * factor % MOD

            if stack:
                stack[-1].append(tid)
            else:
                root_children.append(tid)

    _, factor = get_type(root_children)
    ans = ans * factor % MOD

    print(ans)

if __name__ == "__main__":
    main()