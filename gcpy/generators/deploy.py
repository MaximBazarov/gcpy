import os
from gcpy.Types import ListOfFunctions


def deploy(functions: ListOfFunctions):
    commands = []
    for f in functions:
        commands.append(
            u'gcloud functions deploy {} {}'
            # TODO: update labels when they exist
            u'--update-labels s=mimir '
            u'--runtime python37 '
            u'--timeout={} '
            u'--region europe-west2 '
                .format(f.name, f().cli_trigger_string, f.timeout)
        )

    for command in commands:
        print(command)
        os.system(command)
