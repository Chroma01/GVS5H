import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    s = data[1].strip()
    k = s.count('1')

    # Answer = (2^N - 1) * 2^k mod MOD
    # Reasoning (verified by brute force for all N<=6 and random N=7):
    # distinct indegree sequences of cycle+hub graph =
    #   (indegree sequences of the N-cycle) * (choices of spoke orientations)
    # = (2^N - 1) * 2^k.
    ans = (pow(2, N, MOD) - 1) * pow(2, k, MOD) % MOD
    print(ans)

main()