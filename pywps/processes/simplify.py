from pywps import Process, ComplexInput, ComplexOutput, LiteralInput, Format


class Simplify(Process):
    """Process calculating area of given polygon
    """

    def __init__(self):
        inputs = [ComplexInput('layer', 'Layer', [Format('application/gml+xml')]),
                    LiteralInput('tolerance', 'Tolerance value', data_type='float')]
        outputs = [ComplexOutput('simplify', 'Simplify',
                            [Format('application/gml+xml')])]

        super(Simplify, self).__init__(
            self._handler,
            identifier='simplify',
            title='Process simplify',
            abstract="""Process returns the simplify of a submitted GML file""",
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        import geopandas as gpd
        from pygml.v32 import encode_v32
        from lxml import etree

        # prepare data
        gdf = gpd.read_file(
            request.inputs['layer'][0].file, engine='fiona')
        tolerance = float(request.inputs['tolerance'][0].data)
        
        gdf_simplify = gdf.simplify(tolerance=tolerance)
        if gdf_simplify.empty:
            return response

        tree = encode_v32(gdf_simplify.__geo_interface__['features'][0]['geometry'], 'simplify')
        response.outputs['simplify'].data = etree.tostring(
            tree, pretty_print=True).decode()
        return response
