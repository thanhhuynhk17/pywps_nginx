from pywps import Process, ComplexInput, Format, ComplexOutput
from processes.predicates.validator import Validator


class Equals(Process, Validator):
    """Returns True if A and B are spatially equal.
    """

    def __init__(self):
        inputs = [ComplexInput('geomA', 'Geometry', [Format('application/gml+xml')]),
                  ComplexInput('geomB', 'Geometry', [
                               Format('application/gml+xml')]),
                  ]
        outputs = [ComplexOutput('predicate', 'Equals result', [
                                 Format('application/json')])]

        super(Equals, self).__init__(
            self._handler,
            identifier='equals',
            title='Returns True if A and B are spatially equal.',
            abstract="""
            If A is within B and B is within A, A and B are considered equal.
            The ordering of points can be different.""",
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
        super(Equals, self)._handler(geomA, geomB)

        predicate = geomA.equals(geomB, align=False)
        response.outputs['predicate'].data = json.dumps(
            {'mask': predicate.to_numpy(dtype=bool).tolist()})
        return response
