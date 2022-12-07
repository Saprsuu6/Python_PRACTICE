def GetNumber():
    number = None
    
    while True:
        try:
            number = int(input(), 10)
        except:
            print('number can be only int')
            continue

        if number < 0:
            print('number could be only positive')
            continue

        return number

print('Let first number: ')
number_one = GetNumber()

print('Let second number: ')
number_two = None

while number_two != number_one:
    number_two = GetNumber()

    if number_two != number_one:
        print('numbers are not equals')


print ('numbers are equals!!!')


