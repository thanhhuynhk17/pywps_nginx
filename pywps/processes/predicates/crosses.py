from pywps import Process, ComplexInput, ComplexOutput, Format
from processes.predicates.validator import Validator


class Crosses(Process, Validator):
    """Returns True if A and B spatially cross.
    """

    def __init__(self):
        inputs = [ComplexInput('geomA', 'Geometry', [Format('application/gml+xml')]),
                  ComplexInput('geomB', 'Geometry', [
                               Format('application/gml+xml')])
                  ]
        outputs = [ComplexOutput('predicate', 'Crosses result', [
                                 Format('application/json')])]

        super(Crosses, self).__init__(
            self._handler,
            identifier='crosses',
            title='Process returns True if A and B spatially cross',
            abstract="""
            A crosses B if they have some but not all interior points in common,
            the intersection is one dimension less than the maximum dimension of A or B,
            and the intersection is not equal to either A or B.""",
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
        super(Crosses, self)._handler(geomA, geomB)

        predicate = geomA.crosses(geomB, align=False)
        response.outputs['predicate'].data = json.dumps(
            {'mask': predicate.to_numpy(dtype=bool).tolist()})
        return response
