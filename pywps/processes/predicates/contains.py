from pywps import Process, ComplexInput, ComplexOutput, Format
from processes.predicates.validator import Validator


class Contains(Process, Validator):
    """Returns True if geometry B is completely inside geometry A
    """

    def __init__(self):
        inputs = [ComplexInput('geomA', 'Geometry', [Format('application/gml+xml')]),
                  ComplexInput('geomB', 'Geometry', [
                               Format('application/gml+xml')])]
        outputs = [ComplexOutput(
            'predicate', 'Contains result', [
                Format('application/json')])]

        super(Contains, self).__init__(
            self._handler,
            identifier='contains',
            title='Process contains or contains properly between two geometries',
            abstract="""
            Process returns True if geometry B is completely inside geometry A.
            The operation works on: n-to-n, n-to-1.
            A.contains(B) == B.within(A)""",
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
        super(Contains, self)._handler(geomA, geomB)

        predicate = geomA.contains(geomB, align=False)
        response.outputs['predicate'].data = json.dumps(
            {'mask': predicate.to_numpy(dtype=bool).tolist()})
        return response
