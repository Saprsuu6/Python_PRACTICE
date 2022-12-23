import os
import errors


def check_auth():
    if 'HTTP_AUTHORIZATION' in os.environ.keys():
        return os.environ['HTTP_AUTHORIZATION']
    else:
        # відправляємо 401
        errors.send401()
        raise Exception("Authorization required")
