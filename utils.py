
def check_prime(num, primes):
    if num < 2:
        return False
    for p in primes:
        if p * p > num:
            break
        if num % p == 0:
            return False
    return True

def get_primes(n):
    num = 2
    primes = []
    while len(primes) < n:
        if check_prime(num, primes):
            primes.append(num)
        num += 1
    return primes
