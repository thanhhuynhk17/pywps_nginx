#!/usr/bin/env python3

from pywps.app.Service import Service

# processes need to be installed in PYTHON_PATH

# from processes.sleep import Sleep
# from processes.ultimate_question import UltimateQuestion
# from processes.centroids import Centroids
from processes.sayhello import SayHello
# from processes.feature_count import FeatureCount
# from processes.buffer import Buffer
# from processes.area import Area

processes = [
    # FeatureCount(),
    SayHello(),
    # Centroids(),
    # UltimateQuestion(),
    # Sleep(),
    # Buffer(),
    # Area()
]

# Service accepts two parameters:
# 1 - list of process instances
# 2 - list of configuration files
application = Service(
    processes,
    ['/pywps/default.cfg']
)