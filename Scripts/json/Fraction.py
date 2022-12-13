from fractions import Fraction
import math
class Fraction:
    def __init__(self, numerator = 1, denumerator = 1) -> None:
        if (denumerator==0):
            raise Exception("denumerator can't be 0")
        
        self.numerator = numerator
        self.denumerator = denumerator

    '''Get fruction in str'''
    def get_fraction(self) -> str:
        return f"({self.numerator}/{self.denumerator})"

    '''Reduce fraction'''
    def reduce_fraction(self):
        k = math.gcd(self.numerator, self.denumerator)
        return f"({self.numerator//k}/{self.denumerator//k})"


def main():
    try:
        f1=Fraction(3, 6)
        print(f1.get_fraction())
        print(f1.reduce_fraction())
        print("------------------")
        f2=Fraction(5, -1)
        print(f2.get_fraction())
        print("------------------")
        f=Fraction()
        print(f.get_fraction())
        print("------------------")
        f=Fraction(0, 1)
        print(f.get_fraction())
        print("------------------")
        f=Fraction(0)
        print(f.get_fraction())
        print("------------------")
        f=Fraction(4, -10)
        print(f.get_fraction())
        print("------------------")
        f=Fraction(-4, 0)
        print(f.get_fraction())
        print("------------------")
    except Exception as err:
        print(err)

if __name__ == "__main__":
    main()