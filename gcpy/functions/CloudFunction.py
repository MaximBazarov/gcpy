class CloudFunctionTrigger:
    cli_trigger_string = '--trigger '


class CloudFunction:
    name = 'function_public_name'
    timeout = 60
    labels = []
    trigger = CloudFunctionTrigger()

    def __init__(self):
        pass

    def url(self):
        return self.name
