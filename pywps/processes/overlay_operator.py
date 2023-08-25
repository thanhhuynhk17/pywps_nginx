from pywps import Process, ComplexInput, LiteralInput, ComplexOutput, Format

class OverlayOperator(Process):
    """Process returns the overlay result of two features from a submitted GML file
    """
    def __init__(self):
        inputs = [ComplexInput('left_layer', 'Layer', [Format('application/gml+xml')]),
                ComplexInput('right_layer', 'Layer', [Format('application/gml+xml')]),
                LiteralInput('operator', "Overlay operator",
                                abstract='All available operators: intersection, union, identity, symmetric_difference, difference', data_type='string')]
        outputs = [ComplexOutput('overlay', 'Result layer', [Format('application/gml+xml')])]

        super(OverlayOperator, self).__init__(
            self._handler,
            identifier='overlay_operator',
            title='Process a overlay operator',
            abstract="""Process returns the overlay result of two features from submitted GML files""",
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        from geopandas import read_file
        from common.helpers import gdf_to_gml
        from pywps.app.exceptions import ProcessError

        # prepare data
        gdf_left =  read_file(request.inputs['left_layer'][0].file, engine='fiona')
        gdf_right =  read_file(request.inputs['right_layer'][0].file, engine='fiona')
        operator = str(request.inputs['operator'][0].data)

        try:
            gdf_overlay = gdf_left.overlay(gdf_right, how=operator)
        except ValueError as e:
            raise ProcessError(f"ValueError: {str(e)}")
        if gdf_overlay.empty:
            return response
        
        gml_str = gdf_to_gml(gdf_overlay)
        response.outputs['overlay'].data = gml_str
        return response