from random import randint
from sympy import mod_inverse

class EllipticCurve:
    def __init__(self, a, b, p, m=None, q=None):
        self.a = a
        self.b = b
        self.p = p
        self.m = m  # порядок группы точек кривой
        self.q = q  # порядок некоторой цикл подгруппы, m = nq

    def mul(self, P, k):
        #print("k", k)
        if k == 0:
            return (0, 0)
        if k == 1:
            return P
        else:
            half = k // 2
            half_mul = self.mul(P, half)
            if k % 2 == 0:
                return self.add(half_mul, half_mul)
            else:
                return self.add(P, self.add(half_mul, half_mul))


    def add(self, A, B):
        if A == (0, 0): return B
        if B == (0, 0): return A

        xA, yA = A
        xB, yB = B
        if xA == xB:
            if yB == -yA:
                return (0, 0)
            elif yA == yB != 0:
                s = (3 * xA * xA + self.a) * mod_inverse(2 * yA, self.p) % self.p
                x = (s * s - 2 * xA) % self.p
                y = (-yA + s * (xA - x)) % self.p
                return x % self.p, y % self.p
        else:
            s = ((yA - yB) * mod_inverse(xA - xB, self.p)) % self.p
            x = (s * s - xA - xB) % self.p
            y = (-yA + s * (xA - x)) % self.p
            return x % self.p, y % self.p

def h_(m):
    return m

class SignatureGOST3410:
    def __init__(self, elliptic, P, h):
        self.elliptic = elliptic
        self.P = P
        self.h = h

    def sign(self, m, d):
        q = self.elliptic.q
        e = self.h(m) % q
        if e == 0:
            e = 1
        r = 0
        s = 0
        while s == 0:
            while r == 0:
                k = randint(1, q)
                C = self.elliptic.mul(self.P, k)
                r = C[0] % q
            s = (r * d + k * e) % q
        return r, s

    def verify(self, m, signature, Q):
        q = self.elliptic.q
        r, s = signature
        r = int(r)
        s = int(s)
        e = self.h(m) % q
        if e == 0:
            e = 1
        v = mod_inverse(e, q)
        z1 = (s * v) % q
        z2 = (-r * v) % q
        C = self.elliptic.add(self.elliptic.mul(self.P, z1), self.elliptic.mul(Q, z2))
        R = C[0] % q
        if R == r:
            return True
        else:
            return False


a = 7
b = 43308876546767276905765904595650931995942111794451039583252968842033849580414
q = 57896044618658097711785492504343953927082934583725450622380973592137631069619
d = 55441196065363246126355624130324183196576709222340016572108097750006097525544
p = 57896044618658097711785492504343953926634992332820282019728792003956564821041
Q = (57520216126176808443631405023338071176630104906313632182896741342206604859403,
     17614944419213781543809391949654080031942662045363639260709847859438286763994)
P = (2, 4018974056539037503335449422937059775635739389905545080690979365213431566280)
elliptic = EllipticCurve(a=a, b=b, p=p, m=q, q=q)
sig = SignatureGOST3410(elliptic=elliptic, P=P, h=h_)

signature = sig.sign(1303, d)
print("signed", signature)
print(sig.verify(1303, signature, Q))