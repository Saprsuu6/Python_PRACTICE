def get_imitate_header():
    header = ""

    header += "GET: /tutorials/other/top-20-mysql-best-practices/ HTTP/1.1\n"
    header += "Host: net.tutsplus.com\n"
    header += "User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)\n"
    header += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\n"
    header += "Accept-Language: en-us,en;q=0.5\n"
    header += "Accept-Encoding: gzip,deflate\n"
    header += "Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7\n"
    header += "Keep-Alive: 300\n"
    header += "Connection: keep-alive\n"
    header += "Cookie: PHPSESSID=r2t5uvjq435r4q7ib3vtdjq120\n"
    header += "Pragma: no-cache\n"
    header += "Cache-Control: no-cache"

    return header


def write_file():
    try:
        with open("file.txt", mode='w', encoding='utf-8') as f:
            f.write(get_imitate_header())
    except OSError as err:
        print("File error: ", err.strerror)


def get_dict():
    dictionary = {}

    try:
        with open("file.txt") as f:
            for line in f.readlines():
                line = line.replace("\n", '')
                array = line.split(sep=':')
                array[1] = array[1].strip()
                dictionary.update({array[0]: array[1]})
    except OSError as err:
        print("File read error: ", err.strerror)
    finally:
        return dictionary


def main():
    write_file()
    items = get_dict().items()

    for item in items:
        print(item)


if (__name__ == "__main__"):
    main()
