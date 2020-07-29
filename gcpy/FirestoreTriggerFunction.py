from enum import Enum

from gcpy.functions.CloudFunction import CloudFunction
from gcpy.firestore.Collection import FirestoreCollection
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
    name: str
    collection_to_listen: FirestoreCollection.__class__
    trigger: FirestoreTrigger.__class__

    def handle(self, data, context):
        """
        Google Firestore Trigger cloud function.

        Parses the data to `Change`, that is old: Document and new: Document,
        then calls `handle_change(doc_id: old: new: trigger:)`.

        `Document` is to be overridden in ancestors.

        Args:
            data: data of changes
            context: context of changes

        """
        try:
            print('FirestoreTriggerFunction:handle(self, data, context): {} '.format(data))
            change = self.collection_to_listen.document_type.changes(data)
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

        `Document` is a class that defined in the ancestor FirestoreCollection

        :param doc_id: Document id from resource
        :param trigger: FirestoreTrigger
        :param old: old `Document`
        :param new: new `Document`
        :return:
        """
        print('Unhandled change triggered by {} from old: {} to new: {}'.format(trigger, old, new))
        return
