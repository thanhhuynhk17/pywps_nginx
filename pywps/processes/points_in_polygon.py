from pywps import Process, ComplexInput, LiteralInput, ComplexOutput, Format
from processes.predicates.validator import Validator


class PointsInPolygon(Process, Validator):
    """Process returns the overlay result of two features from a submitted GML file
    """

    def __init__(self):
        inputs = [ComplexInput('points', 'Multipoint', [Format('application/gml+xml')]),
                  ComplexInput('polygon', 'Polygon', [
                               Format('application/gml+xml')]),
                  LiteralInput('output_format', "GML or GeoJson format",
                               abstract="""
                                (Optional) default: gml
                                gml: response as format gml
                                geojson: response as format geojson
                                """, data_type='string', default='gml')]
        outputs = [ComplexOutput('points_gml', 'Output as format GML',
                                 supported_formats=[Format('application/gml+xml')]),
                   ComplexOutput('points_geojson', 'Output as format GEOJson',
                                 supported_formats=[Format('application/geo+json')])]

        super(PointsInPolygon, self).__init__(
            self._handler,
            identifier='points_in_polygon',
            title='Process returns points is completely in a polygon',
            abstract="""""",
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        from pywps.app.exceptions import ProcessError
        from common.helpers import gdf_to_gml
        from geopandas import read_file
        import json
        # prepare data
        geomA = read_file(request.inputs['points'][0].file, engine='fiona')
        geomB = read_file(request.inputs['polygon'][0].file, engine='fiona')
        output_format = str(request.inputs['output_format'][0].data)
        # validation
        super(PointsInPolygon, self)._handler(geomA, geomB)
        predicate = geomA.within(geomB)
        pred_arr = predicate.to_numpy(dtype=bool)
        geomA = geomA[pred_arr]

        if output_format == 'gml':
            gml_str = gdf_to_gml(geomA)
            response.outputs['points_gml'].data = gml_str
        elif output_format == 'geojson':
            geojson_str = geomA.__geo_interface__
            response.outputs['points_geojson'].data = json.dumps(geojson_str)
        else:
            raise ProcessError('output_format invalid')
        return response
