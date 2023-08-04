from pywps import Process, ComplexInput, LiteralInput, ComplexOutput, Format

class OverlayOperator(Process):
    """Process returns the overlay result of two features from a submitted GML file
    """
    def __init__(self):
        inputs = [ComplexInput('left_layer', 'Layer', [Format('application/gml+xml')]),
                ComplexInput('right_layer', 'Layer', [Format('application/gml+xml')]),
                LiteralInput('operator', 'Overlay operator', data_type='string')]
        outputs = [ComplexOutput('overlay', 'Result layer', [Format('application/gml+xml')])]

        super(OverlayOperator, self).__init__(
            self._handler,
            identifier='overlay_operator',
            title='Process a overlay operator',
            abstract="""Process returns the overlay result of two features from a submitted GML file""",
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
        gdf_left =  gpd.read_file(request.inputs['left_layer'][0].file, engine='fiona')
        gdf_right =  gpd.read_file(request.inputs['right_layer'][0].file, engine='fiona')
        operator = request.inputs['operator'][0].data

        gdf_overlay = gdf_left.overlay(gdf_right, how=operator)
        if gdf_overlay.empty:
            return response
        
        tree = encode_v32(gdf_overlay.__geo_interface__['features'][0]['geometry'], 'overlay')
        response.outputs['overlay'].data = etree.tostring(tree, pretty_print=True).decode()
        return response