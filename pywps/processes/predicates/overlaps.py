from pywps import Process, ComplexInput, Format, ComplexOutput
from processes.predicates.validator import Validator


class Overlaps(Process, Validator):
    """Returns True if A and B spatially overlap.
    """

    def __init__(self):
        inputs = [ComplexInput('geomA', 'Geometry', [Format('application/gml+xml')]),
                  ComplexInput('geomB', 'Geometry', [
                               Format('application/gml+xml')]),
                  ]
        outputs = [ComplexOutput('predicate', 'Overlaps result', [
                                 Format('application/json')])]

        super(Overlaps, self).__init__(
            self._handler,
            identifier='overlaps',
            title='Returns True if A and B spatially overlap.',
            abstract="""A and B overlap if they have some but not all points in common,
            have the same dimension, and the intersection of the interiors
            of the two geometries has the same dimension as the geometries themselves.
            That is, only polyons can overlap other polygons and only lines
            can overlap other lines.
            If either A or B are None, the output is always False.
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
        super(Overlaps, self)._handler(geomA, geomB)

        predicate = geomA.overlaps(geomB, align=False)
        response.outputs['predicate'].data = json.dumps(
            {'mask': predicate.to_numpy(dtype=bool).tolist()})
        return response
