import arcpy
import os
from math import sin, cos
from math import radians


def rotate(point, origin, angle):
    """
    Rotate a point around the origin given an angle (in radians).
    """
    ox, oy = origin
    px, py = point

    qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
    qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy)
    
    return qx, qy


def create_feature_class(in_features, out_features):
    """
    Create an empty feature class with field.
    """

    describe = arcpy.Describe(in_features)
    
    arcpy.management.CreateFeatureclass(
        *os.path.split(out_features), 
        geometry_type='POLYGON',
        spatial_reference=describe.spatialReference
    )

    # Add a field to the output to store the input's object id
    arcpy.management.AddField(out_features, 'ORIG_FID', 'LONG')
    
    return

    
def create_rotated_features(in_features, out_features, origin, angle):
    """
    Create the rotated features.
    """

    with arcpy.da.SearchCursor(in_features, ['SHAPE@', 'OID@']) as scursor:
        with arcpy.da.InsertCursor(out_features, ['SHAPE@', 'ORIG_FID']) as icursor:
            for row in scursor:
               
                # Assuming single-part polygon features for simplicity.
                # Iterate through each coordinate, and pack rotated
                # coordinates into list.
                coords = []
                for pt in scursor[0][0]:
                    rotated_coords = rotate((pt.X, pt.Y), origin, angle)
                    coords += [rotated_coords]

                oid = scursor[1]
            
                # Insert coordinates as a list
                icursor.insertRow([coords, oid])


if __name__ == '__main__':

    in_features = arcpy.GetParameterAsText(0)
    out_features = arcpy.GetParameterAsText(1)
    angle = radians(arcpy.GetParameter(2))
    option = arcpy.GetParameterAsText(3)
    feature_set = arcpy.GetParameter(4)
    point = arcpy.GetParameterAsText(5)
    
    create_feature_class(in_features, out_features)
    
    if option == 'POINT':
        # Create a geometry from the x,y-coordinates
        rotation_point = [float(i) for i in point.split(' ')]

    elif option == 'FEATURESET':
        # Extract the point from the feature set
        with arcpy.da.SearchCursor(feature_set, 'SHAPE@XY') as cursor:
            for row in cursor:
                rotation_point = row[0]
                # Use the first point, skip any others
                break
    

    create_rotated_features(in_features, out_features, rotation_point, angle)
