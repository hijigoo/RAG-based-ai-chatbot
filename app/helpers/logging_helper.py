import sys
import logging

logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s,%(module)s,%(processName)s,%(levelname)s,%(message)s', level=logging.INFO,
                    stream=sys.stderr)
