import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    s = data[1].strip()
    # Leaf costs: cost to make leaf 0 or 1
    c0 = [1 if ch == '1' else 0 for ch in s]
    c1 = [1 if ch == '0' else 0 for ch in s]
    # Bottom-up combine triples
    for _ in range(n):
        m = len(c0) // 3
        n0 = [0] * m
        n1 = [0] * m
        idx = 0
        for i in range(m):
            a0 = c0[idx]; b0 = c0[idx+1]; d0 = c0[idx+2]
            # sum of two smallest = total - max
            n0[i] = a0 + b0 + d0 - (a0 if a0 >= b0 and a0 >= d0 else (b0 if b0 >= d0 else d0))
            a1 = c1[idx]; b1 = c1[idx+1]; d1 = c1[idx+2]
            n1[i] = a1 + b1 + d1 - (a1 if a1 >= b1 and a1 >= d1 else (b1 if b1 >= d1 else d1))
            idx += 3
        c0, c1 = n0, n1
    # Root current value is 0 if c0[0] == 0 else 1 (since leaf cost 0 for actual value propagates)
    # Actually root value = 0 if c0[0] <= c1[0]? No: root value determined by original evaluation.
    # But c0[0] is min cost to make root 0, c1[0] to make root 1.
    # Current root value v has cost 0 to keep; the other is answer.
    # Since exactly one of c0[0], c1[0] is 0? Not necessarily, but the min cost to achieve actual value is 0.
    # The answer is the cost to achieve the opposite value.
    # We can determine current value by evaluating, or note: if c0[0] == 0 then current is 0 else current is 1.
    # Because min cost to make root its actual value is 0, and to make it opposite is >0 (unless already both? impossible).
    # Safer: answer = c1[0] if c0[0] == 0 else c0[0]
    ans = c1[0] if c0[0] == 0 else c0[0]
    print(ans)

main()