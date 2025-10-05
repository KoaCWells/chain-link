"""
Sets up initial configurations for logging. Used to configure both console logs and output file logs.
Code contributors: Koa Wells koa.wells@hotmail.com
"""
import logging
from pathlib import Path
from datetime import datetime

output_file = Path(__file__).parent / 'logs' / f'{datetime.now()}.log'

def setup_logger():
  """
  Sets up the configuration for the ChainLink logger
  :return: None
  """
  logging.basicConfig(
    level=logging.INFO,  # minimum level to log
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
      logging.FileHandler(output_file),  # writes to a file
      logging.StreamHandler()          # also prints to console
    ]
  )