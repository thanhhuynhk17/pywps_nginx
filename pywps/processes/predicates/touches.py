from pywps import Process, ComplexInput, Format, ComplexOutput
from processes.predicates.validator import Validator


class Touches(Process, Validator):
    """Returns True if the only points shared between A and B are on the boundary of A and B.
    """

    def __init__(self):
        inputs = [ComplexInput('geomA', 'Geometry', [Format('application/gml+xml')]),
                  ComplexInput('geomB', 'Geometry', [
                               Format('application/gml+xml')]),
                  ]
        outputs = [ComplexOutput('predicate', 'Touches result', [
                                 Format('application/json')])]

        super(Touches, self).__init__(
            self._handler,
            identifier='touches',
            title='Returns True if the only points shared between A and B are on the boundary of A and B.',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        from geopandas import read_file
        import json
        # prepare data
        geomA = read_file(request.inputs['geomA'][0].file, engine='fiona')
        geomB = read_file(request.inputs['geomB'][0].file, engine='fiona')
        super(Touches, self)._handler(geomA, geomB)

        predicate = geomA.touches(geomB, align=False)
        response.outputs['predicate'].data = json.dumps(
            {'mask': predicate.to_numpy(dtype=bool).tolist()})
        return response
