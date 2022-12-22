class MyInfo:
    def __init__(self) -> None:
        self.info = []

    def add_info(self, info=None) -> None or Exception:
        if (info == None):
            raise Exception('You have to set info')

        self.info.append(info)

    def get_info(self) -> dict or str:
        return self.info if len(self.info) != 0 else 'Infos is empty'


def main():
    my_info = MyInfo()

    my_info.add_info({"Артемов В.П.", {'Ч', ''}})

    print(my_info.get_info())


if __name__ == "__main__":
    main()
