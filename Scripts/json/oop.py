from unicodedata import numeric


class MyClass:
    x=10

    def __init__(self,
            y = 20, w = 30) -> None:
        self.y=y
        self.w=w

    def __init__(self) -> str:
        return f"({self.y},{self.w})"

    def get_general_sum(self) -> int:
        return MyClass.x + self.y + self.w

def main():
    obj1=MyClass()
    obj2=MyClass(40)
    obj3=MyClass(50,60)
    obj4=MyClass(w=70) 
    del obj1.x
    print(obj4.get_general_sum())


if __name__ == "__main__":
    main()