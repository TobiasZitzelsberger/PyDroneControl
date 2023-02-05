import utm
import xml.etree.ElementTree as ET


def convert_utm(utm_data):
    latlon_data = utm.to_latlon(utm_data.easting, utm_data.northing, 32)


def get_ground_data(path):

    tree = ET.parse(path)
    root = tree.getroot()

    for cityObject in root.iter('{http://www.opengis.net/citygml/1.0}cityObjectMember'):
        print(cityObject)
        for groundSurface in cityObject.iter('{http://www.opengis.net/citygml/building/1.0}GroundSurface'):
            print(groundSurface)
            for posList in groundSurface.iter('{http://www.opengis.net/gml}posList'):
                print(posList.text)
                print()
