import sys
from bisect import bisect_right

def sieve(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    primes = [i for i, val in enumerate(is_prime) if val]
    return primes

def generate_400_numbers(limit, primes):
    numbers = set()
    n = len(primes)
    for i in range(n):
        p = primes[i]
        p2 = p * p
        if p2 > limit:
            break
        # iterate over even powers of p
        power_p = p2
        while power_p <= limit:
            for j in range(i + 1, n):
                q = primes[j]
                q2 = q * q
                if power_p * q2 > limit:
                    break
                power_q = q2
                while power_p * power_q <= limit:
                    numbers.add(power_p * power_q)
                    # increase q exponent by 2
                    if power_q > limit // (q * q):
                        break
                    power_q *= q * q
            # increase p exponent by 2
            if power_p > limit // (p * p):
                break
            power_p *= p * p
    return sorted(numbers)

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    Q = int(data[0])
    A_list = list(map(int, data[1:1+Q]))
    max_A = max(A_list)
    # smallest 400 number is 36 = 2^2 * 3^2
    # we need primes up to sqrt(max_A) for p^2 <= max_A
    # but we also need q^2 up to max_A, so primes up to sqrt(max_A)
    import math
    prime_limit = int(math.isqrt(max_A)) + 1
    primes = sieve(prime_limit)
    four_hundred_numbers = generate_400_numbers(max_A, primes)
    # Ensure 36 is included (it should be, but just in case)
    if 36 not in four_hundred_numbers:
        four_hundred_numbers.append(36)
        four_hundred_numbers.sort()
    out_lines = []
    for A in A_list:
        # largest N <= A
        idx = bisect_right(four_hundred_numbers, A) - 1
        if idx >= 0:
            out_lines.append(str(four_hundred_numbers[idx]))
        else:
            # problem guarantees existence, but just in case
            out_lines.append("36")
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()