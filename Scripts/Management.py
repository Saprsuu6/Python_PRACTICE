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
                      'BD': datetime.date(2015, 11, 12), 'Country': 'Ізраїль', 'Avia_company': 'МАУ', 'Departure_date': datetime.date(2022, 10, 13), 'Departure_time': datetime.time(22, 30), 'Class': 'Бізнес', 'Price': 470})
    my_info.add_info({'Name': 'Сидорова Е.А', 'Sex': 'ж',
                      'BD': datetime.date(2012, 11, 19), 'Country': 'Іспанія', 'Avia_company': 'МАУ', 'Departure_date': datetime.date(2022, 9, 22), 'Departure_time': datetime.time(18, 40), 'Class': 'Бізнес', 'Price': 490})
    my_info.add_info({'Name': 'Богданов А.С', 'Sex': 'ч',
                      'BD': datetime.date(1979, 1, 19), 'Country': 'Іспанія', 'Avia_company': 'МАУ', 'Departure_date': datetime.date(2021, 12, 30), 'Departure_time': datetime.time(18, 40), 'Class': 'Бізнес', 'Price': 490})
    my_info.add_info({'Name': 'Буртик Н.К', 'Sex': 'ж',
                      'BD': datetime.date(1980, 1, 21), 'Country': 'Туреччина', 'Avia_company': 'Turkish Airlines', 'Departure_date': datetime.date(2021, 10, 6), 'Departure_time': datetime.time(7, 30), 'Class': 'Перший', 'Price': 440})
    my_info.add_info({'Name': 'Горкун В.Л.', 'Sex': 'ч',
                      'BD': datetime.date(2016, 12, 13), 'Country': 'Іспанія', 'Avia_company': 'МАУ', 'Departure_date': datetime.date(2020, 11, 19), 'Departure_time': datetime.time(18, 40), 'Class': 'Бізнес', 'Price': 490})
    my_info.add_info({'Name': 'Горяєв С.Н', 'Sex': 'ч',
                      'BD': datetime.date(1957, 9, 30), 'Country': 'Франція', 'Avia_company': 'AirFrance', 'Departure_date': datetime.date(2021, 12, 3), 'Departure_time': datetime.time(12, 30), 'Class': 'Економ', 'Price': 395})
    my_info.add_info({'Name': 'Зайцева Н.В.', 'Sex': 'ж',
                      'BD': datetime.date(1953, 6, 16), 'Country': 'Туреччина', 'Avia_company': 'Turkish Airlines', 'Departure_date': datetime.date(2020, 1, 6), 'Departure_time': datetime.time(7, 30), 'Class': 'Економ', 'Price': 300})
    my_info.add_info({'Name': 'Іванов Р.Т.', 'Sex': 'ч',
                      'BD': datetime.date(1973, 8, 1), 'Country': 'США', 'Avia_company': 'American Airlines', 'Departure_date': datetime.date(2021, 12, 22), 'Departure_time': datetime.time(10, 30), 'Class': 'Бізнес', 'Price': 850})
    my_info.add_info({'Name': 'Шаркова П.Д.', 'Sex': 'ж',
                      'BD': datetime.date(1980, 6, 25), 'Country': 'Німеччина', 'Avia_company': 'Lufthansa', 'Departure_date': datetime.date(2020, 12, 23), 'Departure_time': datetime.time(16, 20), 'Class': 'Бізнес', 'Price': 450})


def main():
    my_info = MyInfo()

    fill_info(my_info)
    print(my_info.get_info())
    # print(my_info.get_info()[0]['BD'])


if __name__ == "__main__":
    main()
