from pywps import Process, ComplexInput, ComplexOutput, LiteralInput, Format


class Buffer(Process):
    """Process calculating area of given polygon
    """

    def __init__(self):
        inputs = [ComplexInput('layer', 'Layer', [Format('application/gml+xml')]),
                  LiteralInput('distance', 'Distance in meters',
                               data_type='float'),
                  LiteralInput('cap_style', 'Specifies the shape of buffered line endings',
                               abstract='''
                                All available styles: round, square, flat. Default: round.
                                round: results in circular line endings.
                                Both square and flat result in rectangular line endings.
                                Only flat will end at the original vertex.
                                While square involves adding the buffer width.''',
                               data_type='string', default='round'),
                  LiteralInput('join_style', 'Specifies the shape of buffered line midpoints',
                               abstract='''
                                All available styles: round, bevel, mitre. Default round.
                                round: results in rounded shapes.
                                bevel: results in a beveled edge that touches the original vertex.
                                mitre: results in a single vertex that is beveled.''',
                               data_type='string', default='round'),
                  ]
        outputs = [ComplexOutput('buffer', 'Buffer',
                                 [Format('application/gml+xml')])]

        super(Buffer, self).__init__(
            self._handler,
            identifier='buffer',
            title='Process buffer',
            abstract="""Process returns the buffer of a submitted GML file""",
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        from common.helpers import gdf_to_gml
        from geopandas import read_file
        from numpy import pi

        gdf = read_file(request.inputs['layer'][0].file, engine='fiona')
        distance = float(request.inputs['distance'][0].data)
        cap_style = str(request.inputs['cap_style'][0].data)
        join_style = str(request.inputs['join_style'][0].data)
        if gdf.empty or distance <= 0:
            return response
        CAP_STYLES = {'round': 1, 'flat': 2, 'square': 3}
        JOIN_STYLES = {'round': 1, 'bevel': 2, 'mitre': 3}

        # # project to utm crs
        # centroid = gdf.centroid
        # utm_crs = utm_crs_from_latlon(centroid[0].y, centroid[0].x)
        # # buffering in meter
        # gdf_buffer = gdf.to_crs(utm_crs)
        # gdf_buffer["geometry"] = gdf_buffer.buffer(distance)
        # gdf_buffer = gdf_buffer.to_crs(4326) # re-projected

        # convert distance from meters to degrees
        R = 6378137  # earth's radius in meters
        deg = distance * 180 / (pi*R)

        gdf_buffer = gdf.copy()
        gdf_buffer["geometry"] = gdf_buffer.buffer(deg,
                                                   cap_style=CAP_STYLES[cap_style],
                                                   join_style=JOIN_STYLES[join_style])

        # make multi polygon
        gml_str = gdf_to_gml(gdf_buffer)
        response.outputs['buffer'].data = gml_str

        return response
