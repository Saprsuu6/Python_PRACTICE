import datetime


class MyInfo:
    def __init__(self) -> None:
        self.info = []

    def add_info(self, info=None) -> None or Exception:
        if (info == None):
            raise Exception('You have to set info')

        self.info.append(info)

    def get_info(self) -> list or str:
        return self.info if len(self.info) != 0 else 'Infos is empty'


def fill_info(my_info: MyInfo) -> None:
    my_info.add_info({'Name': 'Артемов В.П.', 'Sex': 'ч',
                      'BD': datetime.date(1992, 12, 11), 'Country': 'Німеччина', 'Avia_company': 'Lufthansa', 'Departure_date': datetime.date(2022, 2, 12), 'Departure_time': datetime.time(16, 20), 'Class': 'Економ', 'Price': 340})
    my_info.add_info({'Name': 'Крейд С.Р.', 'Sex': 'ч',
                      'BD': datetime.date(2015, 11, 12), 'Country': 'Ізраїль', 'МАУ': 'Lufthansa', 'Departure_date': datetime.date(2022, 10, 13), 'Departure_time': datetime.time(22, 30), 'Class': 'Бізнес', 'Price': 470})
    my_info.add_info({'Name': 'Сидорова Е.А', 'Sex': 'ж',
                      'BD': datetime.date(2012, 11, 19), 'Country': 'Іспанія', 'МАУ': 'Lufthansa', 'Departure_date': datetime.date(2022, 9, 22), 'Departure_time': datetime.time(18, 40), 'Class': 'Бізнес', 'Price': 490})
    my_info.add_info({'Name': 'Богданов А.С', 'Sex': 'ч',
                      'BD': datetime.date(1979, 1, 19), 'Country': 'Іспанія', 'МАУ': 'Lufthansa', 'Departure_date': datetime.date(2021, 12, 30), 'Departure_time': datetime.time(18, 40), 'Class': 'Бізнес', 'Price': 490})


def main():
    my_info = MyInfo()

    fill_info(my_info)
    print(my_info.get_info())
    # print(my_info.get_info()[0]['BD'])


if __name__ == "__main__":
    main()
