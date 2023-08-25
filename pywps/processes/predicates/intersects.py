from pywps import Process, ComplexInput, Format, ComplexOutput
from processes.predicates.validator import Validator


class Intersects(Process, Validator):
    """Returns True if A and B share any portion of space.
    """

    def __init__(self):
        inputs = [ComplexInput('geomA', 'Geometry', [Format('application/gml+xml')]),
                  ComplexInput('geomB', 'Geometry', [
                               Format('application/gml+xml')]),
                  ]
        outputs = [ComplexOutput('predicate', 'Intersects result', [
                                 Format('application/json')])]

        super(Intersects, self).__init__(
            self._handler,
            identifier='intersects',
            title='Returns True if A and B share any portion of space.',
            abstract="""Intersects implies that overlaps, touches and within are True.
            intersects(A, B) == ~disjoint(A, B)
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
        super(Intersects, self)._handler(geomA, geomB)

        predicate = geomA.intersects(geomB, align=False)
        response.outputs['predicate'].data = json.dumps(
            {'mask': predicate.to_numpy(dtype=bool).tolist()})
        return response
