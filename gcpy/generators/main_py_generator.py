from gcpy.FirestoreTriggerFunction import FirestoreTriggerFunction, FirestoreTrigger
from gcpy.functions.HTTPFunction import HTTPFunction, HTTPTrigger
from gcpy.PubSubTriggerFunction import PubSubFunction, PubSubTrigger
from gcpy.functions.Types import ListOfCloudFunctionTypes, CloudFunctionType


def generate_function_import(function_type: type):
    return 'from {} import {} '.format(function_type.__module__, function_type.__name__)


def main_py_code(function_type: CloudFunctionType):
    params = ''
    if function_type.trigger.__class__ == FirestoreTrigger:
        params = '(data, context)'
    if function_type.trigger.__class__ == PubSubTrigger:
        params = '(event, context)'
    if function_type.trigger.__class__ == HTTPTrigger:
        params = '(request)'

    code = [
        '\n',
        'def {}{}:'.format(function_type.name, params),
        '    try:',
        '        return {}().handle{}'.format(function_type.__name__, params),
        '    except Exception as e:',
        '        return answer.failure(400, \'{}\'.format(e))',
        '    except:  # catch *all* exceptions',
        '        e = sys.exc_info()[0]',
        '        return answer.failure(400, \'Exception: {} | {}\'.format(type(e), e))',
    ]
    return code


def generate(functions: ListOfCloudFunctionTypes, filename: str = "main.py"):
    main_py = open(filename, "w")
    main_py.write('import sys\n')
    main_py.write('from gcpy.utils import answer\n')
    for f in functions:
        main_py.write(generate_function_import(f))
        main_py.write('\n')

    for f in functions:
        for line in main_py_code(f):
            main_py.write(line)
            main_py.write('\n')

    main_py.close()
