from processes.sayhello import SayHello
from processes.total_length import TotalLength
from processes.overlay_operator import OverlayOperator
from processes.centroids import Centroids
from processes.simplify import Simplify
from processes.convex_hull import ConvexHull
from processes.buffer import Buffer
from processes.points_in_polygon import PointsInPolygon

# [BEGIN] predicates
from processes.predicates.contains import Contains
from processes.predicates.covers import Covers
from processes.predicates.covered_by import Covered_by
from processes.predicates.crosses import Crosses
from processes.predicates.disjoint import Disjoint
# from processes.predicates.dwithin import Dwithin
from processes.predicates.equals import Equals
from processes.predicates.intersects import Intersects
from processes.predicates.overlaps import Overlaps
from processes.predicates.touches import Touches
from processes.predicates.within import Within
# [END] predicates

processes = [
    SayHello(),
    TotalLength(),
    OverlayOperator(),
    Centroids(),
    Simplify(),
    ConvexHull(),
    Buffer(),
    PointsInPolygon(),
# [BEGIN] predicates
    Contains(),
    Covers(),
    Covered_by(),
    Crosses(),
    Disjoint(),
    # Dwithin(),
    Equals(),
    Intersects(),
    Overlaps(),
    Touches(),
    Within()
# [END] predicates

]