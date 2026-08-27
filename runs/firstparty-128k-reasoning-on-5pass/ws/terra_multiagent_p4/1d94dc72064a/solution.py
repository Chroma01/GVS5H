import sys

def state_type(even_buffer, odd_buffer):
    """
    Outcome for a nonterminal state with:
      even_buffer: number of unclaimed indices with A_i - 1 even
      odd_buffer:  number of unclaimed indices with A_i - 1 odd

    Return:
      'W': current player wins for either buffer-total parity
      'O': current player wins iff current available delay buffer is odd
      'E': current player wins iff current available delay buffer is even
    """
    e = even_buffer
    o = odd_buffer

    if e == 0:
        return 'W' if o == 1 else 'O'

    if e == 1:
        if o == 0:
            return 'W'
        if o == 1:
            return 'O'
        if o == 2:
            return 'W'
        return 'E'

    if e == 2:
        return 'W' if o == 1 else 'O'

    return 'E' if e % 2 == 1 else 'O'


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    if n == 1:
        print("Fennec")
        return

    # A_i odd means A_i - 1 is even.
    e = sum(x & 1 for x in a)
    o = n - e

    # Claiming an index with even buffer starts the opponent with an even
    # available delay total. Such a state is losing exactly for type O.
    if e > 0 and state_type(e - 1, o) == 'O':
        print("Fennec")
        return

    # Claiming an index with odd buffer starts the opponent with an odd
    # available delay total. Such a state is losing exactly for type E.
    if o > 0 and state_type(e, o - 1) == 'E':
        print("Fennec")
        return

    print("Snuke")


if __name__ == "__main__":
    main()