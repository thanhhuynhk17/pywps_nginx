from pywps import Process, ComplexInput, ComplexOutput, Format


class Centroids(Process):
    """Process calculating area of given polygon
    """

    def __init__(self):
        inputs = [ComplexInput('layer', 'Layer', [Format('application/gml+xml')])]
        outputs = [ComplexOutput('centroids', 'Centroids',
                            [Format('application/gml+xml')])]

        super(Centroids, self).__init__(
            self._handler,
            identifier='centroids',
            title='Process centroids',
            abstract="""Process returns the centroids from a submitted GML file""",
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        from geopandas import read_file
        from common.helpers import gdf_to_gml
        from pywps.app.exceptions import ProcessError

        # http://www.datypic.com/sc/niem21/e-gml32_MultiPoint.html
        
        # prepare data
        gdf = read_file(
            request.inputs['layer'][0].file, engine='fiona')
        try:
            gdf["geometry"] = gdf.centroid
            gml_str = gdf_to_gml(gdf)
            response.outputs['centroids'].data = gml_str
            
            return response
        except Exception as e:
            raise ProcessError(f"{str(e)}")