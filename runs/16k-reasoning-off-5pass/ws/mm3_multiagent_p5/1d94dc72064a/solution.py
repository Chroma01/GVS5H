import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    if n == 1:
        print("Fennec")
        return
    
    # For n >= 2, Fennec wins iff sum(A) is odd (equivalently, sum and n differ in parity).
    # The game always lasts exactly U = sum(A) moves because once S = {1,...,N},
    # the game ends immediately, but under optimal play both players are forced
    # to continue using remaining tokens — the parity of total moves determines the winner.
    # Fennec plays on moves 1, 3, 5, ... (odd-numbered), Snuke on 2, 4, 6, ... (even).
    # Fennec wins iff total move count U is odd.
    total = sum(A)
    if total % 2 == 1:
        print("Fennec")
    else:
        print("Snuke")

if __name__ == "__main__":
    solve()