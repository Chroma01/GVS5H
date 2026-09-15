import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = list(map(int, data[1:1 + n]))

    # Adjacent gaps. gaps[idx] corresponds to 1-indexed gap position idx+1.
    gaps = [x[i + 1] - x[i] for i in range(n - 1)]

    odd_vals, even_vals = [], []
    odd_coeff, even_coeff = [], []

    for idx, g in enumerate(gaps):
        pos = idx + 1            # 1-indexed gap position
        c = n - pos              # contribution coefficient of this gap to the sum
        if pos % 2 == 1:
            odd_vals.append(g)
            odd_coeff.append(c)
        else:
            even_vals.append(g)
            even_coeff.append(c)

    # Rearrangement inequality: pair largest values with smallest coefficients,
    # independently per parity class.
    odd_vals.sort(reverse=True)
    even_vals.sort(reverse=True)
    odd_coeff.sort()
    even_coeff.sort()

    total = n * x[0]             # X_1 is invariant
    for v, c in zip(odd_vals, odd_coeff):
        total += v * c
    for v, c in zip(even_vals, even_coeff):
        total += v * c

    print(total)

main()