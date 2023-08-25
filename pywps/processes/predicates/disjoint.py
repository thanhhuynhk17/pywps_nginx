from pywps import Process, ComplexInput, ComplexOutput, Format
from processes.predicates.validator import Validator


class Disjoint(Process, Validator):
    """Returns True if A and B do not share any point in space.
    """

    def __init__(self):
        inputs = [ComplexInput('geomA', 'Geometry', [Format('application/gml+xml')]),
                  ComplexInput('geomB', 'Geometry', [
                               Format('application/gml+xml')])
                  ]
        outputs = [ComplexOutput('predicate', 'Disjoint result', [
                                 Format('application/json')])]

        super(Disjoint, self).__init__(
            self._handler,
            identifier='disjoint',
            title='Returns True if A and B do not share any point in space.',
            abstract="""
            Disjoint implies that overlaps, touches, within, and intersects are False.
            Note missing (None) values are never disjoint.
            A.disjoint(B) == ~A.intersects(B)""",
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
        super(Disjoint, self)._handler(geomA, geomB)

        predicate = geomA.disjoint(geomB, align=False)
        response.outputs['predicate'].data = json.dumps(
            {'mask': predicate.to_numpy(dtype=bool).tolist()})
        return response
