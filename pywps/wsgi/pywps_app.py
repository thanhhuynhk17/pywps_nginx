#!/usr/bin/env python3

from pywps.app.Service import Service

# processes need to be installed in PYTHON_PATH

# from processes.sleep import Sleep
# from processes.ultimate_question import UltimateQuestion
# from processes.centroids import Centroids
from common.pywps_services import processes

# Service accepts two parameters:
# 1 - list of process instances
# 2 - list of configuration files
application = Service(
    processes,
    ['/pywps/default.cfg']
)