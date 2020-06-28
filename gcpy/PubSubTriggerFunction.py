import base64

from gcpy.CloudFunction import CloudFunction
from gcpy.utils.binary import str_to_dict


class PubSubTrigger:
    topic: str = None

    def __init__(self, topic: str):
        self.topic = topic


class PubSubFunction(CloudFunction):
    name: str = None
    trigger: PubSubTrigger = None

    @property
    def cli_trigger_string(self):
        return '--trigger-topic {} ' \
            .format(self.trigger.topic)

    def handle(self, event, context):
        """
        Pub/Sub event handler

        :param event: GCP Pub/Sub event
        :param context: GCP context
        :return:
        """
        if 'data' in event:
            message = base64.b64decode(event['data']).decode('utf-8')
            self.handle_message(str_to_dict(message))
        else:
            self.handle_message({})

    def handle_message(self, message: dict):
        """
        To override in ancestors.
        Gets called with parsed message as a dict

        :param message: parsed into a dict message
        :return:
        """
        print('Unhandled message in {}: {}'.format(type(self).__name__, message))
