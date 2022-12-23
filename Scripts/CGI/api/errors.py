def send401(message: str = None) -> None:
    print("Status: 401 Unauthorized")
    print('WWW-Authenticate: Basic realm "Authorization required" ')
    print()
    if message:
        print(message)
    return
