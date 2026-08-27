import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    # Parse N
    n = int(input_data[0])
    
    # Parse A (though we don't strictly need the values for the logic derived)
    # The logic is: if N is odd, Fennec wins. If N is even, Snuke wins.
    # This is because the game ends when the N-th distinct index is picked.
    # The player who picks the N-th distinct index wins.
    # Since players play optimally, the parity of the total moves is determined by N.
    # Fennec makes moves 1, 3, 5, ...
    # Snuke makes moves 2, 4, 6, ...
    # The N-th move is made by Fennec if N is odd, and by Snuke if N is even.
    # The "waste" moves (picking already visited indices) can be managed by players
    # such that they don't change the winner determined by the mandatory N moves.
    
    if n % 2 == 1:
        print("Fennec")
    else:
        print("Snuke")

if __name__ == '__main__':
    solve()