import logging

from aiomisc.log import basic_config

from api.app import run_app


basic_config(logging.DEBUG, buffered=True)

run_app()
