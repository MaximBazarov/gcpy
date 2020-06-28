def failure(code: int, message: str):
    print('FAILURE: {}'.format(message))
    return message, code, ''


def success(message: str = 'Ok'):
    print(message)
    return message, 200, ''
