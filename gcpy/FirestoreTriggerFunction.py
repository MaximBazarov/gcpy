from enum import Enum

from gcpy.CloudFunction import CloudFunction
from gcpy.FirestoreCollection import FirestoreCollection
from gcpy.utils import answer


class FirestoreTrigger(Enum):
    """

    https://cloud.google.com/functions/docs/calling/cloud-firestore
    """
    # onUpdate	Triggered when a document already exists and has any value changed.
    onUpdate = 'update'

    # onDelete	Triggered when a document with data is deleted.
    onDelete = 'delete'

    # onCreate	Triggered when a document is written to for the first time.
    onCreate = 'create'

    # onWrite: Triggered when onCreate, onUpdate or onDelete is triggered.
    onWrite = 'write'

    # For cases when trigger is not present
    noTrigger = ''


class FirestoreTriggerFunction(CloudFunction):
    name: str = None
    collection_to_listen: FirestoreCollection = None
    trigger: FirestoreTrigger = None
    project_name: str = None

    @property
    def cli_trigger_string(self):
        return '--trigger-event providers/cloud.firestore/eventTypes/document.{} ' \
               '--trigger-resource "projects/{}/databases/(default)/documents/{}/{{document}}" ' \
            .format(self.project_name, self.trigger.value, self.collection_to_listen.name)

    def handle(self, data, context):
        try:
            change = self.collection_to_listen.changes_from_event(data)
            trigger = FirestoreTrigger.noTrigger
            event_type = context.event_type.split('.')[-1]
            doc_id = context.resource.split('/')[-1]
            for t in FirestoreTrigger:
                if t.value == event_type:
                    trigger = t
            self.handle_change(doc_id, change.old, change.new, trigger)
        except ValueError as err:
            answer.failure(400, '{}'.format(err))

    def handle_change(self, doc_id, old, new, trigger: FirestoreTrigger):
        """

        To override in ancestors
        Will be called when change occurs

        StockExchangeDocument is a class that defined in the ancestor FirestoreCollection

        :param doc_id: Document id from resource
        :param trigger: FirestoreTrigger
        :param old: old StockExchangeDocument
        :param new: new StockExchangeDocument
        :return:
        """
        print('Unhandled change triggered by {} from old: {} to new: {}'.format(trigger, old, new))
        return
