from pywps import Process, ComplexInput, ComplexOutput, Format
from processes.predicates.validator import Validator


class Covers(Process, Validator):
    """Returns True if no point in geometry B is outside geometry A.
    """

    def __init__(self):
        inputs = [ComplexInput('geomA', 'Geometry', [Format('application/gml+xml')]),
                  ComplexInput('geomB', 'Geometry', [
                               Format('application/gml+xml')])
                  ]
        outputs = [ComplexOutput('predicate', 'Covers result', [
                                 Format('application/json')])]

        super(Covers, self).__init__(
            self._handler,
            identifier='covers',
            title='Process covers between two geometries',
            abstract="""
            Process returns True if no point in geometry B is outside geometry A.
            A.covers(B) == B.covered_by(A)""",
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
        super(Covers, self)._handler(geomA, geomB)

        predicate = geomA.covers(geomB, align=False)
        response.outputs['predicate'].data = json.dumps(
            {'mask': predicate.to_numpy(dtype=bool).tolist()})
        return response
