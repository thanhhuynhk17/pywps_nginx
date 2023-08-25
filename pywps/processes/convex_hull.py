from pywps import Process, ComplexInput, ComplexOutput, Format


class ConvexHull(Process):
    """Process calculating area of given polygon
    """

    def __init__(self):
        inputs = [ComplexInput(
            'layer', 'Layer', [Format('application/gml+xml')])]
        outputs = [ComplexOutput('convex_hull', 'Convex_hull',
                                 [Format('application/gml+xml')])]

        super(ConvexHull, self).__init__(
            self._handler,
            identifier='convex_hull',
            title='Process convex hull',
            abstract="""Process returns the convex hull from a submitted GML file""",
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        from geopandas import read_file, GeoDataFrame
        from common.helpers import gdf_to_gml

        # prepare data
        gdf = read_file(
            request.inputs['layer'][0].file, engine='fiona')
        convex_hull = gdf.unary_union.convex_hull
        gdf_cvhull = GeoDataFrame(geometry=[convex_hull])
        response.outputs['convex_hull'].data = gdf_to_gml(gdf_cvhull)
        return response
