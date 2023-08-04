from pywps import Process, ComplexInput, LiteralOutput, Format


class TotalLength(Process):
    """Process calculating area of given polygon
    """

    def __init__(self):
        inputs = [ComplexInput('layer', 'Layer',
                            [Format('application/gml+xml')])]
        outputs = [LiteralOutput('total_length', 'Total length', data_type='string')]

        super(TotalLength, self).__init__(
            self._handler,
            identifier='total_length',
            title='Process total length',
            abstract="""Process returns the total length of each
                feature from a submitted GML file""",
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        import fiona as fio
        from shapely import geometry
        import geopandas as gpd
        
        data_file =  gpd.read_file(request.inputs['layer'][0].file, engine='fiona')
        data_file.set_crs(4326, inplace=True)

        utm_crs = self.utm_crs_from_latlon(data_file["geometry"][0].centroid.y,
                                            data_file["geometry"][0].centroid.x)
        data_file.to_crs(utm_crs,inplace=True)

        total_length = data_file["geometry"].length

        response.outputs['total_length'].data = f'Total length: {total_length[0]} (m)'

        return response

    def utm_crs_from_latlon(self, lat, lon):
        import utm
        from pyproj import CRS

        crs_params = dict(
            proj = 'utm',
            zone = utm.latlon_to_zone_number(lat, lon),
            south = lat < 0
            )
        return CRS.from_dict(crs_params)