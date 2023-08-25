from pywps import Process, ComplexInput, Format, ComplexOutput
from processes.predicates.validator import Validator


class Within(Process, Validator):
    """Returns True if geometry A is completely inside geometry B.
    """

    def __init__(self):
        inputs = [ComplexInput('geomA', 'Geometry', [Format('application/gml+xml')]),
                  ComplexInput('geomB', 'Geometry', [
                               Format('application/gml+xml')]),
                  ]
        outputs = [ComplexOutput('predicate', 'Within result', [
                                 Format('application/json')])]

        super(Within, self).__init__(
            self._handler,
            identifier='within',
            title='Returns True if geometry A is completely inside geometry B.',
            abstract="""A is within B if no points of A lie in the exterior of B and
            at least one point of the interior of A lies in the interior of B.
            A.within(B) == B.contains(A)
            """,
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
        # validation
        super(Within, self)._handler(geomA, geomB)

        predicate = geomA.within(geomB, align=False)
        response.outputs['predicate'].data = json.dumps(
            {'mask': predicate.to_numpy(dtype=bool).tolist()})
        return response
