import sys
import bisect

def sieve(limit):
    """Return list of primes up to limit (inclusive)."""
    is_prime = bytearray(b'\x01') * (limit + 1)
    is_prime[0:2] = b'\x00\x00'
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            step = i
            start = i * i
            is_prime[start:limit+1:step] = b'\x00' * ((limit - start)//step + 1)
    return [i for i, v in enumerate(is_prime) if v]

def generate_400_numbers(limit):
    """Generate all 400 numbers N = p^(2a) * q^(2b) with distinct primes p<q, a,b>=1, and N<=limit."""
    primes = sieve(10**6)  # enough because 2^2=4, and 10^6^2 = 10^12
    numbers = set()
    n_primes = len(primes)
    for i in range(n_primes):
        p = primes[i]
        p2 = p * p
        if p2 > limit:
            break
        # compute even powers of p
        p_powers = []
        cur = p2
        while cur <= limit:
            p_powers.append(cur)
            if cur > limit // (p * p):
                break
            cur *= p * p
        for pp in p_powers:
            # now iterate over larger primes q
            # max q such that q^2 <= limit // pp
            max_q2 = limit // pp
            # find index of first prime > p
            for j in range(i+1, n_primes):
                q = primes[j]
                if q * q > max_q2:
                    break
                # compute even powers of q
                cur_q = q * q
                while cur_q <= max_q2:
                    numbers.add(pp * cur_q)
                    # check overflow possibility
                    if cur_q > max_q2 // (q * q):
                        break
                    cur_q *= q * q
    return sorted(numbers)

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    Q = int(data[0])
    A_list = list(map(int, data[1:1+Q]))
    MAX_A = 10**12
    four_hundred_numbers = generate_400_numbers(MAX_A)
    out_lines = []
    for A in A_list:
        idx = bisect.bisect_right(four_hundred_numbers, A) - 1
        out_lines.append(str(four_hundred_numbers[idx]))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()