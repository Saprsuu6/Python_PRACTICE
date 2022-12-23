import datetime
from datetime import datetime as date_now


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


def first_task(my_info: MyInfo) -> str:
    count = 0

    for person in my_info.get_info():
        if person['BD'].year > 1960 and person['Sex'] == 'ж':
            print("Name:", person['Name'])
            count += 1

    return 'Count of persons: ' + str(count)

def second_task(my_info: MyInfo) -> str:
    count = 0

    for person in my_info.get_info():
        if date_now.now().year - person['BD'].year < 12:
            person['Price'] = person['Price'] - person['Price'] * 0.3
            price = person['Price']
            print("Name:", person['Name'], "Price with sale: " + f'{int(price)}')
            count += 1

    return 'Count of persons: ' + str(count)
    
def third_task(my_info: MyInfo) -> str:
    count = 0

    for person in my_info.get_info():
        if person['BD'].year > 1980 and person['Sex'] == 'ч':
            print("Name:", person['Name'])
            count += 1

    return 'Count of persons: ' + str(count)

def fourth_task(my_info: MyInfo) -> str:
    count = 0
    mans = 0

    for person in my_info.get_info():
        if person['BD'].month == 11:
            print("Name:", person['Name'])
            count += 1
            
            if person['Sex'] == 'ч':
                mans += 1

    return 'Count of persons: ' + str(count) + " mans from list: " + str(mans)

def fifth_task(my_info: MyInfo) -> str:
    count = 0

    for person in my_info.get_info():
        if person['Country'] == 'Німеччина':
            print("Name:", person['Name'])
            count += 1

    return 'Count of persons: ' + str(count)

def six_task(my_info: MyInfo) -> str:
    # https://lifehacker.ru/kakoj-den-nedeli/ 
    races = 0

    for person in my_info.get_info():
        two_last_year_numbers = person['Departure_date'].year % 100
        year_code = (6 + two_last_year_numbers + two_last_year_numbers / 4) % 7
        month_codes = [1, 4, 4, 0, 2, 5, 0, 3, 6, 1, 4, 6]
        day_of_the_week = (person['Departure_date'].day + month_codes[person['Departure_date'].month - 1] + year_code) % 7

        if int(day_of_the_week) + 1 == 4:
            print('Country:', person['Country'], 'Avia company:', person['Avia_company'], 'Time of depart:', person['Departure_time'], 'Full price:', person['Price'])
            races += 1
    
    return 'Races evey Firthday: ' + str(races)

def seventh_task(my_info: MyInfo) -> str:
    count = 0

    for person in my_info.get_info():
        if person['Departure_date'].month >= 9 and person['Departure_date'].month <= 11:
            print("Avia company:", person['Avia_company'])
            count += 1

    return 'Races in the autumn: ' + str(count)

def eight_task(my_info: MyInfo) -> str:
    count = 0

    for person in my_info.get_info():
        if date_now.now().year - person['BD'].year > 55:
            person['Price'] = person['Price'] - person['Price'] * 0.1
            price = person['Price']
            print("Name:", person['Name'], "Price with sale: " + f'{int(price)}')
            count += 1

    return 'Count of persons: ' + str(count)

def nineth_task(my_info: MyInfo) -> str:
    count = 0

    for person in my_info.get_info():
        if person['Departure_date'].month == 12 and person['Departure_date'].day == 25:
            person['Price'] = person['Price'] - person['Price'] * 0.4
            price = person['Price']
            print("Name:", person['Name'], "Price with sale: " + f'{int(price)}')
            count += 1

    return 'Count of persons: ' + str(count)

def tenth_task(my_info: MyInfo) -> str:
    count = 0

    for person in my_info.get_info():
        if person['Departure_date'].day <= 10:
            print("Avia company:", person['Avia_company'])
            count += 1

    return 'Count of races: ' + str(count)

def main():
    my_info = MyInfo()

    fill_info(my_info)

    #1.
    print(first_task(my_info))
    print()
    #2.
    print(second_task(my_info))
    print()
    #3.
    print(third_task(my_info))
    print()
    #4.
    print(fourth_task(my_info))
    print()
    #5.
    print(fifth_task(my_info))
    print()
    #6.
    print(six_task(my_info))
    print()
    #7.
    print(seventh_task(my_info))
    print()
    #8.
    print(eight_task(my_info))
    print()
    #9.
    print(nineth_task(my_info))
    print()
    #10.
    print(tenth_task(my_info))
    print()

if __name__ == "__main__":
    main()
