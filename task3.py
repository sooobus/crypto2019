# Пусть p - q << sqrt(n)

import math
from random import randint
from sympy import mod_inverse


def naive_mod_pow(n, m, p):
    if m == 0:
        return 1
    else:
        half = m // 2
        half_pow = naive_mod_pow(n, half, p) % p
        if m % 2 == 0:
            return (half_pow * half_pow) % p
        else:
            return (half_pow * half_pow * n) % p


def rsa_keys(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = randint(1, phi - 1)
    while math.gcd(e, phi) != 1:
        e = randint(1, phi - 1)
    d = mod_inverse(e, phi)
    open_key = (n, e)
    close_key = (p, q, d)
    return open_key, close_key


def gen_p_q():
    return 9967, 9973


def rsa_cypher(m):
    p, q = gen_p_q()
    open, close = rsa_keys(p, q)
    return naive_mod_pow(m, open[1], open[0]), open


def crack_rsa(open, m):
    n = open[0]
    sqr = math.floor(math.sqrt(n))
    for i in range(sqr, 0, -1):
        if n % i == 0:
            p = i
            q = n // p
            phi = (p - 1) * (q - 1)
            d = mod_inverse(open[1], phi)
            return naive_mod_pow(m, d, open[0])
            break

def demo(message):
    print("Encrypted message", message, "with RSA:")
    cip, open = rsa_cypher(message)
    print(cip)
    print("Cracked it because of too close primes:")
    print(crack_rsa(open, cip))

demo(13031303)