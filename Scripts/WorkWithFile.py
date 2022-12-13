def write_file1():
    try:
        with open("file.txt", mode='w', encoding='utf-8') as f:
            f.write("Hello from file\n")
            f.write("Next line")
    except OSError as err:
        print("File open error: ", err.strerror)


def file_get_contents(name):
    try:
        f = open(name, mode='r', encoding='utf-8')
        return f.read()
    except OSError as err:
        print("File open error: ", err.strerror)
    finally:
        if f != None:
            f.flush
        else:
            return None


def read_lines1() -> None:
    try:
        with open("file.txt") as f:
            n = 0
            for line in f.readlines():
                n += 1
                print(n, line, end="")
    except OSError as err:
        print("File read error: ", err.strerror)


def main():
    # write_file1()
    # print(file_get_contents("file.txt"))
    read_lines1()


if (__name__ == "__main__"):
    main()
