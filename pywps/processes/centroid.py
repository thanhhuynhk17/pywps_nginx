from pywps import Process, ComplexInput, ComplexOutput, Format


class Centroid(Process):
    """Process calculating area of given polygon
    """

    def __init__(self):
        inputs = [ComplexInput('layer', 'Layer', [Format('application/gml+xml')])]
        outputs = [ComplexOutput('centroid', 'Centroid',
                            [Format('application/gml+xml')])]

        super(Centroid, self).__init__(
            self._handler,
            identifier='centroid',
            title='Process centroid',
            abstract="""Process returns the centroid from a submitted GML file""",
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
        gdf_centroid = gdf["geometry"][0].centroid
        # if gdf_centroid.empty:
        #     return response

        tree = encode_v32(gdf_centroid.__geo_interface__, 'centroid')
        response.outputs['centroid'].data = etree.tostring(
            tree, pretty_print=True).decode()
        return response
