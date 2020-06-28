import os

from gcpy.CloudFunction import CloudFunction
from gcpy.FirestoreTriggerFunction import FirestoreTriggerFunction
from gcpy.HTTPFunction import HTTPFunction
from gcpy.PubSubTriggerFunction import PubSubFunction
from gcpy.Types import ListOfCloudFunctionTypes, CloudFunctionType


def main_py_imports(function_type: type):
    return 'from {} import {} '.format(function_type.__module__, function_type.__name__)


def main_py_code(function_type: CloudFunctionType):
    params = ''
    if function_type.__base__ == FirestoreTriggerFunction:
        params = '(data, context)'
    if function_type.__base__ == PubSubFunction:
        params = '(event, context)'
    if function_type.__base__ == HTTPFunction:
        params = '(request)'

    code = [
        '\n',
        'def {}{}:'.format(function_type.name, params),
        '    try:',
        '        return {}().handle{}'.format(function_type.__name__, params),
        '    except Exception as e:',
        '        return answer.throw_failure(400, \'{}\'.format(e))',
        '    except:  # catch *all* exceptions',
        '        e = sys.exc_info()[0]',
        '        return answer.throw_failure(400, \'Exception: {} | {}\'.format(type(e), e))',
    ]
    return code


def generate(functions: ListOfCloudFunctionTypes, filename: str = "main.py"):
    main_py = open(filename, "w")
    main_py.write('import sys\n')
    main_py.write('from utils import answer\n')
    for f in functions:
        main_py.write(main_py_imports(f))
        main_py.write('\n')

    for f in functions:
        for line in main_py_code(f):
            main_py.write(line)
            main_py.write('\n')

    main_py.close()
