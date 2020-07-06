#airflow DAG, needed for airflow to pickup this dag file.

import sys

# TODO: add this to dotenv
#APP_PATH = "/Users/yipstar/real_projects/surf_python"
APP_PATH = "/home/yipstar/projects/surf_python"
sys.path.append(APP_PATH)
# print(sys.path)

from huey.dag.buoy_data import *
