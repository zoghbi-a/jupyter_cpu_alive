# Copyright (c) 2024 University of Maryland

import os
from jupyter_server._tz import utcnow
from tornado.ioloop import IOLoop, PeriodicCallback
import psutil
from functools import partial

__version__ = "0.1.1"


async def update_last_activity(settings, logger, percent_min=70):
    """Checks for CPU usage and update the last activity if there is activity
    
    Parameters
    ----------
    settings: dict
        ServerApp setting dict
    logger: logging object
    percent_min: int
        Minimum CPU activity to consider as running.
    """
    # consider individual cpu's separately
    #cpu_active = [cpu>percent_min for cpu in psutil.cpu_percent(percpu=True)]
    #isactive = any(cpu_active)
    isactive = sum(psutil.cpu_percent(percpu=True)) > percent_min
    text = f"jupyter_cpu_alive activity: {isactive}"    
    if isactive:
        now = utcnow()
        settings['api_last_activity'] = now
        text += f'; activity updated to: {now}'
    logger.info(text)

def _jupyter_server_extension_points():
    return [{
        "module": "jupyter_cpu_alive"
    }]

def load_jupyter_server_extension(nb_app):
    # minimum cpu percentage
    percent_min = os.environ.get('JUPYTER_CPU_ALIVE_PERCENT_MIN', 70)
    # interval in seconds; default is 10 min
    default_interval = 10*60
    try:
        interval = os.environ.get('JUPYTER_CPU_ALIVE_INTERVAL', default_interval)
        interval = float(interval)
    except ValueError:
        nb_app.log.info(f'jupyter_cpu_alive: JUPYTER_CPU_ALIVE_INTERVAL cannot be converted to a float; using {default_interval}')
        interval = default_interval
    interval = 30
    func = partial(
        update_last_activity,
        settings=nb_app.web_app.settings,
        logger=nb_app.log,
        percent_min=percent_min,
    )
    # note that this needs the interval in milliseconds
    pc = PeriodicCallback(func, interval*1e3)
    nb_app.log.info(f'jupyter_cpu_alive starting with: percent_min: {percent_min}, interval: {interval}')
    pc.start()