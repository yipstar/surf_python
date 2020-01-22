import os
from datetime import datetime, timedelta, timezone

# db stuff
from airflow.hooks.postgres_hook import PostgresHook
from sqlalchemy.pool import NullPool

# External modules
import requests,yaml,matplotlib.pyplot as plt,numpy as np,pandas as pd,scipy
