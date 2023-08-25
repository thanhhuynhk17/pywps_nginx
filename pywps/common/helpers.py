def utm_crs_from_latlon(lat, lon):
    from pyproj import CRS
    import utm

    crs_params = dict(
        proj='utm',
        zone=utm.latlon_to_zone_number(lat, lon),
        south=lat < 0
    )
    return CRS.from_dict(crs_params)

def gdf_to_gml(gdf):
    from lxml import etree
    from osgeo import ogr
    from json import dumps

    # define namespaces
    nsmap = {
        'wfs':'http://www.opengis.net/wfs',
        'gml':'http://www.opengis.net/gml',
        'feature':'http://mapserver.gis.umn.edu/mapserver'
    }
    # creat root
    root = etree.Element(etree.QName(nsmap['wfs'],'FeatureCollection'),nsmap=nsmap)
    for fea in gdf.__geo_interface__['features']:
        # create gml tree
        geojson = dumps(fea['geometry'])
        geom_gml = ogr.CreateGeometryFromJson(geojson).ExportToGML(options = ['NAMESPACE_DECL=YES'])
        geom_tree = etree.fromstring(geom_gml)
        # insert gml tree
        featureMember = etree.SubElement(root, etree.QName(nsmap['gml'],'featureMember'))
        features = etree.SubElement(featureMember, etree.QName(nsmap['feature'],'features'))
        geom = etree.SubElement(features, etree.QName(nsmap['feature'],'geometry'))
        geom.insert(0,geom_tree)
    gml_str = etree.tostring(root, pretty_print=True).decode()

    return gml_str

def predicate_validator(geomA, geomB):

    # input validation
    if len(geomA) == len(geomB):
        pass
    elif len(geomA) == 1:  # 1-to-n, invalid!
        return False
    elif len(geomB) != 1:  # n-to-n', invalid!
        return False
    # all passed
    return True