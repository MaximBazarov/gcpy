import os

from gcpy.FirestoreTriggerFunction import FirestoreTriggerFunction, FirestoreTrigger
from gcpy.functions.HTTPFunction import HTTPFunction, HTTPTrigger
from gcpy.PubSubTriggerFunction import PubSubFunction, PubSubTrigger
from gcpy.functions.Types import ListOfCloudFunctionTypes, CloudFunctionType
from gcpy.generators import main_py_generator


def generate_commands(
        project_id: str,
        functions: ListOfCloudFunctionTypes,
        region: str,
        labels: dict = None
):
    """

    Generates `gcloud functions deploy` commands for all the functions from the list

    :param project_id: GCP Project ID
    :param functions: List of `CloudFunction` types
    :param region: GCP Cloud Functions Region
    :param labels: dictionary with labels
    :return:
    """
    commands = []

    for f in functions:
        command = u'gcloud functions deploy {} {}'.format(f.name, trigger_string(f, project_id))
        command += u' --runtime python37'

        # Timeout
        command += u' --timeout={}'.format(f.timeout)

        # Region
        command += u' --region={}'.format(region)

        # Labels
        labels_param = ""
        if labels:
            for label in labels.keys():
                labels_param = '{}={} '.format(label, labels[label])

        if labels_param:
            command += u' --update-labels {}'.format(labels_param)

        commands.append(command)
    return commands


def trigger_string(function_type: CloudFunctionType, project_id: str):
    if function_type.trigger.__class__ == FirestoreTrigger:
        return '--trigger-event providers/cloud.firestore/eventTypes/document.{} ' \
               '--trigger-resource "projects/{}/databases/(default)/documents/{}/{{document}}" ' \
            .format(function_type.trigger.value,
                    project_id,
                    function_type.collection_to_listen.name
                    )
    if function_type.trigger.__class__ == PubSubTrigger:
        return '--trigger-topic {} ' \
            .format(function_type.trigger.topic)
    if function_type.trigger.__class__ == HTTPTrigger:
        return '--trigger-http '


def params_string(function_type: CloudFunctionType):
    params = ''
    if function_type.__base__ == FirestoreTriggerFunction:
        params = '(data, context)'
    if function_type.__base__ == PubSubFunction:
        params = '(event, context)'
    if function_type.__base__ == HTTPFunction:
        params = '(request)'


def deploy(
        functions: ListOfCloudFunctionTypes,
        project_id: str,
        region: str,
        main_py_filename: str = 'main.py',
        labels: dict = None,
        execute=False
):
    """
    - Generates `main.py` containing all the functions
    - Generates and runs `gcloud functions deploy` commands for all the functions from the list
    https://cloud.google.com/sdk/gcloud/reference/functions/deploy

    :param functions: List of `CloudFunction` types
    :param project_id: GCP Project ID
    :param region: GCP Cloud Functions Region
    :param main_py_filename: full name with path to `main.py` e.g. ```../main.py```
    :param labels: dictionary with labels
    :param execute: True if you also want to execute generated commands, False by default

    :return: list of commands to execute
    """
    main_py_generator.generate(functions, main_py_filename)
    commands = generate_commands(project_id, functions, region, labels)
    for command in commands:
        print('Executing: {}'.format(command))
        if execute:
            os.system(command)
    return commands
