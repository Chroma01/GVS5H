import sys

def solve():
    data = sys.stdin.buffer.read().split()
    N = int(data[0]); X = int(data[1]); Y = int(data[2])
    S = data[3].decode(); T = data[4].decode()

    def signature(s):
        n = len(s)
        absorbed = [-1] * n
        token_types = []
        pz = 0
        po = 0
        pend_z = []
        pend_o = []
        for i in range(n):
            if s[i] == '0':
                pend_z.append(i)
                pz += 1
                if pz == X:
                    tid = len(token_types)
                    token_types.append('Z')
                    for pos in pend_z:
                        absorbed[pos] = tid
                    pend_z = []
                    pz = 0
            else:
                pend_o.append(i)
                po += 1
                if po == Y:
                    tid = len(token_types)
                    token_types.append('O')
                    for pos in pend_o:
                        absorbed[pos] = tid
                    pend_o = []
                    po = 0
        result = []
        emitted = set()
        for i in range(n):
            t = absorbed[i]
            if t >= 0:
                if t not in emitted:
                    emitted.add(t)
                    result.append(token_types[t])
            else:
                result.append('z' if s[i] == '0' else 'o')
        return tuple(result)

    print("Yes" if signature(S) == signature(T) else "No")

solve()