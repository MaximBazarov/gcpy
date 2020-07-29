from gcpy.functions.CloudFunction import CloudFunctionTrigger, CloudFunction
from gcpy.utils.binary import binary_decode


class HTTPTrigger(CloudFunctionTrigger):
    pass


class HTTPFunction(CloudFunction):
    name = 'function_public_name'
    trigger = HTTPTrigger()

    def handle(self, request):
        print('Handling {}'.format(request))

    @staticmethod
    def body(request):
        result = request.data
        if not result:
            return
        return binary_decode(result)
