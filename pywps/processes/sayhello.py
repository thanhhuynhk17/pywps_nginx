
from pywps import Process, LiteralInput, LiteralOutput, UOM


class SayHello(Process):
    def __init__(self):
        inputs = [LiteralInput('name', 'Input name', data_type='string')]
        outputs = [LiteralOutput('response',
                                 'Output response', data_type='string')]

        super(SayHello, self).__init__(
            self._handler,
            identifier='say_hello',
            title='Process Say Hello',
            abstract='Returns a literal string output\
             with Hello plus the inputed name',
            version='1.3.3.7',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        import socket
        response.outputs['response'].data = f'Hello \
            {request.inputs["name"][0].data}, {socket.gethostname()}'

        response.outputs['response'].uom = UOM('unity')
        return response
