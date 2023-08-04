#!/usr/bin/env python3

from pywps.app.Service import Service

# processes need to be installed in PYTHON_PATH

# from processes.sleep import Sleep
# from processes.ultimate_question import UltimateQuestion
# from processes.centroids import Centroids
from processes.sayhello import SayHello
from processes.total_length import TotalLength
from processes.overlay_operator import OverlayOperator
from processes.centroid import Centroid
from processes.simplify import Simplify
from processes.convex_hull import ConvexHull

processes = [
    SayHello(),
    TotalLength(),
    OverlayOperator(),
    Centroid(),
    Simplify(),
    ConvexHull()
]

# Service accepts two parameters:
# 1 - list of process instances
# 2 - list of configuration files
application = Service(
    processes,
    ['/pywps/default.cfg']
)