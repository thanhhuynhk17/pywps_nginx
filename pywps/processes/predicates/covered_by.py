from pywps import Process, ComplexInput, ComplexOutput, Format
from processes.predicates.validator import Validator


class Covered_by(Process, Validator):
    """Returns True if no point in geometry A is outside geometry B.
    """

    def __init__(self):
        inputs = [ComplexInput('geomA', 'Geometry', [Format('application/gml+xml')]),
                  ComplexInput('geomB', 'Geometry', [
                               Format('application/gml+xml')])
                  ]
        outputs = [ComplexOutput('predicate', 'Covered by result', [
                                 Format('application/json')])]

        super(Covered_by, self).__init__(
            self._handler,
            identifier='covered_by',
            title='Process covers between two geometries',
            abstract="""
            Process returns True if no point in geometry A is outside geometry B.
            A.covered_by(B) == B.covers(A)""",
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
        super(Covered_by, self)._handler(geomA, geomB)

        predicate = geomA.covered_by(geomB, align=False)
        response.outputs['predicate'].data = json.dumps(
            {'mask': predicate.to_numpy(dtype=bool).tolist()})
        return response
