#! C:\Python\python.exe

import os
envs_template = ["REQUEST_METHOD",
                 "QUERY_STRING", "REQUEST_URI", "REMOTE_ADDR", "REQUEST_SCHEME"]


def get_ul() -> str:
    '''Return UL of env variables'''
    envs = "<ul>"

    for k, v in os.environ.items():
        if k in envs_template:  # add in case envs_template consist this key
            envs += f"<li>{k}={v}</li>"

    envs += "</ul>"
    return envs


print("Content-type: text/html; charset=utf8")
print("")
print(f"""<!doctype html />
<html>
<head>
    <title>Py-191</title>
</head>
<body>
    <h1>Hello CGI World!</h1>
    {get_ul()}
</body>
</html>""")
